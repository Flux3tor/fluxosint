# FluxOSINT

FluxOSINT is a modular, web-based OSINT (Open-Source Intelligence) platform built with FastAPI and vanilla JavaScript.

It collects and analyzes publicly available data for:

- Emails
- Username
- Domains
- IP addresses

It also includes **LeakGuard**, a privacy-safe password exposure checker using k-anonymity (your password never leaves the browser).

---

## Live Demo

Frontend:
https://fluxosint.flux3tor.xyz

API Docs:
https://api.fluxosint.flux3tor.xyz/docs

---

## Current Modules (WIP)

### Email Intel
- MX record lookup
- Disposable email detection
- Domain age check
- Gravatar presence
- Public paste mentions
- Risk scoring

### Username Intel
Checks username presence across:
- Github
- Reddit
- Twitter / X

### Domain Intel
- IP resolution
- WHOIS creation date
- Registrar information

### IP Intel
- Country
- City
- ISP
- Organization

### LeakGuard
Client-side SHA-1 hashing + k-anonymity against the HaveIBeenPwned range API.
The backend only receives the first 5 hash characters.

---

## Tech Stack

**Backend**
- FastAPI
- SQLite
- dnspython
- python-whois
- requests
- BeautifulSoup

**Frontend**
- HTML
- CSS
- Vanilla JavaScript

**Deployment**
- Render (backend)
- Github Pages (frontend)
- Custom domain

---

## Disclaimer

FluxOSINT only uses publicly accessible data sources.
Built for educational and ethical research purposes.

Do not use it for harassment, stalking, or privacy violations.

---