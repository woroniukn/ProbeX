# ProbeX


#  :closed_lock_with_key: ProbeX – Python Security Toolkit


ProbeX is a dual-module Python toolkit designed for authorized penetration testing and network reconnaissance.

It combines:


### :globe_with_meridians: A TCP Port Scanner

### :syringe: A SQL Injection Tester

### :rocket: Features


#### :mag_right: Port Scanner

Scans TCP ports on a target host

Detects open / closed / filtered ports

Identifies running services

Supports custom port ranges

Built using Python socket


#### :syringe: SQL Injection Tester

Detects SQLi vulnerabilities in web forms

Automatically sends crafted payloads

Identifies error-based injection points

Reports vulnerable parameters

Built with requests + BeautifulSoup

:brain: How It Works

Port Scanner

Establishes TCP connections using sockets

Checks response behavior to determine port status

Attempts basic service identification

SQL Injection Tester

1. Form Discovery

Parses web pages using BeautifulSoup

2. Payload Injection

Sends payloads like:

' OR 1=1 --

3. **Detection**

   * Looks for SQL errors

   * Detects authentication bypass

   * Identifies abnormal responses

4. **Reporting**

   * Outputs vulnerable inputs

   * Highlights successful exploits

---

## 🖥️ Usage

```bash

python probex.py --scan <target>

```

Example:

```bash

python probex.py --scan 192.168.1.1

```

---

## 📊 Example Findings

### Port Scanner

* Port 80 open (Apache/2.4.65)

* Exposed `/admin` directory

* Missing security headers:

  * X-Frame-Options

  * CSP

  * HSTS

### SQL Injection Tester

* Login bypass using `' OR 1=1 --`

* Vulnerable search input

* Reflected XSS detected:

  ```html

  <script>alert(1)</script>

  ```

---

## ⚠️ Disclaimer

> This tool is intended **for educational purposes and authorized testing only**.

> Do NOT use ProbeX on systems without explicit permission.

---

## 🛠️ Tech Stack

* Python

* Socket

* Requests

* BeautifulSoup

---

## 📌 Key Learnings

* Implemented real network scanning using sockets

* Gained hands-on experience with SQL injection attacks

* Built a modular CLI-based security toolkit

---

## 📂 Project Structure

```

probex/

│── probex.py

│── scanner/

│── sqli/

│── utils/

```

---

## ⭐ Future Improvements

* Add multi-threaded scanning

* Improve service fingerprinting

* Add more vulnerability checks (XSS, CSRF, etc.)

* Export reports (JSON / HTML)

---

