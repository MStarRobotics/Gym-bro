#!/usr/bin/env python3
"""
Simple converter for `flutter test --machine` JSON events to JUnit XML.
It reads JSON lines from stdin, aggregates 'testDone' events, and reports
pass/fail per test case.
"""
import json
import sys
import xml.etree.ElementTree as ET

# os module not needed; can be removed


def convert_json_lines_to_junit(json_lines, out_path):
    tests = []
    failures = 0
    # start_time isn't used; tests are reported per testDone events
    for line in json_lines:
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if obj.get('type') == 'testStart':
            # testStart contains metadata; ignoring start_time for now
            _ = obj.get('time')
        if obj.get('type') == 'testDone':
            name = obj.get('test')
            result = obj.get('result')
            duration = obj.get('time')
            tests.append((name, result, duration))
            if result != 'success':
                failures += 1

    suite = ET.Element(
        'testsuite',
        name='flutter_tests',
        tests=str(len(tests)),
        failures=str(failures),
    )
    for name, result, duration in tests:
        tc = ET.SubElement(suite, 'testcase', classname='flutter', name=name)
        if result != 'success':
            failure = ET.SubElement(tc, 'failure', message=result)
            failure.text = f'Test result: {result}'

    tree = ET.ElementTree(suite)
    tree.write(out_path, encoding='utf-8', xml_declaration=True)


def main():
    if len(sys.argv) < 2:
        print('Usage: flutter_test_to_junit.py output.xml')
        sys.exit(1)
    out_path = sys.argv[1]
    lines = sys.stdin.readlines()
    convert_json_lines_to_junit(lines, out_path)


if __name__ == '__main__':
    main()
