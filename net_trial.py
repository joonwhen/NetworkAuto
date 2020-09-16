from netmiko import ConnectHandler
from threading import Thread
import mysql.connector as sql
import re

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

# Strip to IP Address
def obtain_ip(raw_ip):
    y = str(raw_ip)
    x = re.search("[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", y)
    return x.group()

# Strip Credentials Details
def params_strip(raw_data):
    y = str(raw_data)
    x = re.search('[A-Za-z0-9_]+', y)
    return x.group()

# Device Selection
def Device_Selection():
    print("Enter Hardware Name: ")
    chosen_device = input()
    db_selector = network_db.cursor()

    # Obtain IP Address
    db_selector.execute("SELECT IP_Address FROM port_ip WHERE Hardware_Name = '"+chosen_device+"' GROUP BY Hardware_Name")
    db_result = db_selector.fetchone() # .fetchall()
    address = obtain_ip(db_result)

    # Obtain Credentials to Login
    db_selector.execute("SELECT C.Device_Type FROM credentials as C JOIN port_ip as P WHERE C.Hardware_Name = P.Hardware_Name AND C.Port_No = P.Port_No AND P.IP_ADDRESS = '"+address+"'")
    db_result = db_selector.fetchall()
    connection_info = []
    connection_info.append(params_strip(db_result))

    db_selector.execute("SELECT C.Device_Password FROM credentials as C JOIN port_ip as P WHERE C.Hardware_Name = P.Hardware_Name AND C.Port_No = P.Port_No AND P.IP_ADDRESS = '"+address+"'")
    db_result = db_selector.fetchall()
    connection_info.append(params_strip(db_result))

    db_selector.execute("SELECT C.Secret FROM credentials as C JOIN port_ip as P WHERE C.Hardware_Name = P.Hardware_Name AND C.Port_No = P.Port_No AND P.IP_ADDRESS = '"+address+"'")
    db_result = db_selector.fetchall()
    connection_info.append(params_strip(db_result))

    device_config(address, connection_info)

# IP Selection
def IP_Selection():
    print("Enter IP Address: ")
    address = input()

    db_selector = network_db.cursor()
    # Obtain Credentials to Login
    db_selector.execute("SELECT C.Device_Type FROM credentials as C JOIN port_ip as P WHERE C.Hardware_Name = P.Hardware_Name AND C.Port_No = P.Port_No AND P.IP_ADDRESS = '"+address+"'")
    db_result = db_selector.fetchall()
    connection_info = []
    connection_info.append(params_strip(db_result))

    db_selector.execute("SELECT C.Device_Password FROM credentials as C JOIN port_ip as P WHERE C.Hardware_Name = P.Hardware_Name AND C.Port_No = P.Port_No AND P.IP_ADDRESS = '"+address+"'")
    db_result = db_selector.fetchall()
    connection_info.append(params_strip(db_result))

    db_selector.execute("SELECT C.Secret FROM credentials as C JOIN port_ip as P WHERE C.Hardware_Name = P.Hardware_Name AND C.Port_No = P.Port_No AND P.IP_ADDRESS = '"+address+"'")
    db_result = db_selector.fetchall()
    connection_info.append(params_strip(db_result))

    device_config(address, connection_info)

# Configuration
def device_config(IP_Address, connection_info):
    
    # Infornation Needed to Connect to Device
    # Improve on this to extract such information from SQL
    connection = {
        'device_type': connection_info[0],
        'host':   IP_Address,
        'password': connection_info[1],
        'secret': connection_info[2]
    }     
    print("Connecting to: " + IP_Address)
    net_connect = ConnectHandler(**connection)

    if(net_connect):
        net_connect.enable()
        print("Connected to " + IP_Address)
        while True:
            print("Enter Command: ")
            command = input()
            print("")
            if(command == 'x'):
                break
            else:
                output = net_connect.send_command_timing(
                    command_string=command,
                    strip_prompt=False,
                    strip_command=True
                )
                if "Delete filename" in output:
                    output += net_connect.send_command_timing(
                        command_string="\n",
                        strip_prompt=False,
                        strip_command=False
                    )
                if "confirm" in output:
                    output += net_connect.send_command_timing(
                        command_string="y",
                        strip_prompt=False,

                        strip_command=False
                    )
                print(output)
                
    else:
        print("Connection Failed")

# Initialisation    
user_input()