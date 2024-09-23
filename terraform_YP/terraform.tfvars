virtual_machines = {
  "vm-2" = {
    vm_name   = "vm-sprint12-02" # Имя ВМ
    vm_desc   = "Описание vm-sprint12-02" # Описание
    vm_cpu    = 2 # Кол-во ядер процессора
    ram       = 2 # Оперативная память в ГБ
    disk      = 15 # Объём диска в ГБ
    disk_name = "vm-2-disk" # Название диска
    template  = "fd8qh3qqmbq35jn5920n" # ID образа ОС для использования
    preemptible = true
  },
  "vm-3" = {
    vm_name   = "vm-sprint12-03"
    vm_desc   = "Описание vm-sprint12-03"
    vm_cpu    = 2
    ram       = 2
    disk      = 16
    disk_name = "vm-3-disk"
    template  = "fd8849jlk3ok903lqcuv"
    preemptible = true
  },
  "vm-4" = {
    vm_name   = "vm-sprint12-04"
    vm_desc   = "Описание vm-sprint12-04"
    vm_cpu    = 2
    ram       = 2
    disk      = 17
    disk_name = "vm-4-disk"
    template  = "fd8qh3qqmbq35jn5920n"
    preemptible = true
    
  }
}

network = {
    existing_network_id = "enpq8hrot41agq9ug68l"
    existing_subnet_id = "e9bsdtj7vme4iddaq7qb"
}