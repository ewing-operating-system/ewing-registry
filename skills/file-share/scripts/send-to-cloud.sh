#!/bin/bash
# Send one or more files to Hovering Cloud
# Usage: bash send-to-cloud.sh file1 [file2] [file3] ...

set -e

PORT_FILE="$HOME/.hovering-cloud/port"
AUTHOR="$(hostname)"

# Check if server is running
if [ ! -f "$PORT_FILE" ]; then
  echo "ERROR: Hovering Cloud is not running. Port file not found."
  echo "Run: bash ~/Downloads/hovering-cloud/install.sh"
  exit 1
fi

PORT=$(cat "$PORT_FILE")

# Verify server is alive
if ! curl -s --connect-timeout 2 "http://127.0.0.1:${PORT}/items" > /dev/null 2>&1; then
  echo "ERROR: Hovering Cloud server not responding on port ${PORT}."
  echo "It may have crashed. Restart with: cd ~/.hovering-cloud/app && npx electron ."
  exit 1
fi

if [ $# -eq 0 ]; then
  echo "Usage: bash send-to-cloud.sh file1 [file2] [file3] ..."
  exit 1
fi

SENT=0
FAILED=0

for FILE in "$@"; do
  if [ ! -f "$FILE" ]; then
    echo "SKIP: $FILE (not found)"
    FAILED=$((FAILED + 1))
    continue
  fi

  FILENAME=$(basename "$FILE")
  SIZE=$(stat -f%z "$FILE" 2>/dev/null || stat --format=%s "$FILE" 2>/dev/null)

  echo "Uploading: $FILENAME ($(numfmt --to=iec $SIZE 2>/dev/null || echo "${SIZE} bytes"))..."

  RESULT=$(curl -s -w "\n%{http_code}" \
    -F "file=@${FILE}" \
    -F "author=${AUTHOR}" \
    "http://127.0.0.1:${PORT}/upload")

  HTTP_CODE=$(echo "$RESULT" | tail -1)
  BODY=$(echo "$RESULT" | head -n -1)

  if [ "$HTTP_CODE" = "200" ]; then
    echo "  -> Shared to cloud"
    SENT=$((SENT + 1))
  elif [ "$HTTP_CODE" = "413" ]; then
    echo "  -> FAILED: Cloud is full (200MB limit)"
    FAILED=$((FAILED + 1))
  else
    echo "  -> FAILED: HTTP $HTTP_CODE"
    FAILED=$((FAILED + 1))
  fi
done

echo ""
echo "Done. ${SENT} sent, ${FAILED} failed."
