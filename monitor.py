import json
import os
import platform
import subprocess
import time

def ping_node(ip_address):
    """
    Pings a network node and returns its status and response time.
    """
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', ip_address]
    
    start_time = time.time()
    response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    end_time = time.time()
    
    latency = round((end_time - start_time) * 1000, 2)
    
    if response.returncode == 0:
        return "ONLINE", latency
    else:
        return "OFFLINE", None

def run_network_audit():
    # 1. Load targets from the JSON configuration file
    try:
        with open('nodes.json', 'r') as file:
            nodes = json.load(file)
    except FileNotFoundError:
        print("❌ Error: nodes.json configuration file not found!")
        return

    print("==================================================")
    print(f"📡 STARTING TELECOM NETWORK STATUS AUDIT")
    print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("==================================================")

    online_count = 0
    total_nodes = len(nodes)

    # 2. Loop through each node dynamically
    for node in nodes:
        print(f"Checking: {node['name']} [{node['ip']}] ({node['type']})...")
        status, latency = ping_node(node['ip'])
        
        if status == "ONLINE":
            online_count += 1
            print(f"  └─ Status: 🟢 ONLINE | Latency: {latency} ms\n")
        else:
            print(f"  └─ Status: 🔴 OFFLINE | Target Unreachable\n")

    # 3. Print overall health summaries
    print("==================================================")
    print(f"📊 AUDIT COMPLETE SUMMARY")
    print(f"Total Nodes Monitored: {total_nodes}")
    print(f"Network Availability:  {online_count}/{total_nodes} Nodes Operational")
    print("==================================================\n")

if __name__ == "__main__":
    run_network_audit()