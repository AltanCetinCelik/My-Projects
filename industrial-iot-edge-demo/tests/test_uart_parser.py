from edge.edge_gateway_demo import parse_uart_bridge_line


def test_parse_can_line():
    sample = parse_uart_bridge_line("<CAN,201,8,5A032A0302000000>")

    assert sample is not None
    assert sample.machine_id == "NODE_201"
    assert sample.rpm == 858
    assert sample.temperature_c == 62
    assert sample.vibration_mm_s == 0.3
    assert sample.current_a == 0.2


def test_ignore_heartbeat_line():
    assert parse_uart_bridge_line("<HB,51000,1,14,8>") is None
