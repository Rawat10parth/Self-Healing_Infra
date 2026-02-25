resource "aws_launch_template" "app_template" {
  name_prefix   = "self-healing-template"
  image_id      = "ami-02b49a24cfb95941c"
  instance_type = "t2.micro"

  vpc_security_group_ids = [aws_security_group.web_sg.id]

  iam_instance_profile {
    name = aws_iam_instance_profile.ec2_cloudwatch_instance_profile.name
  }

  user_data = base64encode(<<EOF
#!/bin/bash
sudo apt update -y
sudo apt install -y apache2
sudo systemctl start apache2
sudo systemctl enable apache2
echo "<h1>Self Healing Infra Running</h1>" > /var/www/html/index.html
EOF
  )
}

resource "aws_autoscaling_group" "app_asg" {
  name                 = "self-healing-asg"
  vpc_zone_identifier  = data.aws_subnets.default.ids
  target_group_arns    = [aws_lb_target_group.app_tg.arn]
  min_size             = 1
  max_size             = 1
  desired_capacity     = 1

  launch_template {
    id      = aws_launch_template.app_template.id
    version = "$Latest"
  }

  health_check_type = "ELB"
}