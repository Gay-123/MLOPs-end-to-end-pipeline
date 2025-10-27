provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "rg" {
  name     = "mlopsrggayathri01"
  location = "eastasia"
}

resource "azurerm_container_registry" "acr" {
  name                = "mlopsacr2025gayathri"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = true
}

resource "azurerm_kubernetes_cluster" "aks" {
  name                = "mlopsaksfrauddetect01"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  dns_prefix          = "mlopsdns2025"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_B2s"
  }

  identity {
    type = "SystemAssigned"
  }

  depends_on = [azurerm_container_registry.acr]
}
