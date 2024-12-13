provider "yandex" {
  token     = var.yc_token
  cloud_id  = var.yc_cloud_id
  folder_id = var.yc_folder_id
  zone      = var.yc_zone
}

resource "yandex_function" "github_parser" {
  name       = "github_parser"
  runtime    = "python39"
  entrypoint = "main.handler"

  content {
    source_path = "./function.zip"
  }

  environment = {
    GH_TOKEN    = var.gh_token
    DB_HOST     = var.db_host
    DB_PORT     = var.db_port
    DB_NAME     = var.db_name
    DB_USER     = var.db_user
    DB_PASSWORD = var.db_password
  }
}

resource "yandex_function_iam_binding" "invoker" {
  function_id = yandex_function.github_parser.id
  members     = ["serviceAccount:${var.service_account_id}"]
}

resource "yandex_function_trigger" "scheduler" {
  name = "github_parser_trigger"

  function_id = yandex_function.github_parser.id

  cron_expression = "0 */12 * * *"

  invoke_function {
    retry_settings {
      retry_attempts = 3
      interval       = "10s"
    }
  }
}

variable "yc_token" {}
variable "yc_cloud_id" {}
variable "yc_folder_id" {}
variable "yc_zone" {}
variable "gh_token" {}
variable "db_host" {}
variable "db_port" {}
variable "db_name" {}
variable "db_user" {}
variable "db_password" {}
variable "service_account_id" {}
