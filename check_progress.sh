#!/bin/bash
# Check progress of overnight run

echo "📊 OVERNIGHT RUN PROGRESS"
echo "========================="
echo ""

# Check if running
if pgrep -f "baseline_all_models.py" > /dev/null; then
    echo "✅ Script is RUNNING"
    echo ""
else
    echo "⏹️  Script is NOT running (finished or not started)"
    echo ""
fi

# Show last 30 lines of log
if [ -f testing/overnight_run.log ]; then
    echo "Last 30 lines of log:"
    echo "---"
    tail -30 testing/overnight_run.log
else
    echo "❌ Log file not found yet"
fi

echo ""
echo "To see full log: tail -f testing/overnight_run.log"
echo "To check cloud status: sb-cli list-runs swe-bench_lite test"
