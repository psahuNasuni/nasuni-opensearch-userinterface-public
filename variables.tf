
################### Lambda Provisioning Specific Variables ###################
variable "runtime" {
  default = "python3.8"
}
variable "region" {
  default = "us-east-2"
}
variable "aws_profile" {
  default = "nasuni"
}
variable "admin_secret" {
  default = "nasuni-labs-os-admin"
}
variable "internal_secret" {
  default = ""
}
variable "stage_name" {
  default = "dev"
  description = "api stage name"
}
#########################################
