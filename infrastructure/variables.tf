variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
  default     = "mlopsrggayathri01"
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "eastasia"
}

variable "acr_name" {
  description = "Name of Azure Container Registry"
  type        = string
  default     = "mlopsacr2025gayathri"
}

variable "aks_name" {
  description = "Name of the AKS cluster"
  type        = string
  default     = "mlopsaksfrauddetect01"
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
  default     = "mlopsdns2025"
}

variable "client_id" {
  description = "Azure Client ID"
  type        = string
}

variable "client_secret" {
  description = "Azure Client Secret"
  type        = string
}

variable "tenant_id" {
  description = "Azure Tenant ID"
  type        = string
}

variable "subscription_id" {
  description = "Azure Subscription ID"
  type        = string
}
