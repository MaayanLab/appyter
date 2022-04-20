import logging
logger = logging.getLogger(__name__)

from appyter.execspec.spec import AbstractExecutor
from appyter.ext.asyncio.try_n_times import async_try_n_times
from appyter.ext.asyncio.helpers import ensure_async
from appyter.ext.dict import dict_merge

def endless_watch(*args, **kwargs):
  from kubernetes import watch
  w = watch.Watch()
  s = iter(w.stream(*args, **kwargs))
  v = None
  while True:
    try:
      event = next(s)
      v = event['object'].metadata.resource_version
      yield event
    except StopIteration:
      s = iter(w.stream(*args, **kwargs, resource_version=v))

class KubernetesExecutor(AbstractExecutor):
  ''' Run executions as kubernetes jobs
  Example uri:
  kube::maayanlab/myimage:latest?namespace=default
  '''
  protocol = 'kube'

  def __init__(self, url=None, **kwargs) -> None:
    super().__init__(url=url, **kwargs)
    from kubernetes import config
    config.load_incluster_config()

  def _submit(self, job, namespace='default'):
    from kubernetes import client
    batchV1 = client.BatchV1Api()
    batchV1.create_namespaced_job(
      namespace=namespace,
      body=client.V1Job(
        api_version='batch/v1',
        kind='Job',
        metadata=client.V1ObjectMeta(
          name=job['id'],
          annotations={
            f"container.apparmor.security.beta.kubernetes.io/appyter-{job['id']}": 'unconfined'
          },
        ),
        spec=client.V1JobSpec(
          template=client.V1PodTemplateSpec(
            spec=client.V1PodSpec(
              restart_policy='Never',
              containers=[
                client.V1Container(
                  name=f"appyter-{job['id']}",
                  image=self.url,
                  command=[
                    'appyter', 'nbexecute',
                    *(
                      f"--{k}={v}" if len(k) > 1 else f"-{k}{v}"
                      for k, v in dict_merge(
                        {
                          's': job['url'],
                          'w': job['cwd'],
                          'data-dir': job['storage'],
                        },
                        **self.executor_options.get('args', {})
                      ).items()
                    ),
                    job['ipynb'],
                  ],
                  security_context=client.V1SecurityContext(
                    privileged=True,
                    capabilities=client.V1Capabilities(
                      add=['SYS_ADMIN'],
                    ),
                  ),
                  volume_mounts=[
                    client.V1VolumeMount(
                      name='fuse',
                      mount_path='/dev/fuse',
                    )
                  ],
                ),
              ],
              volumes=[
                client.V1Volume(
                  name='fuse',
                  host_path=client.V1HostPathVolumeSource(
                    path='/dev/fuse',
                  )
                ),
              ],
            ),
          ),
          ttlSecondsAfterFinished=120,
          backoff_limit=1,
        ),
      ),
    )
  submit = ensure_async(_submit)

  def _wait_for(self, run_id, namespace='default', debug=False):
    from kubernetes import client
    coreV1 = client.CoreV1Api()
    batchV1 = client.BatchV1Api()
    for event in endless_watch(batchV1.list_namespaced_job, namespace, 
      label_selector=f"job-name={run_id}"
    ):
      logger.debug(str(event))
      event_type = event['type']
      event_job = event['object']
      if event_type == 'MODIFIED':
        if event_job.status.succeeded or event_job.status.failed:
          break
    logger.info(f"{run_id} completed")
    return 0
  wait_for = ensure_async(_wait_for)

  async def _run(self, **job):
    yield dict(type='status', data=f"Submitting appyter for execution..")
    await async_try_n_times(3, self._submit, job, namespace=self.executor_options.get('namespace', 'default'))
    yield dict(type='status', data=f"Queued successfully, your execution will begin when resources are available..")
    # TODO: kubernetes probably reports some additional status we can report
    await self._wait_for(job['id'], namespace=self.executor_options.get('namespace', 'default'), debug=self.executor_options.get('debug'))
    yield dict(type='status', data=f"Job completed.")
