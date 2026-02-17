import boto3
import json

autoscaling = boto3.client('autoscaling')

def lambda_handler(event, context):
    try:
        message = json.loads(event['Records'][0]['Sns']['Message'])
        print("SNS Message:", message)

        instance_id = message['Trigger']['Dimensions'][0]['value']
        print("Instance ID:", instance_id)

        autoscaling.set_instance_health(
            InstanceId=instance_id,
            HealthStatus='Unhealthy',
            ShouldRespectGracePeriod=False
        )

        print("Marked unhealthy → ASG will replace instance")

    except Exception as e:
        print("Error:", str(e))
