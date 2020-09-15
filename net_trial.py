from netmiko import ConnectHandler
from datetime import datetime
from threading import Thread
import mysql.connector as sql
import re
startTime = datetime.now()

# Establish Connection to MySQL Database 
network_db = sql.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "network"
)

# Prompting User Input / Main Menu
def user_input():
    print("Configure by: ")
    print("1. Device Name")
    print("2. IP Address")
    user_selection = input()

    if(user_selection == '1'):
        Device_Selection()
    if(user_selection == '2'):
        IP_Selection()

def obtain_ip(raw_ip):
    y = str(raw_ip)
    x = re.search("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", y)
    return x.group()

# Device Selection
def Device_Selection():
    print("Enter Hardware Name: ")
    Hardware_Name = input()
    db_selector = network_db.cursor()
    db_selector.execute("SELECT IP_Address FROM network_hardware WHERE Hardware_Name = Hardware_Name")
    db_result = db_selector.fetchone() # .fetchall()
    address = obtain_ip(db_result)
    device_config(address)

# IP Selection
def IP_Selection():
    print("Enter IP Address: ")
    IP_Address = input()
    device_config(IP_Address)

# Configuration
def device_config(IP_Address):

    connection = {
        'device_type': 'cisco_ios_telnet',
        'host':   IP_Address,
        'password': 'cisco',
        'secret': 'cisco'
    }         

    command = "show ip int brief"
    net_connect = ConnectHandler(**connection)

    output = net_connect.send_command(command)
    print(output)

# Initialisation    
user_input()