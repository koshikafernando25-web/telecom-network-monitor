import concurrent.futures
import json

import platform
import subprocess
import time

def ping_node(node):
    """
    Pings a single network node. 
    Returns updated dictionary with status, latency, and performance evaluation.
    """
    ip_address = node['ip']
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', ip_address]
    
    start_time = time.time()
    response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    end_time = time.time()
    
    latency = round((end_time - start_time) * 1000, 2)
    
    if response.returncode == 0:
        # Latency Threshold Assessment Logic
        if latency < 50:
            quality = "EXCELLENT"
            icon = "🟢"
        elif latency <= 150:
            quality = "AVERAGE"
            icon = "🟡"
        else:
            quality = "HIGH LATENCY ALERT"
            icon = "⚠️"
            
        return {**node, "status": "ONLINE", "latency": latency, "quality": quality, "icon": icon}
    else:
        return {**node, "status": "OFFLINE", "latency": None, "quality": "CRITICAL DOWN", "icon": "🔴"}

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
        "\n==================================================================",
        f"📡 STARTING DAY 6 ANALYTICS & INTELLIGENT NETWORK AUDIT",
        f"⏰ Audit Timestamp: {timestamp}",
        "=================================================================="
    ]
    
    for line in header_lines:
        print(line)
        
    with open(log_filename, 'a', encoding='utf-8') as log_file:
        log_file.write("\n".join(header_lines) + "\n")

        # 3. Parallel Execution Multi-Threading
        audited_nodes = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(ping_node, nodes)
            for result in results:
                audited_nodes.append(result)

        # 4. Process, Analyze, and Flag Results
        online_count = 0
        total_nodes = len(audited_nodes)
        alert_count = 0

        for node in audited_nodes:
            if node['status'] == "ONLINE":
                online_count += 1
                log_entry = (
                    f"Checking: {node['name']} [{node['ip']}] ({node['type']})...\n"
                    f"  └─ Status: {node['icon']} {node['status']} | Latency: {node['latency']} ms [{node['quality']}]\n"
                )
                # If it's a high latency warning, track it as an alert anomaly
                if node['quality'] == "HIGH LATENCY ALERT":
                    alert_count += 1
                    log_entry += f"  ⚠️  [PERFORMANCE ALERT] Target routing delay exceeds standard operational thresholds.\n"
            else:
                alert_count += 1
                log_entry = (
                    f"Checking: {node['name']} [{node['ip']}] ({node['type']})...\n"
                    f"  └─ Status: {node['icon']} {node['status']} | Target Unreachable [{node['quality']}]\n"
                    f"  🚨 [CRITICAL ALERT] Immediate network verification required for this route!\n"
                )
            
            print(log_entry, end="")
            log_file.write(log_entry)

        # Calculate Availability Percentage
        availability_rate = round((online_count / total_nodes) * 100, 2)

        summary_lines = [
            "==================================================================",
            f"📊 INTELLIGENT AUDIT COMPLETE SUMMARY",
            f"Total Nodes Monitored : {total_nodes}",
            f"Network Availability  : {online_count}/{total_nodes} Operational ({availability_rate}%)",
            f"Active Status Anomalies: {alert_count} Alerts Flagged",
            "=================================================================="
        ]
        
        for line in summary_lines:
            print(line)
            log_file.write(line + "\n")

if __name__ == "__main__":
    # Runs once dynamically on-demand, logs data permanently, then shuts down cleanly.
    run_network_audit()