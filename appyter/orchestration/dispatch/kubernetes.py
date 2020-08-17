''' Launch kubernetes job from within a kubernetes cluster
'''

import json

def dispatch(job=None, namespace='default', **kwargs):
  from kubernetes import client, config
  config.load_incluster_config()
  client.BatchV1Api().create_namespaced_job(
    namespace=namespace,
    body=client.V1Job(
      api_version='batch/v1',
      kind='Job',
      metadata=client.V1ObjectMeta(
        name=job['session'],
      ),
      spec=client.V1JobSpec(
        template=client.V1PodTemplateSpec(
          metadata=client.V1ObjectMeta(
            labels=dict(
              app=f"appyter-{job['session']}",
            )
          ),
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
        backoff_limit=4
      ),
    ),
  )
  # TODO: watch job, on job completed return
