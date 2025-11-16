import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.flutter_test_to_junit import convert_json_lines_to_junit


def test_convert_json_lines_to_junit(tmp_path: Path):
    # Create a minimal set of machine JSON lines from flutter test
    json_lines = [
        '{"type":"testStart","test":"t1","time":1}\n',
        '{"type":"testDone","test":"t1","result":"success","time":10}\n',
        '{"type":"testStart","test":"t2","time":2}\n',
        '{"type":"testDone","test":"t2","result":"failure","time":3}\n',
    ]
    out_path = tmp_path / "out.xml"
    convert_json_lines_to_junit(json_lines, str(out_path))
    assert out_path.exists()
    root = ET.parse(out_path).getroot()
    assert root.attrib.get("tests") == "2"
    assert int(root.attrib.get("failures", "0")) == 1
    # check that the failing testcase contains a failure node
    fails = 0
    for tc in root.findall('testcase'):
        if tc.find('failure') is not None:
            fails += 1
    assert fails == 1
