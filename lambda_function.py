import boto3
import json
import datetime

asg = boto3.client("autoscaling")
cw  = boto3.client("cloudwatch")

def get_instances_in_asg(asg_name):
    resp = asg.describe_auto_scaling_groups(
        AutoScalingGroupNames=[asg_name]
    )

    groups = resp.get("AutoScalingGroups", [])

    if not groups:
        raise Exception(f"ASG {asg_name} not found")

    inst = [
        i["InstanceId"]
        for i in groups[0]["Instances"]
        if i["LifecycleState"] == "InService"
    ]

    if not inst:
        raise Exception("No InService instances found")
    
    return inst

def get_cpu(instance_id):
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(minutes=10)

    stats = cw.get_metric_statistics(
        Namespace="AWS/EC2",
        MetricName="CPUUtilization",
        Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
        StartTime=start,
        EndTime=end,
        Period=60,
        Statistics=["Average"]
    )

    datapoints = stats.get("Datapoints", [])
    if not datapoints:
        return 0

    latest = sorted(datapoints, key=lambda x: x["Timestamp"])[-1]
    return latest["Average"]

def lambda_handler(event, context):
    print("Event:", json.dumps(event))

    msg = json.loads(event["Records"][0]["Sns"]["Message"])
    dimensions = msg["Trigger"]["Dimensions"]

    asg_name = ""
    for d in dimensions:
        if d["name"] == "AutoScalingGroupName":
            asg_name = d["value"]

    if not asg_name:
        raise Exception("ASG name missing from alarm message")

    instances = get_instances_in_asg(asg_name)

    # Find instance with highest CPU usage
    max_cpu = -1
    bad_instance = instances[0]

    for iid in instances:
        cpu = get_cpu(iid)
        print(f"Instance {iid} CPU: {cpu}")
        if cpu > max_cpu:
            max_cpu = cpu
            bad_instance = iid

    print(f"Marking {bad_instance} as Unhealthy")

    asg.set_instance_health(
        InstanceId=bad_instance,
        HealthStatus="Unhealthy",
        ShouldRespectGracePeriod=False
    )

    return {"replaced_instance": bad_instance}