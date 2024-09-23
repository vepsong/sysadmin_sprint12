import json
import subprocess
import requests

HOST_NGINX_PROXY_VM_NAME = "vm-2"  # Имя хоста-прокси
HOST_NGINX_PROXY_VM_PORT = 3000
NUM_REQUESTS = 10  # Количество запросов для тестирования


def get_terraform_output(terraform_dir):
    """Запуск команды terraform output для получения IP-адресов."""
    try:
        output = subprocess.check_output(['terraform', 'output', '-json'], cwd=terraform_dir)
        data = json.loads(output)
        return data
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении Terraform: {e}")
        return None
    except json.JSONDecodeError:
        print("Ошибка при разборе JSON-вывода Terraform.")
        return None


def find_vm_name_by_ip(ip, terraform_data):
    """Поиск имени ВМ по IP-адресу."""
    for vm_name, vm_data in terraform_data['vm_nat_ip']['value'].items():
        if vm_data == ip:
            return vm_name
    return 'Неизвестно'


def send_request_to_proxy(proxy_ip, terraform_data):
    """Отправка запросов к IP-адресу прокси-сервера nginx."""
    for i in range(NUM_REQUESTS):
        try:
            # Отправляем запрос на прокси-сервер
            response = requests.get(f"http://{proxy_ip}:{HOST_NGINX_PROXY_VM_PORT}")
            # Проверяем заголовки, которые могут содержать информацию о конечном сервере
            real_ip = response.headers.get('X-Upstream-Server', 'Неизвестно')

            # Найдем имя ВМ по реальному IP
            vm_name = find_vm_name_by_ip(real_ip.split(':')[0], terraform_data)

            # Выводим результат
            print(f"Запрос {i+1}: Перенаправлено на сервер с IP: {real_ip} (ВМ: {vm_name}). Статус: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при отправке запроса на прокси: {e}")


def main():
    # Укажите директорию с Terraform
    terraform_dir = '/home/sprint12_admin/sysadmin_sprint12/terraform_YP'

    # Получаем вывод terraform output
    data = get_terraform_output(terraform_dir)

    if data is None:
        return

    # Проверка наличия ключа vm_nat_ip и получение IP-адреса прокси
    if 'vm_nat_ip' in data and 'value' in data['vm_nat_ip']:
        vm_nat_ip_value = data['vm_nat_ip']['value']

        # Получаем IP-адрес хоста прокси-сервера (vm-2)
        proxy_ip = vm_nat_ip_value.get(HOST_NGINX_PROXY_VM_NAME)

        if proxy_ip:
            # Отправка HTTP-запросов к прокси-серверу (vm-2)
            send_request_to_proxy(proxy_ip, data)
        else:
            print(f"IP-адрес для {HOST_NGINX_PROXY_VM_NAME} не найден.")
    else:
        print("Ключ 'vm_nat_ip' отсутствует в выводе Terraform.")

if __name__ == '__main__':
    main()
