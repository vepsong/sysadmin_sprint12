import json
import subprocess

def main():
    # Укажите директорию с Terraform
    terraform_dir = '/home/sprint12_admin/sysadmin_sprint12/terraform_YP'

    # Загрузка параметров аутентификации из .auth.json
    try:
        with open('.auth.json') as config_file:
            config = json.load(config_file)
        ansible_user = config['ansible_user']
        ansible_password = config['ansible_password']
    except FileNotFoundError:
        print("Файл .auth.json не найден.")
        return
    except KeyError:
        print("Неправильный формат файла .auth.json.")
        return

    # Запуск команды terraform output в указанной директории
    try:
        output = subprocess.check_output(['terraform', 'output', '-json'], cwd=terraform_dir)
        data = json.loads(output)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении Terraform: {e}")
        return
    except json.JSONDecodeError:
        print("Ошибка при разборе JSON-вывода Terraform.")
        return

    # Проверка наличия ключа vm_nat_ip и получение IP-адресов
    if 'vm_nat_ip' in data and 'value' in data['vm_nat_ip']:
        vm_nat_ip_value = data['vm_nat_ip']['value']

        # Генерация inventory.yaml
        with open('inventory.yaml', 'w') as f:
            f.write("linux: #Группа хостов\n")
            f.write("  children: #Обозначение, что будет подгруппа хостов\n")
            f.write("    nginx: #Имя подгруппы хостов\n")
            f.write("      hosts: #Узлы группы\n")

            # Итерация по IP-адресам и запись в файл
            for vm, ip in vm_nat_ip_value.items():
                host_name = f"{vm}"  # Используем имя машины
                f.write(f"        {host_name}:\n")
                f.write(f"          ansible_host: {ip}\n")

            # Добавление переменных
            f.write("  vars: #Переменные, доступные или используемые для всех подгрупп\n")
            f.write(f'    ansible_user: "{ansible_user}"\n')
            f.write(f'    ansible_password: "{ansible_password}"\n')
            f.write('    connection_protocol: ssh #тип подключения\n')
            f.write('    ansible_become: false #Становиться ли другим пользователем после подключения\n')

        print("inventory.yaml успешно сгенерирован.")

if __name__ == '__main__':
    main()
