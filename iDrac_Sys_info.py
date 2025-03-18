import redfish
from prettytable import PrettyTable
import time
import os

# Lista de iDRACs para conectar (adicione mais conforme necessário)
idrac_list = [
    {"ip": "192.168.3.33", "user": "root", "password": "123"},
    {"ip": "192.168.3.254", "user": "root", "password": "123"},
    {"ip": "192.168.3.189", "user": "root", "password": "123"},
  ##  {"ip": "192.168.1.102", "user": "root", "password": "password3"},
]
# Create table

def clear_screen():
    # Verifica se o sistema operacional é Windows
    if os.name == 'nt':
        os.system('cls')  # Comando para limpar a tela no Windows
    else:
        os.system('clear')
    

table = PrettyTable()
table.field_names = ["iDRAC IP", "CPU Temps", "Fan Speeds", "Fan Health", "CPU Health", "RAM Health"]

# Loop infinito para monitoramento contínuo
while True:
    clear_screen()
    for idrac in idrac_list:
        ip = idrac["ip"]
        user = idrac["user"]
        password = idrac["password"]

        try:
            # Conectar ao iDRAC
            session = redfish.redfish_client(
                base_url=f"https://{ip}",
                username=user,
                password=password,
                default_prefix="/redfish/v1",
            )
            session.login()

            # Obter dados térmicos
            response = session.get("/redfish/v1/Chassis/System.Embedded.1/Thermal")
            thermal_data = response.dict

            # Separar sensores de CPU, FANs, e verificar status de saúde
            cpus = []
            fans = []
            fans_status = []
            cpus_health = []
            ram_health = []
            total_fan_speed = 0
            num_fans = 0

            # Processar dados de Temperaturas e CPUs
            if "Temperatures" in thermal_data:
                for sensor in thermal_data["Temperatures"]:
                    if sensor.get("PhysicalContext") == "CPU":
                        cpus.append(f"{sensor.get('Name')}: {sensor.get('ReadingCelsius')}°C")
                        cpu_health = sensor["Status"]["Health"]
                        if cpu_health != "OK":
                            cpus_health.append(f"❌ {sensor.get('Name')} - {cpu_health}")

            # Processar dados de Fans
            if "Fans" in thermal_data:
                for fan in thermal_data["Fans"]:
                    fan_status = fan["Status"]["Health"]
                    fans.append(f"{fan.get('Name')}: {fan.get('Reading')} {fan.get('ReadingUnits')}")
                    if fan_status != "OK":
                        fans_status.append(f"❌ {fan.get('Name')} - {fan_status}")
                    
                    # Somar a velocidade dos fãs
                    total_fan_speed += fan.get("Reading", 0)
                    num_fans += 1

            # Resumo da velocidade dos fãs
            if num_fans > 0:
                avg_fan_speed = int(total_fan_speed / num_fans)
                fan_summary = f"Avg Speed: {avg_fan_speed} RPM"
            else:
                fan_summary = "No fan data"

            # Verificar saúde da RAM
            ram_response = session.get("/redfish/v1/Systems/System.Embedded.1/Memory")
            ram_data = ram_response.dict
            ram_health_status = "OK"
            if "Members" in ram_data:
                for ram in ram_data["Members"]:
                    ram_status = ram.get("Status", {}).get("Health", "OK")
                    if ram_status != "OK":
                        ram_health.append(f"❌ {ram.get('Oem', {}).get('Dell', {}).get('Name', 'RAM')} - {ram_status}")
                    if ram_status != "OK":
                        ram_health_status = "❌ RAM Health Issue"
            
            # Formatar os dados para exibição na tabela
            cpu_temps = "\n".join(cpus) if cpus else "No data"
            fan_speeds = fan_summary if fans else "No data"
            fan_health = "\n".join(fans_status) if fans_status else "Fans Health ✅ OK"
            cpu_health = "\n".join(cpus_health) if cpus_health else "CPU Health ✅ OK"
            ram_health_status = "\n".join(ram_health) if ram_health else "RAM Health ✅ OK"

            # Adicionar uma linha para cada iDRAC
            table.add_row([ip, cpu_temps, fan_speeds, fan_health, cpu_health, ram_health_status])

            # Adicionar uma linha de separação entre as entradas dos iDRACs
            table.add_row(["-" * len(field) for field in table.field_names])

            # Logout da sessão Redfish
            session.logout()

        except Exception as e:
            table.add_row([ip, "Connection Error", "Connection Error", "Connection Error", "Connection Error", "Connection Error"])
            print(f"Error connecting to iDRAC {ip}: {e}")

    # Exibir a tabela final
    print(table)

    # Limpar a tabela para a próxima iteração
    table.clear_rows()

    # Esperar 60 segundos antes da próxima execução
    time.sleep(60)