#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
MVP_DIR="$ROOT_DIR/validation-tests/mvp-demo"
LOOP_DIR="$MVP_DIR/feature-loop"
QUEUE_DIR="$ROOT_DIR/validation-tests/policy-gate-fixtures/t2_human_queue"
RESULTS_DIR="$MVP_DIR/results"

mkdir -p "$RESULTS_DIR"
rm -f "$RESULTS_DIR"/*.log "$RESULTS_DIR"/*.json 2>/dev/null || true

echo "MVP Demo Run"
echo "============"
echo "Repo: $ROOT_DIR"

reset_loop() {
  cp "$LOOP_DIR/workflow.seed.json" "$LOOP_DIR/workflow.json"
  cp "$LOOP_DIR/context.seed.json" "$LOOP_DIR/context.json"
  find "$LOOP_DIR/review" -type f -name '*.json' -delete || true
  find "$LOOP_DIR/spec" -type f ! -name '.gitkeep' -delete || true
  find "$LOOP_DIR/design" -type f ! -name '.gitkeep' -delete || true
  find "$LOOP_DIR/implementation" -type f ! -name '.gitkeep' -delete || true
}

reset_queue() {
  cp "$QUEUE_DIR/workflow.seed.json" "$QUEUE_DIR/workflow.json"
  cp "$QUEUE_DIR/context.seed.json" "$QUEUE_DIR/context.json"
  find "$QUEUE_DIR/review" -type f -name '*.json' -delete || true
}

echo ""
echo ">>> Scenario 1: multi-agent + handovers + review loop"
reset_loop
python3 "$ROOT_DIR/orchestrator/main.py" "$LOOP_DIR" --mode=autonomous | tee "$RESULTS_DIR/mvp_loop.log"

echo ""
echo ">>> Scenario 2: human queue path"
reset_queue
python3 "$ROOT_DIR/orchestrator/main.py" "$QUEUE_DIR" --mode=autonomous | tee "$RESULTS_DIR/mvp_queue.log"

QUEUE_ID="$(python3 "$ROOT_DIR/orchestrator/human_queue.py" "$QUEUE_DIR" list --status PENDING | python3 -c 'import sys, json; print(json.loads(sys.stdin.readline())["queue_id"])')"
python3 "$ROOT_DIR/orchestrator/human_queue.py" "$QUEUE_DIR" ack --queue-id "$QUEUE_ID" --reviewer "principal"
python3 "$ROOT_DIR/orchestrator/human_queue.py" "$QUEUE_DIR" resolve --queue-id "$QUEUE_ID" --decision GO --reviewer "principal" --summary "Approved in MVP demo"
python3 "$ROOT_DIR/orchestrator/main.py" "$QUEUE_DIR" --mode=autonomous >> "$RESULTS_DIR/mvp_queue.log"

echo ""
echo ">>> Metrics summary"
python3 "$ROOT_DIR/orchestrator/audit_metrics.py" "$ROOT_DIR/validation-tests" --output "$RESULTS_DIR/mvp_metrics.json" | tee "$RESULTS_DIR/mvp_metrics_stdout.json"

echo ""
echo "Done."
echo "- Loop log:   $RESULTS_DIR/mvp_loop.log"
echo "- Queue log:  $RESULTS_DIR/mvp_queue.log"
echo "- Metrics:    $RESULTS_DIR/mvp_metrics.json"
