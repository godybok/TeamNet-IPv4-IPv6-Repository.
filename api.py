"""
api.py - REST API integration (owner: Gavin Adrian Santos, branch feature/api-integration)

Gets this computer's public IP addresses and the details for each one.
These functions only talk to the internet. They never print anything,
so the display code (display.py) can format the results however it likes.

APIs used (free, no API key):
  - ipify    https://www.ipify.org  -> public IPv4 (api.ipify.org) or IPv6 (api6.ipify.org)
  - ipapi.co https://ipapi.co       -> location, ISP and ASN for one IP
                                       (free limit: about 1,000 lookups a day)

Why two APIs? ipapi.co/json/ on its own only returns ONE address, whichever
one the connection happens to use. ipify lets us ask for IPv4 and IPv6 separately.
"""

import requests

# ---------------------------------------------------------------------------
# Settings
# ---------------------------------------------------------------------------
IPV4_URL = "https://api.ipify.org?format=json"     # answers over IPv4 only
IPV6_URL = "https://api6.ipify.org?format=json"    # answers over IPv6 only
DETAILS_URL = "https://ipapi.co/{ip}/json/"        # {ip} is replaced with the address

TIMEOUT = 8   # seconds to wait before giving up on an API

# ipapi.co sometimes blocks the default "python-requests" name, so we send our own.
HEADERS = {"User-Agent": "TeamNet-IP-App/1.0 (student project)"}


# ---------------------------------------------------------------------------
# API functions
# ---------------------------------------------------------------------------
def get_public_ip(url):
    """
    Ask ipify for our public address.
    Returns the IP as text, or None if it fails
    (no internet, no IPv6 on this network, timeout, etc.).
    """
    try:
        response = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()           # turn HTTP errors (404, 500) into exceptions
        return response.json().get("ip")      # ipify replies {"ip": "x.x.x.x"}
    except (requests.RequestException, ValueError):
        return None                           # ValueError = reply was not JSON


def get_ip_details(ip):
    """
    Ask ipapi.co for location, ISP and ASN of one IP.
    Always returns a dictionary. If something went wrong it contains
    {"error": True, "reason": "..."} so the display code can show why.
    """
    try:
        response = requests.get(DETAILS_URL.format(ip=ip), headers=HEADERS, timeout=TIMEOUT)
        if response.status_code == 429:
            return {"error": True, "reason": "Daily lookup limit reached. Try again later."}
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return {"error": True, "reason": f"Could not reach ipapi.co ({e.__class__.__name__})"}
    except ValueError:
        return {"error": True, "reason": "ipapi.co did not send back JSON"}

    # ipapi.co can also report errors inside a normal reply,
    # e.g. {"error": true, "reason": "RateLimited"}
    if data.get("error"):
        return {"error": True, "reason": data.get("reason", "Unknown error")}
    return data
