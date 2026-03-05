#!/bin/bash
# NeuroLens - Stop All Services
# Bash script for Linux/Mac
# Usage: ./stop_all_services.sh

echo "================================================"
echo "  NeuroLens - Stopping All Services"
echo "================================================"
echo ""

if [ ! -f .pids ]; then
    echo "No PID file found. Services may not be running or weren't started with start_all_services.sh"
    echo "You can manually find and kill processes on ports:"
    echo "  lsof -ti:8000,8001,8002,8003,5173 | xargs kill -9"
    exit 1
fi

# Read PIDs from file
PIDS=$(cat .pids)

echo "Stopping services..."
for PID in $PIDS; do
    if kill -0 $PID 2>/dev/null; then
        echo "  Stopping process $PID..."
        kill $PID
    else
        echo "  Process $PID not running"
    fi
done

# Wait a moment
sleep 2

# Force kill if still running
for PID in $PIDS; do
    if kill -0 $PID 2>/dev/null; then
        echo "  Force stopping process $PID..."
        kill -9 $PID
    fi
done

# Clean up
rm -f .pids

echo ""
echo "All services stopped!"
echo ""
