#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <log-file>" >&2
  exit 1
fi

log_file="$1"

if [[ ! -f "$log_file" ]]; then
  echo "Error: file not found: $log_file" >&2
  exit 1
fi

count_level() {
  local level="$1"
  # Match the level as a complete word, regardless of surrounding text.
  grep -Ec "(^|[[:space:]])${level}([[:space:]]|$)" "$log_file" || true
}

total_lines=$(wc -l < "$log_file" | tr -d ' ')
info_count=$(count_level INFO)
warn_count=$(count_level WARN)
error_count=$(count_level ERROR)

printf 'Log summary: %s\n' "$log_file"
printf '%s\n' '----------------------------'
printf 'Total lines : %s\n' "$total_lines"
printf 'INFO        : %s\n' "$info_count"
printf 'WARN        : %s\n' "$warn_count"
printf 'ERROR       : %s\n' "$error_count"
printf '\nError entries:\n'

grep -nE '(^|[[:space:]])ERROR([[:space:]]|$)' "$log_file" | sed 's/^[0-9]*://' || true
