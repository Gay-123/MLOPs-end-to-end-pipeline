# variables.tf
variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
  default     = "mlops-rg"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "eastasia"
}

variable "acr_name" {
  description = "Name of Azure Container Registry"
  type        = string
  default     = "mlopsacr-gayathri01"
}

variable "aks_name" {
  description = "Name of the AKS cluster"
  type        = string
  default     = "fraud-mlops-aks"
}

variable "node_count" {
  description = "Number of nodes in AKS"
  type        = number
  default     = 1
}

variable "vm_size" {
  description = "VM size for AKS node pool"
  type        = string
  default     = "Standard_B2s"
}

variable "dns_prefix" {
  description = "DNS prefix for AKS"
  type        = string
  default     = "mlops"
}
