[README.md](https://github.com/user-attachments/files/34877171/README.md)
# TeamNet – IPv4/IPv6 Address Application

DEVASC Project Activity 3 (Option 2). A Python prototype that shows a network technician the computer's public IPv4 and IPv6 addresses, with location, country code, ISP and ASN for each.

## Team

| Member | Role |
|---|---|
| Brian Louis Ralleta | Scrum Master / Project Manager |
| Gavin Adrian Santos | Recorder & Lead Python Developer (REST API integration) |
| Andrei Hernandez | Repository Maintainer & UI/UX Lead (output formatting) |

## Setup and run

```
pip install -r requirements.txt
python ip_app.py
```

## How it works

1. Asks **ipify** for the public IPv4 (`api.ipify.org`) and IPv6 (`api6.ipify.org`). If the network has no IPv6, that request fails and the app prints "Not available on this network".
2. Sends each address to **ipapi.co** (`https://ipapi.co/<ip>/json/`) for city, region, country, country code, ISP (`org`) and ASN.
3. Prints both results in one dashboard.

We use two APIs because `ipapi.co/json/` on its own only returns one address, whichever one the connection happens to use.

## Code layout

| File | What it does | Owner / branch |
|---|---|---|
| `api.py` | `get_public_ip()`, `get_ip_details()`. Only talks to the internet, never prints. | Gavin / `feature/api-integration` |
| `display.py` | `print_ip_block()`, `print_dashboard()`. Only prints, never calls the internet. | Andrei / `feature/output-format` |
| `ip_app.py` | `main()`: gets both addresses, looks up details, prints the dashboard. | Brian / `feature/main-app` |

To show another field from ipapi.co (for example `timezone` or `postal`), add one `print` line in `print_ip_block()` in `display.py`. Full field list: https://ipapi.co/api/

## Known limits

- ipapi.co's free tier allows about 1,000 lookups a day. When the limit is hit, the app still shows the addresses and says the details are unavailable.
- Each API call waits up to 8 seconds before giving up.

## Backlog (for Project Activity 4)

- Show local LAN IP (e.g. 192.168.x.x) next to the public IP
- Save results to a text or CSV log file
- Simple GUI with Tkinter or Flask
- Automatic retry when ipapi.co rate-limits
