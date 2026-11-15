"""
TeamNet - IPv4/IPv6 Address Application (prototype)
DEVASC Project Activity 3, Option 2
Main program (owner: Brian Louis Ralleta, branch feature/main-app)

Shows a network technician this computer's public IPv4 and IPv6 addresses,
with location, country code, ISP and ASN for each.

Files:
  api.py      - gets the data from the REST APIs  (no printing)
  display.py  - prints the dashboard               (no internet calls)
  ip_app.py   - this file, ties the two together

Run:   pip install requests
       python ip_app.py
"""

from api import IPV4_URL, IPV6_URL, get_public_ip, get_ip_details
from display import print_dashboard


def main():
    print("Fetching current public IP information...")

    # Ask for IPv4 first, then IPv6, and look up details for each one found.
    results = []
    for label, url in (("Public IPv4", IPV4_URL), ("Public IPv6", IPV6_URL)):
        ip = get_public_ip(url)
        details = get_ip_details(ip) if ip else {}
        results.append((label, ip, details))

    if all(ip is None for _, ip, _ in results):
        print("Could not get any public IP. Check your internet connection.")
        return

    print_dashboard(results)


if __name__ == "__main__":
    main()
