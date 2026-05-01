#!/bin/bash

# Colors
GREEN="\033[1;32m"
CYAN="\033[1;36m"
YELLOW="\033[1;33m"
RESET="\033[0m"

clear

# BIG TITLE (clean + bold)
echo -e "${CYAN}"
figlet -f slant -w $(tput cols) "SELF HEALING CYBER DEFENSE PLATFORM"
echo -e "${RESET}"

# Name section
echo -e "${GREEN}               Developed by Mamon${RESET}"
echo ""

# Divider
echo -e "${CYAN}====================================================${RESET}"

# Loading animation
loading() {
    echo -ne "${YELLOW}$1${RESET}"
    for i in {1..3}; do
        echo -ne "."
        sleep 0.25
    done
    echo ""
}

echo ""
echo -e "${CYAN}[+] Booting Cyber Defense System...${RESET}"

# Activate venv
loading "[+] Activating virtual environment"
source ~/venv/bin/activate

# Prepare logs
loading "[+] Preparing log environment"
mkdir -p logs
# --- CLEAN OLD LOGS FIRST ---
rm -f /tmp/test_auth.log
rm -f logs/alerts.jsonl
rm -f logs/alerts_enriched.jsonl
rm -f logs/actions.log
rm -f logs/detection.log
touch /tmp/test_auth.log logs/alerts.jsonl logs/alerts_enriched.jsonl logs/actions.log logs/detection.log
> /tmp/test_auth.log
> logs/alerts.jsonl
> logs/alerts_enriched.jsonl
> logs/actions.log
> detection.log
# Start service function
start_service() {
    loading "$1"
    shift
    "$@" > /dev/null 2>&1 &
    sleep 0.6
}

# Start services (clean mode)
start_service "[+] Metrics Exporter" python3 -m monitoring.metrics_exporter
start_service "[+] Detection Engine" python3 -m detection.run_signature_scanner
start_service "[+] Threat Intelligence" python3 -m intel.enrich_runner
start_service "[+] Orchestrator API" python3 -m orchestrator.api
start_service "[+] Dashboard UI" python3 dashboard/app.py

# Packet sniffer
echo -e "${CYAN}[!] Starting Packet Sniffer (root required)${RESET}"
sudo ~/venv/bin/python3 -m monitoring.packet_sniffer > /dev/null 2>&1 &

echo ""
echo -e "${GREEN}====================================================${RESET}"
echo -e "${GREEN}        ✔ SYSTEM FULLY OPERATIONAL ✔${RESET}"
echo -e "${GREEN}====================================================${RESET}"

echo ""
echo -e "${CYAN}[🌐] Dashboard → http://127.0.0.1:5000${RESET}"
echo -e "${CYAN}[⚡] Mode → Autonomous / Self-Healing${RESET}"
echo -e "${CYAN}[!] Press CTRL+C to shutdown system${RESET}"

# Cleanup
trap "echo -e '\n${YELLOW}[!] Shutting down system...${RESET}'; pkill -f monitoring; pkill -f detection; pkill -f intel; pkill -f orchestrator; pkill -f dashboard; exit" SIGINT

wait
