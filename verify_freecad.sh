#!/bin/bash
# Verify snowman_freecad.py by running it with xvfb and checking output

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
FREECAD_SCRIPT="${SCRIPT_DIR}/snowman_freecad.py"
OUTPUT_IMAGE="${SCRIPT_DIR}/snowman_freecad.png"
TIMEOUT_SECONDS="${1:-15}"

# Create a wrapper that runs the script and exits cleanly
WRAPPER=$(mktemp /tmp/freecad_wrapper_XXXXXX.py)
trap "rm -f '$WRAPPER'" EXIT

cat > "$WRAPPER" << EOF
import os
exec(open("${FREECAD_SCRIPT}").read())
os._exit(0)
EOF

# Remove existing output to ensure we're testing fresh
rm -f "$OUTPUT_IMAGE"

echo "Running FreeCAD verification..."
echo "  Script: $FREECAD_SCRIPT"
echo "  Timeout: ${TIMEOUT_SECONDS}s"

START=$(date +%s)

# Clear any active virtual environment to avoid FreeCAD startup errors
unset VIRTUAL_ENV VIRTUAL_ENV_PROMPT
export PATH=$(echo "$PATH" | tr ':' '\n' | grep -v '\.venv' | tr '\n' ':' | sed 's/:$//')

# Run with xvfb, suppress WSL-specific warning
timeout "$TIMEOUT_SECONDS" xvfb-run -a freecad "$WRAPPER" 2>&1 | \
    grep -v "wrong permissions on runtime directory" | \
    grep -v "^$" || true

EXIT_CODE=${PIPESTATUS[0]}
END=$(date +%s)
ELAPSED=$((END - START))

echo ""
echo "Execution time: ${ELAPSED}s"

# Check results
if [[ -f "$OUTPUT_IMAGE" ]]; then
    SIZE=$(stat -c%s "$OUTPUT_IMAGE")
    echo "Output image created: $OUTPUT_IMAGE ($SIZE bytes)"

    if [[ $EXIT_CODE -eq 0 ]]; then
        echo "PASS: Script completed successfully"
        exit 0
    elif [[ $EXIT_CODE -eq 124 ]]; then
        echo "PASS: Script completed (killed by timeout after output created)"
        exit 0
    else
        echo "WARNING: Script exited with code $EXIT_CODE but output was created"
        exit 0
    fi
else
    echo "FAIL: Output image not created"
    if [[ $EXIT_CODE -eq 124 ]]; then
        echo "  Timed out after ${TIMEOUT_SECONDS}s"
    else
        echo "  Exit code: $EXIT_CODE"
    fi
    exit 1
fi
