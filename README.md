# 🛡️ Self-Healing Cyber Defense Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-WebApp-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Security](https://img.shields.io/badge/Cybersecurity-Automation-red)
![Platform](https://img.shields.io/badge/Platform-Linux-black)
![OS](https://img.shields.io/badge/Tested%20on-Kali%20Linux-informational)
![API](https://img.shields.io/badge/API-REST-blueviolet)
![Monitoring](https://img.shields.io/badge/Monitoring-Prometheus-orange)
![Logs](https://img.shields.io/badge/Logs-JSONL-lightgrey)
![Threat-Intel](https://img.shields.io/badge/Threat%20Intel-AbuseIPDB%20%7C%20OTX-blue)
![Automation](https://img.shields.io/badge/Automation-Self--Healing-critical)
![Firewall](https://img.shields.io/badge/Firewall-nftables-important)
![Dashboard](https://img.shields.io/badge/Dashboard-Flask%20UI-success)
![Project](https://img.shields.io/badge/Project-Type%20Cybersecurity-blue)
![Maintained](https://img.shields.io/badge/Maintained-Yes-brightgreen)
![Open%20Source](https://img.shields.io/badge/Open%20Source-Yes-success)
![PRs](https://img.shields.io/badge/PRs-Welcome-blue)
![GitHub repo size](https://img.shields.io/github/repo-size/mamon404/Self_Healing_Cyber_Defense_Platform)
![GitHub stars](https://img.shields.io/github/stars/mamon404/Self_Healing_Cyber_Defense_Platform)
![GitHub forks](https://img.shields.io/github/forks/mamon404/Self_Healing_Cyber_Defense_Platform)
![GitHub issues](https://img.shields.io/github/issues/mamon404/Self_Healing_Cyber_Defense_Platform)

---

# 🚀 Overview

An autonomous cybersecurity system designed to continuously monitor, detect, and respond to security threats in real time by integrating multiple layers of intelligence and automation. It not only identifies suspicious activities from system logs and network traffic but also enriches these events using external threat intelligence sources to provide deeper context such as reputation, origin, and historical behavior. The platform evaluates each detected threat through a risk-based decision engine that applies predefined policies and dynamic scoring to determine the severity and appropriate course of action. Based on this evaluation, it automatically executes response mechanisms including blocking malicious IP addresses, notifying administrators, collecting forensic snapshots, and initiating recovery processes to maintain system stability. By combining detection, enrichment, decision-making, and automated response into a unified workflow, the system demonstrates a proactive and self-healing approach to modern cybersecurity challenges.

---
# ⚡ Features

- Real-time log-based attack detection (e.g., SSH brute-force)
- Network monitoring using packet sniffer
- Threat intelligence enrichment (AbuseIPDB, OTX, ThreatMiner)
- Risk-based decision engine for threat evaluation
- Automated response actions (block IP, notify admin, restart service)
- System snapshot collection for forensic analysis
- Self-healing mechanism to maintain system stability
- Centralized logging across detection, enrichment, and response
- REST API for orchestration and automation
- Live monitoring dashboard with metrics visualization

---
# 🏗️ Architecture Diagram

```id="arch1"
                +----------------------+
                |   Log / Network Data |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |      Detection       |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |     Enrichment       |
                | (Threat Intelligence)|
                +----------+-----------+
                           |
                           v
                +----------------------+
                |   Decision Engine    |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |   Response System    |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |    Self-Healing      |
                +----------------------+
```
<img width="853" height="1280" alt="Workflow 1" src="https://github.com/user-attachments/assets/06e43d20-d02a-4241-8b6b-877f0897f9e7" />

# 💻 Tech Stack
```
Python
Flask
Scapy
Requests
JSON
Linux (Kali)
Prometheus (Metrics Format)
cURL
jq
```
---
# Folder Structure
```
self_healing_cyber_platform/
│
├── monitoring/            # Packet sniffer + metrics exporter
├── detection/             # Signature & anomaly detection engines
├── intel/                 # Threat intelligence (AbuseIPDB, OTX, ThreatMiner)
├── orchestrator/          # Decision engine + API
├── response/              # Response actions (block IP, notify, snapshot)
├── healing/               # Self-healing logic
├── dashboard/             # Flask web dashboard UI
├── config/                # Configuration files
├── logs/                  # Runtime logs
│   ├── alerts.jsonl
│   ├── alerts_enriched.jsonl
│   ├── actions.log
|   ├── detection.log
│   └── snapshots/
│
├── main.sh                # Start all services
├── requirements.txt       # Dependencies
├── README.md              # Documentation
├── .env                   # Environment template

```




## ⚙️ Installation

```bash id="inst1"

https://github.com/mamon404/Self_Healing_Cyber_Defense_Platform.git
cd self_healing_cyber_platform

```
## Create Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
```
## Install Dependencies 

```
pip install -r requirements.txt
```

## 🔐 Setup Environment

```bash id="env1"
nano .env
```

Edit `.env`:

```id="env2"
ABUSIX_KEY=your_key
ABUSEIPDB_API_KEY=your_key
OTX_API_KEY=your_key
SLACK_WEBHOOK_URL=your_webhook
```

---

#  Permission 

```bash id="run1"
chmod +x main.sh
./main.sh
```
<img width="1879" height="937" alt="Terminal" src="https://github.com/user-attachments/assets/9230fc2b-6d98-43c5-b3eb-e99b4afd4760" />

---

# 🧪 Attack Simulation

## ⚠️ Educational Purpose Only
This project is developed strictly for educational and research purposes.
All attack simulations are performed in a controlled environment and should not be used on real systems without proper authorization.

### Inject another terminal 
```
for ip in 45.33.32.156 103.21.244.0 185.220.101.1 91.121.83.118 8.8.8.8; do
  for i in {1..3}; do
    echo "Failed password for invalid user admin from $ip" >> /tmp/test_auth.log
  done
done

```
### 📊 Results After Attack( Output )

After executing the simulated brute-force attack, the system processes the event through all phases and produces the following outputs:

---

### 🔍 Detection Output (`alerts.jsonl`)

- 📄 View full file: [Alerts ](logs/alerts.jsonl)
- 📄 View Detection file: [Detection](logs/detection.log)

The `alerts.jsonl` file contains the raw detection output generated by the system in real time.  
It records security events identified by the detection engine based on predefined rules.

When suspicious activity such as repeated failed SSH login attempts is observed, the system automatically creates structured alert entries. Each alert includes key information such as:

- Rule ID (type of attack detected)  
- Description of the threat  
- Severity level (e.g., high, medium, low)  
- Source IP address  
- Timestamp of the event  

This file represents the **first stage of the pipeline**, where raw logs are transformed into meaningful security alerts.  
It serves as the input for further processing, including threat intelligence enrichment and automated response.

---
<img width="1920" height="1080" alt="alert" src="https://github.com/user-attachments/assets/078c9703-3330-4ea6-884e-b6f99998a3fe" />

---

### 🌐 Threat Intelligence Enrichment (`alerts_enriched.jsonl`)
📄 View full file: [Alerts_enriched](logs/alerts_enriched.jsonl)

The `alerts_enriched.jsonl` file contains the enriched version of detected alerts, where additional threat intelligence data is appended to each event.

After an alert is generated by the detection engine, it is passed to the enrichment module, which queries external threat intelligence sources such as AbuseIPDB and AlienVault OTX.

This process enhances the original alert by adding contextual information about the source IP, including:

- IP reputation score  
- ISP (Internet Service Provider)  
- Geolocation (country, region)  
- Usage type (e.g., hosting, CDN, residential)  
- Historical abuse reports  
- Threat validation indicators  

The enriched output combines both the original alert data and the intelligence data into a structured format.  
This allows the decision engine to make more accurate and informed security decisions.

This file represents the **intelligence layer of the system**, bridging raw detection and automated response.

---
<img width="1919" height="1003" alt="alerts_enriched" src="https://github.com/user-attachments/assets/595a5b73-f70b-4469-8ec8-fb8047854b5e" />

---

### ⚡ Automated Response (`actions.log`)
📄 View full file: [Actions](logs/actions.log)


The `actions.log` file records all decisions and automated responses executed by the system after a threat is detected and analyzed.

Once an alert is enriched with threat intelligence, it is passed to the decision engine, which evaluates the risk level based on severity and contextual data.  
If the threat is classified as high risk, the system automatically triggers predefined response actions.

Each entry in this file contains detailed information about:
- Decision ID (unique identifier for each event)  
- Evaluated risk score and risk level  
- Trigger conditions and decision policy  
- Actions executed by the system  
- Parameters used for each action  
- Execution results and status (success / failure / dry-run)  

Typical automated actions include:
- Blocking the malicious IP address (using firewall rules)  
- Collecting a system snapshot for forensic analysis  
- Sending notification alerts to the administrator  
- Restarting affected services to maintain system stability  

This file represents the **core response and self-healing layer** of the system, where intelligent decisions are translated into real-time actions.

It also provides full traceability, allowing administrators to audit how each threat was handled by the system.

<img width="1919" height="1003" alt="actions" src="https://github.com/user-attachments/assets/7b63a9a1-1f8d-4523-9546-72199b7f4114" />

---
# 🖥️ Dashboard Preview

The dashboard provides detailed system information including CPU usage, memory status, hostname, IP address, MAC address, operating system details, and total memory usage. It also displays real-time system performance metrics and includes an automated feature that restarts the system every 5 seconds for continuous monitoring and recovery.

<img width="1718" height="938" alt="dashboard" src="https://github.com/user-attachments/assets/1e247d66-f445-4230-84db-3a4cde188b7b" />

---

# 📌 Workflow Overview

```text
Log Injection → Detection Engine → Alert Generation
→ Threat Intelligence Enrichment → Risk Evaluation
→ Decision Engine → Automated Actions
→ Self-Healing & Recovery → Dashboard Visualization
```

---

## 🔍 Step-by-Step Flow

#### 1. Log Generation / Attack Injection

* Suspicious activity (e.g., brute-force attack) is written to system logs
* Example: failed SSH login attempts

---

#### 2. Detection Engine

* Scans logs in real time
* Matches attack patterns using predefined rules
* Generates alerts in `logs/alerts.jsonl`

---

#### 3. Threat Intelligence Enrichment

* Extracts source IP from alert
* Queries external APIs (AbuseIPDB, OTX)
* Adds reputation, ISP, and geo data
* Output stored in `logs/alerts_enriched.jsonl`

---

#### 4. Risk Evaluation (Decision Engine)

* Calculates risk score based on severity and threat data
* Classifies attack (LOW / MEDIUM / HIGH)
* Determines response policy

---

#### 5. Automated Response

* Executes predefined actions:

  * Block IP (nftables)
  * Collect system snapshot
  * Notify administrator
  * Restart affected service

---

#### 6. Self-Healing & Recovery

* Automatically mitigates the threat
* Restores system stability
* Ensures continuous availability

---

#### 7. Monitoring & Dashboard

* Displays system metrics (CPU, memory, network)
* Shows real-time system status
* Accessible via web dashboard

###

---

## 🔥 Example Response

* Threat detected
* Risk = HIGH
* Automated actions:

  * block_ip
  * collect_snapshot
  * notify_admin
  * restart_service

---
## 🌐 API Endpoints Overview

The platform exposes a set of robust and well-structured RESTful API endpoints through the Orchestrator service, enabling seamless interaction between different components of the system. These endpoints allow external systems, administrators, and automated processes to monitor system health, submit security alerts, and retrieve real-time performance metrics. Designed with scalability and reliability in mind, the API layer plays a critical role in ensuring efficient communication across the detection, intelligence, decision-making, and response modules.

### GET /health

This endpoint is used to verify the operational status of the API service. It provides a quick and lightweight way to check whether the system is running correctly and is ready to accept requests. This is particularly useful for monitoring tools and automated health checks.

### POST /run

This endpoint accepts incoming security alerts and processes them through the decision engine. Based on the severity and contextual intelligence of the alert, the system evaluates the risk level and triggers appropriate automated response actions such as blocking malicious IPs, collecting system snapshots, notifying administrators, and initiating recovery procedures.

### GET /metrics

This endpoint provides detailed system monitoring data in Prometheus-compatible format. It includes key performance indicators such as CPU usage, memory consumption, and network statistics, enabling real-time observability and integration with monitoring dashboards.

---

## 🎯 Use Case

This system is designed to proactively detect, analyze, and respond to critical real-world cybersecurity threats with high accuracy and automation, including:

* SSH brute-force attacks targeting system access
* Malicious or suspicious IP activity identified through threat intelligence
* Unauthorized access attempts and privilege escalation attempts
* Fully automated threat detection, decision-making, and response workflows

---

## 🚀 Future Improvements

* Implement advanced machine learning and AI-driven anomaly detection for proactive threat identification
* Integrate with real firewall systems to enable live blocking and eliminate dry_run limitations
* Containerize the entire platform using Docker for scalable and portable deployment
* Deploy the system on cloud platforms (AWS, GCP, Azure) for high availability and scalability
* Enhance the dashboard with real-time analytics, visual insights, and interactive monitoring features
* Integrate with enterprise SIEM solutions for centralized logging, correlation, and incident management

---


## 🤝 Contributing

We strongly encourage contributions from the community to enhance and expand this project.

If you would like to contribute:

* Fork the repository to your GitHub account
* Create a new feature or fix branch
* Implement your changes with clear and clean code
* Commit your changes with meaningful messages
* Submit a pull request for review

All contributions, whether small improvements or major features, are highly appreciated and help make this project better.


## 🏁 Conclusion

The **Self-Healing Cyber Defense Platform** successfully demonstrates a complete end-to-end cybersecurity pipeline that integrates detection, threat intelligence, decision-making, and automated response into a unified system.

By continuously monitoring system logs and network activity, the platform is capable of identifying suspicious behavior in real time. It enhances these detections using external threat intelligence sources, enabling deeper context and more accurate risk assessment. The decision engine then evaluates each threat and automatically executes appropriate response actions without requiring manual intervention.

Through its self-healing capabilities, the system not only mitigates threats but also ensures system stability and service availability by performing recovery actions such as restarting services and maintaining operational continuity.

This project highlights the potential of automation in modern cybersecurity, showcasing how intelligent systems can reduce response time, minimize human effort, and improve overall security posture. It serves as a strong foundation for building advanced, scalable, and intelligent cyber defense solutions.


# 👨‍💻 Author

# **Mamon**
---
---
---

---
