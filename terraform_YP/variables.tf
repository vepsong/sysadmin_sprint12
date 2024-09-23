variable "virtual_machines" {
 default = ""
}

#variable "existing_network_id" {
#  description = "ID of the existing VPC network"
#  type        = string
#}

variable "network" {
  description = "Map containing the existing network and subnet IDs"
  type = object({
    existing_network_id = string
    existing_subnet_id  = string
  })
}