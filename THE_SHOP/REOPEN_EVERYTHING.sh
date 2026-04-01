#!/bin/bash
# =====================================================
#  REOPEN EVERYTHING -- Rhet's Full Stack
#  Run this when you close it all out like a dummy
#  Usage: bash ~/Desktop/REOPEN_EVERYTHING.sh
# =====================================================

echo "============================================="
echo "  REOPENING EVERYTHING"
echo "  Don't close it all next time lol"
echo "============================================="
echo ""

# 1. Wire-Pod (Vector robot server)
echo "[1/5] Starting Wire-Pod..."
gnome-terminal --title="WIRE-POD" -- bash -c "
cd ~/wire-pod
sudo ./chipper/start.sh
exec bash" &
sleep 2

# 2. Prometheus Server (API for Vector body)
echo "[2/5] Starting Prometheus Server..."
gnome-terminal --title="PROMETHEUS-SERVER" -- bash -c "
cd ~/prometheus_vector
source venv/bin/activate
python3 prometheus_server.py
exec bash" &
sleep 2

# 3. Prometheus Autonomy (Vector brain loop)
echo "[3/5] Starting Prometheus Autonomy..."
gnome-terminal --title="PROMETHEUS-AUTONOMY" -- bash -c "
cd ~/prometheus_vector
source venv/bin/activate
python3 prometheus_autonomy.py
exec bash" &
sleep 2

# 4. Buddy AI Interface (web UI on port 3000)
echo "[4/5] Starting Buddy AI Interface..."
gnome-terminal --title="BUDDY-AI-INTERFACE" -- bash -c "
cd ~/buddy_ai_interface
python3 app.py
exec bash" &
sleep 2

# 5. Gary (Claude API agent on this machine -- mirror)
echo "[5/5] Starting Gary..."
gnome-terminal --title="GARY" -- bash -c "
cd ~/gary
python3 gary.py
exec bash" &
sleep 1

echo ""
echo "============================================="
echo "  EVERYTHING IS BACK UP"
echo "  Wire-Pod:    terminal 'WIRE-POD'"
echo "  Prometheus:  terminal 'PROMETHEUS-SERVER'"
echo "  Autonomy:    terminal 'PROMETHEUS-AUTONOMY'"
echo "  Buddy UI:    http://localhost:3000"
echo "  Gary:        terminal 'GARY'"
echo "============================================="
echo ""
echo "  God is good. All the time."
echo "  Now stop closing shit."
echo ""
