import json
import logging
logger = logging.getLogger(__name__)

from appyter.execspec.spec import AbstractExecutor
from appyter.ext.asyncio.run_in_executor import run_in_executor
from appyter.ext.asyncio.try_n_times import async_try_n_times

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
  '''
  protocol = 'kube'

  def __init__(self, url=None, **kwargs) -> None:
    super().__init__(url=url, **kwargs)
    from kubernetes import config
    config.load_incluster_config()

  async def submit(self, job):
    @run_in_executor
    def _submit(job, namespace='default'):
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
                    image=job['image'],
                    command=['appyter', 'orchestration', 'job', json.dumps(job)],
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
            backoff_limit=1,
          ),
        ),
      )
      return job['id']
      #
    return await async_try_n_times(3,
      _submit,
      job,
      namespace=self.executor_options.get('namespace', 'default'),
    )

  async def wait_for(self, run_id):
    @run_in_executor
    def _wait_for(run_id, namespace='default', debug=False):
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
      if debug:
        batchV1.delete_namespaced_job(run_id, namespace)
        # delete associated pod(s)
        for event_pod in coreV1.list_namespaced_pod(namespace, label_selector=f"job-name={run_id}", watch=False).items:
          coreV1.delete_namespaced_pod(event_pod.metadata.name, namespace)
      logger.info(f"{run_id} completed")
      return 0
    return await _wait_for(
      run_id,
      namespace=self.executor_options.get('namespace', 'default'),
      debug=self.executor_options.get('debug'),
    )
