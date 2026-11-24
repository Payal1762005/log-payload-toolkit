# Log & Payload Toolkit

A small, recruiter-friendly command-line project demonstrating **Bash log analysis** and **Python XML/CSV parsing** using only standard tools and libraries.

## Features

- Summarises a log file: total lines, `ERROR`/`WARN`/`INFO` counts, and matching error lines.
- Parses an XML file and extracts event details.
- Parses a CSV file and reports row count, status counts, and failed records.
- Includes sample inputs and reproducible example output.

## Project structure

```text
log-payload-toolkit/
├── README.md
├── scripts/
│   ├── log_summary.sh
│   └── parse_payloads.py
└── samples/
    ├── app.log
    ├── events.xml
    └── transactions.csv
```

## Requirements

- Bash (Linux, macOS, or Git Bash on Windows)
- Python 3.8+
- No third-party Python packages

## 1. Summarise a log

```bash
bash scripts/log_summary.sh samples/app.log
```

Sample output:

```text
Log summary: samples/app.log
----------------------------
Total lines : 8
INFO        : 3
WARN        : 2
ERROR       : 3

Error entries:
2026-11-24 09:15:22 ERROR Authentication failed for user=alex
2026-11-24 09:17:03 ERROR Database connection timeout
2026-11-24 09:19:41 ERROR Payment request returned status=500
```

The script uses `grep` to count log levels and print matching error entries. It exits with a helpful message if the input file is missing.

## 2. Parse XML and CSV payloads

Parse both sample payloads:

```bash
python3 scripts/parse_payloads.py --xml samples/events.xml --csv samples/transactions.csv
```

Sample output:

```text
XML summary: samples/events.xml
Events found : 3
- id=101 | type=login | user=alex
- id=102 | type=payment | user=sam
- id=103 | type=logout | user=alex

CSV summary: samples/transactions.csv
Rows found   : 4
Status counts:
- SUCCESS: 2
- FAILED: 2

Failed records:
- transaction_id=T1002 | amount=750.00 | status=FAILED
- transaction_id=T1004 | amount=120.00 | status=FAILED
```

You can provide either `--xml` or `--csv`, or both. The XML parser uses Python's `xml.etree.ElementTree`; CSV parsing uses the built-in `csv` module.

## 3. Try your own files

```bash
bash scripts/log_summary.sh /path/to/application.log
python3 scripts/parse_payloads.py --xml /path/to/events.xml
python3 scripts/parse_payloads.py --csv /path/to/transactions.csv
```

Expected XML structure:

```xml
<events>
  <event id="101" type="login">
    <user>alex</user>
  </event>
</events>
```

Expected CSV columns: `transaction_id`, `amount`, and `status`.

## What this demonstrates

- Shell scripting and text processing with `grep`
- Command-line arguments and input validation
- Structured data parsing with XML and CSV
- Basic aggregation, filtering, and readable reporting
- Clear documentation and reproducible sample runs

## Possible extensions

- Add date-range filtering to the log analyser
- Export parsed results as JSON
- Add automated tests and GitHub Actions CI
