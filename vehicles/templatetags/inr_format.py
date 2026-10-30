from django import template

register = template.Library()


@register.filter(name='inr')
def inr_format(value):
    """
    Format a number or Decimal into Indian Rupee currency representation:
    e.g. 5200000 -> ₹52,00,000
         185000  -> ₹1,85,000
         7800    -> ₹7,800
         4999    -> ₹4,999
    """
    if value is None or value == '':
        return '₹0'
    try:
        val = int(round(float(value)))
    except (ValueError, TypeError):
        return f"₹{value}"

    is_negative = val < 0
    val_str = str(abs(val))

    if len(val_str) <= 3:
        formatted = val_str
    else:
        last3 = val_str[-3:]
        remaining = val_str[:-3]
        parts = []
        while len(remaining) > 2:
            parts.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            parts.insert(0, remaining)
        formatted = f"{','.join(parts)},{last3}"

    return f"-₹{formatted}" if is_negative else f"₹{formatted}"
