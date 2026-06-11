import os
import platform
import subprocess
import time

def ping_node(ip_address):
    """
    Pings a network node and returns its status and response time.
    """
    # Determine the correct ping flag based on the operating system
    # Codespaces runs on Linux, which uses '-c'
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    
    # Building the command (sending exactly 1 packet)
    command = ['ping', param, '1', ip_address]
    
    print(f"📡 Checking connectivity to {ip_address}...")
    start_time = time.time()
    
    # Execute the ping command in the background
    response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    end_time = time.time()
    
    # Calculate round-trip time in milliseconds
    latency = round((end_time - start_time) * 1000, 2)
    
    # If return code is 0, the ping was successful
    if response.returncode == 0:
        return "ONLINE", latency
    else:
        return "OFFLINE", None

if __name__ == "__main__":
    # Test destination: Google's Public DNS (Core Telecom Node)
    target_ip = "8.8.8.8"
    
    status, response_time = ping_node(target_ip)
    
    print("\n📊 --- NETWORK NODE STATUS ---")
    print(f"Target IP: {target_ip}")
    print(f"Status:    {'🟢 ' + status if status == 'ONLINE' else '🔴 ' + status}")
    if response_time:
        print(f"Latency:   {response_time} ms")
    print("-------------------------------\n")