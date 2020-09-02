''' Launch kubernetes job from within a kubernetes cluster
'''

import json


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

def dispatch(job=None, namespace='default', debug=False, **kwargs):
  from kubernetes import client, config
  config.load_incluster_config()
  batchV1 = client.BatchV1Api()
  batchV1.create_namespaced_job(
    namespace=namespace,
    body=client.V1Job(
      api_version='batch/v1',
      kind='Job',
      metadata=client.V1ObjectMeta(
        name=job['session'],
      ),
      spec=client.V1JobSpec(
        template=client.V1PodTemplateSpec(
          spec=client.V1PodSpec(
            restart_policy='Never',
            containers=[
              client.V1Container(
                name=f"appyter-{job['session']}",
                image=job['image'],
                command=['appyter', 'orchestration', 'job', json.dumps(job)],
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
    label_selector=f"job-name={job['session']}"
  ):
    event_type = event['type']
    event_job = event['object']
    if event_type == 'MODIFIED':
      if event_job.status.succeeded or event_job.status.failed:
        break
  #
  if not debug:
    batchV1.delete_namespaced_job(job['session'], namespace)
