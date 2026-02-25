resource "aws_ecr_repository" "lambda_repo" {
  name = "self-healing-lambda"
}

resource "aws_lambda_function" "self_healing_lambda" {
  function_name = "self-healing-lambda"
  role          = aws_iam_role.lambda_exec.arn

  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.lambda_repo.repository_url}:latest"

  timeout       = 30
  memory_size   = 256
}