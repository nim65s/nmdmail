import re
from typing import Any, List, Union


def sanitize_email_address(address: Union[str, None, List[str]]) -> Any:
    if address is None:
        return None

    if isinstance(address, (list, tuple)):
        return [sanitize_email_address(a) for a in address if a is not None]

    if "," in address:
        return sanitize_email_address(address.split(","))

    address = address.strip()

    match = re.match("^(.*)<(.*)>$", address)
    if match:
        name, address = match.groups()
        return name.strip(), address.strip()
    return address


def to_bool(val) -> bool:
    if isinstance(val, str):
        return val.lower() in ("1", "true", "yes", "y")
    return bool(val)
