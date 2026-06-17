import concurrent.futures
import json
import os
import platform
import subprocess
import time

def ping_node(node):
    """
    Pings a single network node. 
    Accepts a node dictionary and returns the updated dictionary with status and latency.
    """
    ip_address = node['ip']
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', ip_address]
    
    start_time = time.time()
    response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    end_time = time.time()
    
    latency = round((end_time - start_time) * 1000, 2)
    
    # Pack results directly into a result dictionary
    if response.returncode == 0:
        return {**node, "status": "ONLINE", "latency": latency}
    else:
        return {**node, "status": "OFFLINE", "latency": None}

def run_network_audit():
    # 1. Load data targets out of the JSON configuration file
    try:
        with open('nodes.json', 'r') as file:
            nodes = json.load(file)
    except FileNotFoundError:
        print("❌ Error: nodes.json configuration file not found!")
        return
    except json.JSONDecodeError:
        print("❌ Error: nodes.json contains invalid formatting structure!")
        return

    # 2. Automated Log Directory Setup
    os.makedirs('logs', exist_ok=True)
    current_date = time.strftime('%Y-%m-%d')
    log_filename = f"logs/network_log_{current_date}.txt"
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    header_lines = [
        "\n==================================================",
        f"📡 STARTING MULTI-THREADED TELECOM NETWORK AUDIT",
        f"⏰ Timestamp: {timestamp}",
        "=================================================="
    ]
    
    for line in header_lines:
        print(line)
        
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write("\n".join(header_lines) + "\n")

        # 3. ✨ DAY 5 MULTI-THREADING ENGINE ✨
        # Spawns background workers to ping all targets simultaneously
        audited_nodes = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Map the ping function across all nodes in parallel
            results = executor.map(ping_node, nodes)
            for result in results:
                audited_nodes.append(result)

        # 4. Process and Log Parallel Results
        online_count = 0
        total_nodes = len(audited_nodes)

        for node in audited_nodes:
            if node['status'] == "ONLINE":
                online_count += 1
                log_entry = f"Checking: {node['name']} [{node['ip']}] ({node['type']})...\n  └─ Status: 🟢 ONLINE | Latency: {node['latency']} ms\n"
            else:
                log_entry = f"Checking: {node['name']} [{node['ip']}] ({node['type']})...\n  └─ Status: 🔴 OFFLINE | Target Unreachable\n"
            
            print(log_entry, end="")
            log_file.write(log_entry)

        summary_lines = [
            "==================================================",
            f"📊 AUDIT COMPLETE SUMMARY",
            f"Total Nodes Monitored: {total_nodes}",
            f"Network Availability:  {online_count}/{total_nodes} Nodes Operational",
            "=================================================="
        ]
        
        for line in summary_lines:
            print(line)
            log_file.write(line + "\n")

if __name__ == "__main__":
    # 5. ✨ DAY 5 INFINITE MONITORING LOOP ✨
    print("🚀 Telecom Monitor Activated. Running in background mode...")
    print("💡 Press Ctrl + C to stop the monitor gracefully at any time.\n")
    
    INTERVAL_SECONDS = 60 # Run the audit every 60 seconds
    
    try:
        while True:
            run_network_audit()
            print(f"\n💤 Sleeping for {INTERVAL_SECONDS} seconds... Next audit incoming.")
            time.sleep(INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        # Catch Ctrl + C gracefully
        print("\n🛑 Shutdown command received! Safely closing background threads and exiting. Goodbye!")