# 🛡️ Self-Healing Cyber Defense Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-WebApp-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Security](https://img.shields.io/badge/Cybersecurity-Automation-red)

---

## 🚀 Overview

An autonomous cybersecurity system that detects threats, enriches them with threat intelligence, evaluates risk, and performs automated response and recovery in real time.

---

## 🏗️ Architecture Diagram

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

---
## Folder Structure
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
## ⚡ Features

* 🔍 Real-time attack detection
* 🧠 Threat intelligence integration
* ⚖️ Risk-based decision making
* ⚡ Automated response system
* ♻️ Self-healing mechanism
* 📊 Live monitoring dashboard

---

## 🖥️ Dashboard Preview

> Add your screenshot here

```id="img1"
![Dashboard](dash.png)
```

---

## ⚙️ Installation

```bash id="inst1"
git clone https://github.com/your-username/self_healing_cyber_platform.git
cd self_healing_cyber_platform
pip install -r requirements.txt
```

---

## 🔐 Setup Environment

```bash id="env1"
cp .env.example .env
```

Edit `.env`:

```id="env2"
ABUSIX_KEY=your_key
ABUSEIPDB_API_KEY=your_key
OTX_API_KEY=your_key
SLACK_WEBHOOK_URL=your_webhook
```

---

## ▶️ Run System

```bash id="run1"
./run_all.sh
```

🌐 Dashboard:

```id="run2"
http://127.0.0.1:5000
```

---

## 🧪 Attack Simulation

```bash id="atk1"
echo "Failed password for invalid user admin from 8.8.8.8" >> /tmp/test_auth.log
```

---

## 📂 Logs

* alerts.jsonl → detected threats
* alerts_enriched.jsonl → enriched intel
* actions.log → automated responses
* snapshots/ → forensic data

---

## 🔄 Workflow

```id="flow1"
Detect → Enrich → Decide → Respond → Heal
```

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

## 🔐 Security

* No secrets stored in repo
* `.env` excluded
* `.env.example` provided

---

## 🧠 Tech Stack

* Python
* Flask
* Scapy
* REST APIs
* JSON Logging

---

## 🎯 Goal

To build a fully automated, intelligent cybersecurity defense system capable of real-time detection and response.

---

## 👨‍💻 Author

**Mamon**
