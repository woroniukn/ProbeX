# 🔍 ProbeX — Python Security Toolkit
 
> Capstone Project for **INCO Academy Cybersecurity Course**.
> A dual-module Python security toolkit for network reconnaissance and web vulnerability testing. 

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.3-lightgrey?logo=flask)
![MySQL](https://img.shields.io/badge/MySQL-PyMySQL-orange?logo=mysql)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Educational-red)

> ⚠️ **For authorized penetration testing and educational use only.** Do not use this toolkit against systems you do not own or have explicit permission to test.

---

## 📌 Overview

**ProbeX** is a Python-based security toolkit with two independent modules designed for authorized penetration testing and network reconnaissance. Both modules run from a unified CLI interface.

| Module | File | Description |
|--------|------|-------------|
| 🔌 **Port Scanner** | `scanner.py` | Scans TCP ports, detects services, and finds exposed directories |
| 💉 **SQL Injection Tester** | `flask_test.py` | Automatically tests web forms for SQLi and XSS vulnerabilities |

---

## 🧰 Tech Stack

- **Python 3**
- **Socket** — low-level TCP port scanning
- **Requests** — HTTP request crafting and payload delivery
- **BeautifulSoup** — HTML parsing for form discovery
- **Flask** — vulnerable test web application (local demo target)
- **PyMySQL** — MySQL database connection for the test app

---

## 📁 Project Structure

```
ProbeX/
├── app.py               # Vulnerable Flask web app (test target)
├── scanner.py           # Module 01 – Port Scanner
├── flask_test.py        # Module 02 – SQL Injection Tester (automated + interactive)
├── requirements.txt     # Python dependencies
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

```bash
git clone https://github.com/RicardoMor98/ProbeX.git
cd ProbeX
pip install -r requirements.txt
```

---

## 🚀 Usage (Take in notice to run the 3 Python Scripts in separate Terminal windows)

### 1. Start the vulnerable Flask test app

```bash
python app.py
# Runs on http://127.0.0.1:5001
```

### 2. Run the Port Scanner

```bash
python scanner.py
```

### 3. Run the SQL Injection Tester

```bash
python flask_test.py
```

The tester will first run an **automated pentest report**, then enter an **interactive mini-pentest mode** where you can manually inject payloads.

---

## 🔌 Module 01 — Port Scanner

Scans TCP ports on a target host to identify open services and potential security misconfigurations.

**Features:**
- Detects open / closed / filtered ports
- Identifies running services and versions
- Exposed directory discovery (e.g., `/admin`, `/.git`, `/backup`)
- Built with Python's native `socket` library

**Demo findings from local test server (`python3 -m http.server 8000`):**

| Finding | Detail |
|---------|--------|
| Port 80 open | Apache/2.4.65 (Debian) |
| Missing security headers | `X-Frame-Options`, `CSP`, `HSTS` |
| Exposed `/admin` directory | No authentication required |

> The scanner discovered a hidden `/admin` path containing an `index.html` file ("secret panel") — accessible in the browser with no login or restrictions.

**Recommendations:**
- Implement authentication middleware on sensitive routes
- Add security headers (`X-Frame-Options`, `Content-Security-Policy`, `HSTS`)
- Remove or restrict admin directories from public access

---

## 💉 Module 02 — SQL Injection Tester

Automatically tests web application forms for SQL injection and reflected XSS vulnerabilities.

**Features:**
- Discovers forms automatically via HTML parsing
- Injects crafted payloads (e.g., `' OR 1=1 --`)
- Detects error-based injection points
- Reports vulnerable parameters
- Validates reflected XSS with `<script>` and `<img onerror>` payloads
- Interactive mini-pentest mode for manual testing

**How it works:**

```
1. Discover  →  BeautifulSoup parses /login to extract form fields
2. Inject    →  requests sends crafted payloads like ' OR 1=1 --
3. Detect    →  Error-based detection via DEBUG SQL logs
4. Report    →  Shows which payloads bypass auth or return all users
5. XSS check →  Reflected payloads confirm additional injection points
```

**Automated report results:**

| Test | Payload | Result |
|------|---------|--------|
| Login SQLi | `' OR 1=1 --` | ✅ SUCCESS (auth bypass) |
| Login SQLi | `' OR username='alice' --` | ✅ SUCCESS |
| Search SQLi | `%' OR 1=1 -- %` | ✅ Users returned |
| Search SQLi | `%' OR 1=2 -- %` | ❌ No users returned |
| XSS | `<script>alert('XSS1')</script>` | ⚠️ Reflected |
| XSS | `<img src=x onerror=alert('XSS2')>` | ⚠️ Reflected |

---

## 🎯 Key Learnings

- Applied Python socket programming for real network interaction
- Understood how SQL injection attacks work at the HTTP request level
- Built modular, reusable code structured for a real security toolkit

---

## ⚖️ Disclaimer

ProbeX is intended **strictly for educational purposes and authorized security testing**. The authors are not responsible for any misuse of this tool. Always obtain explicit written permission before testing any system you do not own.

---

## 👤 Author

**Ricardo Moreira** — [@RicardoMor98](https://github.com/RicardoMor98)
**Nair Woroniuk** — [@woroniukn](https://github.com/woroniukn)

Capstone Project · INCO Academy Cybersecurity Course

Built with Python · For authorized testing only
