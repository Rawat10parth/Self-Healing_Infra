import boto3

ec2 = boto3.client('ec2')

def lambda_handler(event, context):
    print("Event:", event)

    # Get instance ID from CloudWatch alarm
    try:
        instance_id = event['detail']['instance-id']
    except:
        print("Instance ID not found")
        return

    print(f"Restarting instance {instance_id}")

    ec2.reboot_instances(InstanceIds=[instance_id])

    return {
        "status": "Instance reboot triggered"
    }
