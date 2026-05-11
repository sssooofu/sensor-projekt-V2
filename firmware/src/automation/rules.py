"""Evaluate relay threshold rules from config.json relay_rules."""

_OPS = {
    "<":  lambda a, b: a < b,
    ">":  lambda a, b: a > b,
    "<=": lambda a, b: a <= b,
    ">=": lambda a, b: a >= b,
    "==": lambda a, b: a == b,
}


def evaluate(rules, reading):
    """
    Check rules against the latest reading dict.
    Returns the first matching rule dict or None.

    Rule shape: { "sensor": str, "op": str, "value": number,
                  "action": str, "duration_s": int }
    """
    for rule in rules:
        sensor_val = reading.get(rule["sensor"])
        if sensor_val is None:
            continue
        op_fn = _OPS.get(rule["op"])
        if op_fn and op_fn(sensor_val, rule["value"]):
            return rule
    return None
