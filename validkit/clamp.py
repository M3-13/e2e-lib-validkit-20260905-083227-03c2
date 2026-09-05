def clamp(value: int | float, low: int | float, high: int | float) -> int | float:
    for name, arg in (("value", value), ("low", low), ("high", high)):
        if isinstance(arg, bool) or not isinstance(arg, (int, float)):
            raise TypeError(f"clamp: {name} muss vom Typ int oder float sein")
    if low > high:
        raise ValueError("clamp: low darf nicht größer als high sein")
    return max(low, min(value, high))
