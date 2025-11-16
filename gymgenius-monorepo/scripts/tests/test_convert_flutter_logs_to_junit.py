import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path


def run_converter(
    tmp_path: Path, log_content: str, name: str = "sample"
) -> Path:
    logs_dir = tmp_path / "logs"
    out_dir = tmp_path / "out"
    logs_dir.mkdir(parents=True)
    out_dir.mkdir(parents=True)
    log_file = logs_dir / f"{name}.log"
    log_file.write_text(log_content, encoding="utf-8")

    # Run the converter script
    script = Path(__file__).parents[1] / "convert_flutter_logs_to_junit.py"
    cmd = ["python3", str(script), str(logs_dir), str(out_dir)]
    # Run without raising on non-zero return; converter returns 1 when tests
    # fail.
    subprocess.run(cmd, check=False)
    out_file = out_dir / f"{name}.xml"
    assert out_file.exists()
    return out_file


def test_duration_and_sanitization(tmp_path: Path):
    log_content = """
00:00 +1: should pass (0.345s)
00:05 +1: another test "dangerous" & <stuff> (345ms)
00:10 +0 -1: failing test > dangerous (0.120s)
Some tests failed
Traceback (most recent call last):
  File "<string>", line 1, in <module>
Exception: example
"""

    out_file = run_converter(tmp_path, log_content, name="duration_sanitize")
    tree = ET.parse(out_file)
    root = tree.getroot()
    # Expect 4 testcases (3 per-line tests + suite failure) and at least one
    # failure due to the explicit failing test and the 'Some tests failed'
    assert root.attrib.get("tests") == "4"
    assert int(root.attrib.get("failures", "0")) >= 1

    names = [tc.attrib.get("name") for tc in root.findall("testcase")]
    # Ensure the sanitized names don't have <, >, or quotes
    for n in names:
        assert n is not None
        sn = str(n)
        assert "<" not in sn
        assert ">" not in sn
        assert '"' not in sn

    # check durations exist and are floats
    times = [tc.attrib.get("time") for tc in root.findall("testcase")]
    times = [t for t in times if t is not None]
    assert len(times) >= 2
    for t in times:
        assert t is not None
        # ensure it can be parsed as float > 0
        v = float(t)
        assert v > 0.0
