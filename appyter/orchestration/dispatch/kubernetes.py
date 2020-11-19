''' Launch kubernetes job from within a kubernetes cluster
'''

import json
import logging
logger = logging.getLogger(__name__)

from appyter.util import run_in_executor


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

@run_in_executor
def dispatch(job=None, namespace='default', debug=False, **kwargs):
  logger.info(f"starting {job['id']}")
  from kubernetes import client, config
  config.load_incluster_config()
  coreV1 = client.CoreV1Api()
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
  #
  for event in endless_watch(batchV1.list_namespaced_job, namespace, 
    label_selector=f"job-name={job['id']}"
  ):
    logger.debug(str(event))
    event_type = event['type']
    event_job = event['object']
    if event_type == 'MODIFIED':
      if event_job.status.succeeded or event_job.status.failed:
        break
  #
  if not debug:
    batchV1.delete_namespaced_job(job['id'], namespace)
    # delete associated pod(s)
    for event_pod in coreV1.list_namespaced_pod(namespace, label_selector=f"job-name={job['id']}", watch=False).items:
      coreV1.delete_namespaced_pod(event_pod.metadata.name, namespace)
  #
  logger.info(f"{job['id']} completed")
