"""
display.py - Output formatting (owner: Andrei Hernandez, branch feature/output-format)

Prints the IP results as a dashboard for network technicians.
These functions only print. They never call the internet.
To show another ipapi.co field (e.g. "timezone" or "postal"), add one
print line in print_ip_block(). Field list: https://ipapi.co/api/
"""

# ---------------------------------------------------------------------------
# Display functions
# ---------------------------------------------------------------------------
LINE = "=" * 50


def show_value(data, key):
    """Return a field from the API data, or '-' if it is empty."""
    value = data.get(key)
    return value if value not in (None, "") else "-"


def print_ip_block(label, ip, details):
    """Print one section (IPv4 or IPv6) of the dashboard."""
    print(f"\n[ {label} ]")
    if ip is None:
        print("  Not available on this network")
        return
    print(f"  Address      : {ip}")
    if details.get("error"):
        print(f"  Details      : unavailable - {details['reason']}")
        return
    print(f"  Location     : {show_value(details, 'city')}, {show_value(details, 'region')}")
    print(f"  Country      : {show_value(details, 'country_name')} ({show_value(details, 'country_code')})")
    print(f"  ISP          : {show_value(details, 'org')}")
    print(f"  ASN          : {show_value(details, 'asn')}")


def print_dashboard(results):
    """results is a list of (label, ip, details) tuples."""
    print(LINE)
    print("     TEAMNET - NETWORK TECHNICIAN IP DASHBOARD")
    print(LINE)
    for label, ip, details in results:
        print_ip_block(label, ip, details)
    print("\n" + LINE)
