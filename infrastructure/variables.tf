variable "resource_group_name" {
  default = "mlopsrggayathri01"
}

variable "location" {
  default = "eastasia"
}

variable "acr_name" {
  default = "mlopsacr2025gayathri"
}

variable "aks_name" {
  default = "mlopsaksfrauddetect01"
}

variable "node_count" {
  default = 1
}

variable "vm_size" {
  default = "Standard_B2s"
}

variable "dns_prefix" {
  default = "mlopsdns2025"
}

variable "client_id" {}
variable "client_secret" {}
variable "tenant_id" {}
variable "subscription_id" {}
