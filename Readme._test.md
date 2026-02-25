<!-- Commands to run files

terraform apply -target=aws_ecr_repository.lambda_repo

aws ecr get-login-password --region ap-south-1 | \
docker login --username AWS --password-stdin <user-id>.dkr.ecr.ap-south-1.amazonaws.com

docker build -t self-healing-lambda .

docker tag self-healing-lambda:latest <user-id>.dkr.ecr.ap-south-1.amazonaws.com/self-healing-lambda:latest

docker push <user-id>.dkr.ecr.ap-south-1.amazonaws.com/self-healing-lambda:latest -->
