#!/usr/bin/env python3
"""
convert_flutter_logs_to_junit.py

Parse `flutter drive` console logs and convert them into JUnit XML files.

The script looks for common flutter drive output patterns like:
  - success: "00:00 +1: Some test description"
  - failure: "00:00 +0 -1: Some failing test"

It produces a single JUnit XML file per input `.log` file
in the output directory.
"""
from __future__ import annotations

import os
import re
import sys
import xml.etree.ElementTree as ET
from typing import List, Optional, Tuple


def parse_drive_output(
    content: str,
) -> Tuple[List[str], List[str], Optional[str]]:
    """Parse drive log content and return
    (passed_tests, failed_tests, failure_message).

    - passed_tests: descriptions of passing test lines
    - failed_tests: descriptions of failing test lines (or 'suite_failure')
    - failure_message: last exception/error line (truncated)
    """
    passed_tests: List[str] = []
    failed_tests: List[str] = []
    failure_message: Optional[str] = None

    for line in content.splitlines():
        # e.g. "00:00 +1: Some test description"
        m = re.match(r"^\s*\d+:\d+\s+\+(\d+):\s+(.+)$", line)
        if m:
            passed_tests.append(m.group(2).strip())
            continue

        # e.g. "00:00 +0 -1: Some failing test"
        m2 = re.match(r"^\s*\d+:\d+\s+\+\d+\s+-\d+:\s+(.+)$", line)
        if m2:
            failed_tests.append(m2.group(1).strip())
            continue

        # catch traceback lines or 'Exception' indicators
        if any(
            keyword in line
            for keyword in ("EXCEPTION", "Exception", "ERROR", "Traceback")
        ):
            # keep the latest meaningful error and bound its length
            failure_message = (line.strip()[:400])

        if "Some tests failed" in line or "Test failed" in line:
            if "suite_failure" not in failed_tests:
                failed_tests.append("suite_failure")

    return passed_tests, failed_tests, failure_message


def create_testsuite_xml(
    suite_name: str,
    passed_tests: List[str],
    failed_tests: List[str],
    failure_message: Optional[str],
) -> ET.Element:
    """Create an xml.etree.ElementTree Element for the testsuite.

    The function adds a <testcase> for each passed and failed test.
    Failing tests get a nested <failure> child with a message.
    nested <failure> child with a message and optional text.
    """
    total = len(passed_tests) + len(failed_tests)
    ts = ET.Element(
        "testsuite",
        name=suite_name,
        tests=str(total),
        failures=str(len(failed_tests)),
        errors="0",
    )

    for t in passed_tests:
        sanitized, duration_s = _sanitize_and_extract_time(t)
        tc = ET.SubElement(
            ts,
            "testcase",
            classname=str(suite_name),
            name=str(sanitized),
        )
        if duration_s is not None:
            tc.set("time", f"{float(duration_s)}")

    for t in failed_tests:
        if t == "suite_failure":
            tc = ET.SubElement(
                ts, "testcase", classname=suite_name, name=suite_name
            )
            fail_node = ET.SubElement(tc, "failure", message="suite_failure")
            fail_node.text = failure_message or "Suite failure detected"
        else:
            sanitized, duration_s = _sanitize_and_extract_time(t)
            tc = ET.SubElement(
                ts,
                "testcase",
                classname=str(suite_name),
                name=str(sanitized),
            )
            if duration_s is not None:
                tc.set("time", f"{float(duration_s)}")
            fail_node = ET.SubElement(tc, "failure", message="failure")
            fail_node.text = failure_message or f"Failure for {t}"

    return ts


def convert_log_to_junit(
    log_path: str,
    out_dir: str,
) -> str:
    """Process a single log file and write JUnit XML to out_dir.

    Returns path to the generated xml file.
    """
    name = os.path.basename(log_path)
    suite_name = name.replace(".log", "")
    with open(log_path, "r", encoding="utf-8", errors="ignore") as fh:
        content = fh.read()

    passed, failed, failure_message = parse_drive_output(content)
    testsuite = create_testsuite_xml(
        suite_name, passed, failed, failure_message
    )

    sys_out = ET.SubElement(testsuite, "system-out")
    sys_out.text = content[-5000:]

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{suite_name}.xml")
    tree = ET.ElementTree(testsuite)
    tree.write(out_path, encoding="utf-8", xml_declaration=True)
    return out_path


def _sanitize_and_extract_time(name: str) -> Tuple[str, Optional[float]]:
    """Sanitize a test name for JUnit attribute usage and
    extract duration if present.

    - removes potentially invalid XML attribute characters
    - collapses whitespace and replaces punctuation with underscores
    - extracts trailing duration in the form "(0.123s)" or "(123ms)"
    Returns (sanitized_name, duration_seconds).
    """
    if not name:
        return ("", None)
    # Extract duration at the end if present e.g.
    # "... (0.123s)" or "... (123ms)"
    dur = None
    m = re.search(r"\((?P<value>\d+(?:\.\d+)?)(?P<unit>s|ms)\)\s*$", name)
    if m:
        val = float(m.group("value"))
        unit = m.group("unit")
        dur = val if unit == "s" else val / 1000.0
        # remove the duration substring
        name = name[: m.start()].strip()

    # Replace XML attribute dangerous chars and uncommon separators
    sanitized = re.sub(r"[^\w\s\-]", "_", name)
    sanitized = re.sub(r"\s+", " ", sanitized).strip()
    # keep length reasonable
    if len(sanitized) > 250:
        sanitized = sanitized[:250]
    return sanitized, dur


def main() -> int:
    if len(sys.argv) < 3:
        print("Usage: convert_flutter_logs_to_junit.py <log_dir> <out_dir>")
        return 1

    log_dir = sys.argv[1]
    out_dir = sys.argv[2]
    any_failed = False

    if not os.path.isdir(log_dir):
        print(f"Error: {log_dir} is not a directory")
        return 2

    for fname in os.listdir(log_dir):
        if not fname.endswith(".log"):
            continue
        path = os.path.join(log_dir, fname)
        xml_path = convert_log_to_junit(path, out_dir)
        print(f"Wrote JUnit: {xml_path}")
        tree = ET.parse(xml_path)
        root = tree.getroot()
        if root.attrib.get("failures", "0") != "0":
            any_failed = True

    return 1 if any_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
