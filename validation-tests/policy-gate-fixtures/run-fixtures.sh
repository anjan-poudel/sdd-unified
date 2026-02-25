#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
FIXTURE_ROOT="$ROOT_DIR/validation-tests/policy-gate-fixtures"
RESULTS_DIR="$FIXTURE_ROOT/results"

echo "Policy Gate Fixture Run"
echo "======================="
echo "Repo: $ROOT_DIR"

rm -rf "$RESULTS_DIR"
mkdir -p "$RESULTS_DIR"

run_fixture() {
  local name="$1"
  local feature="$FIXTURE_ROOT/$name"
  local review="$feature/review"

  echo ""
  echo ">>> Running fixture: $name"

  cp "$feature/workflow.seed.json" "$feature/workflow.json"
  cp "$feature/context.seed.json" "$feature/context.json"

  # Reset runtime review outputs to deterministic baseline.
  find "$review" -type f -name '*.json' -delete || true
  if [ -d "$feature/review_seed" ]; then
    cp "$feature"/review_seed/*.json "$review"/ 2>/dev/null || true
  fi

  python3 "$ROOT_DIR/orchestrator/main.py" "$feature" --mode=autonomous | tee "$RESULTS_DIR/${name}.log"
}

run_fixture "t0_auto_approve"
run_fixture "t1_auto_review"
run_fixture "t2_human_queue"

echo ""
echo ">>> Computing audit metrics"
python3 "$ROOT_DIR/orchestrator/audit_metrics.py" "$FIXTURE_ROOT" \
  --output "$RESULTS_DIR/audit_metrics.json" | tee "$RESULTS_DIR/audit_metrics_stdout.json"

echo ""
echo "Done. Results:"
echo "- $RESULTS_DIR"
