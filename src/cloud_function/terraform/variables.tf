variable "yc_token" {
  description = "Yandex Cloud IAM Token"
}

variable "yc_cloud_id" {
  description = "ID of the Yandex Cloud"
}

variable "yc_folder_id" {
  description = "ID of the folder in Yandex Cloud"
}

variable "yc_zone" {
  description = "Yandex Cloud zone (e.g., ru-central1-a)"
}

variable "gh_token" {
  description = "GitHub API token"
  sensitive   = true
}

variable "db_host" {
  description = "PostgreSQL host"
}

variable "db_port" {
  description = "PostgreSQL port"
  default     = "5432"
}

variable "db_name" {
  description = "PostgreSQL database name"
}

variable "db_user" {
  description = "PostgreSQL user"
}

variable "db_password" {
  description = "PostgreSQL password"
  sensitive   = true
}

variable "service_account_id" {
  description = "ID of the service account for the function"
}
