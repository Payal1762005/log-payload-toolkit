#!/usr/bin/env python3
"""Parse sample XML events and CSV transaction records."""

import argparse
import csv
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


def parse_xml(path: Path) -> None:
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        raise ValueError(f"could not parse XML file '{path}': {exc}") from exc

    events = root.findall(".//event")
    print(f"XML summary: {path}")
    print(f"Events found : {len(events)}")
    for event in events:
        event_id = event.get("id", "N/A")
        event_type = event.get("type", "N/A")
        user = event.findtext("user", default="N/A")
        print(f"- id={event_id} | type={event_type} | user={user}")


def parse_csv(path: Path) -> None:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            required = {"transaction_id", "amount", "status"}
            columns = set(reader.fieldnames or [])
            missing = required - columns
            if missing:
                raise ValueError(
                    f"CSV file '{path}' is missing columns: {', '.join(sorted(missing))}"
                )
            rows = list(reader)
    except OSError as exc:
        raise ValueError(f"could not read CSV file '{path}': {exc}") from exc

    statuses = Counter(row["status"].strip().upper() for row in rows)
    print(f"CSV summary: {path}")
    print(f"Rows found   : {len(rows)}")
    print("Status counts:")
    for status, count in sorted(statuses.items()):
        print(f"- {status}: {count}")

    failed = [row for row in rows if row["status"].strip().upper() == "FAILED"]
    print("\nFailed records:")
    if not failed:
        print("- None")
    else:
        for row in failed:
            print(
                f"- transaction_id={row['transaction_id']} | "
                f"amount={row['amount']} | status={row['status']}"
            )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarise XML event payloads and CSV transaction records."
    )
    parser.add_argument("--xml", type=Path, help="Path to an XML events file")
    parser.add_argument("--csv", type=Path, help="Path to a CSV transactions file")
    args = parser.parse_args()

    if not args.xml and not args.csv:
        parser.error("provide at least one of --xml or --csv")

    try:
        if args.xml:
            parse_xml(args.xml)
        if args.csv:
            if args.xml:
                print()
            parse_csv(args.csv)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
