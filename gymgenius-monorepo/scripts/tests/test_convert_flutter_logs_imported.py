from scripts.convert_flutter_logs_to_junit import (
    _sanitize_and_extract_time,
    parse_drive_output,
)


def test_extract_durations_and_ms_s_case():
    content = """
00:00 +1: one test (0.345s)
00:05 +1: another one (345ms)
"""
    passed, _failed, _last_error = parse_drive_output(content)
    assert len(passed) == 2
    # Test sanitize and duration extraction for s
    _, duration = _sanitize_and_extract_time(passed[0])
    assert abs(duration - 0.345) < 1e-6
    # Test sanitize and duration extraction for ms
    _, duration2 = _sanitize_and_extract_time(passed[1])
    assert abs(duration2 - 0.345) < 1e-6


def test_sanitization_edge_cases():
    a = 'test "quote" & <danger>!'  # has quotes and angle brackets
    sanitized, _dur = _sanitize_and_extract_time(a)
    assert '<' not in sanitized
    assert '>' not in sanitized
    assert '"' not in sanitized
    assert '&' not in sanitized


def test_long_name_truncates():
    name = 'x' * 500
    sanitized, _dur = _sanitize_and_extract_time(name)
    assert len(sanitized) <= 250
