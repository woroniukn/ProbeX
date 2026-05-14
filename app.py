from flask import Flask, request, render_template_string
import pymysql

app = Flask(__name__)

# -----------------------
# Config
# -----------------------
DEBUG_SQL = True  # Show debug info for educational purposes

# Connect to MariaDB
conn = pymysql.connect(
    host='localhost',
    user='flaskuser',    # your test user
    password='flaskpass',
    database='test_db'
)

# -----------------------
# HTML Templates
# -----------------------
INDEX_HTML = """
<h1>Users Table</h1>
<form method="GET">
    Search Username: <input name="username">
    <input type="submit" value="Search">
</form>
<ul>
{% for user in users %}
    <li>{{ user['id'] }} - {{ user['username'] }} - {{ user['password'] }}</li>
{% endfor %}
</ul>
<a href="{{ url_for('products') }}">Go to Products</a> | 
<a href="{{ url_for('login') }}">Login Page</a> | 
<a href="{{ url_for('xss_test') }}">XSS Test</a>
"""

PRODUCTS_HTML = """
<h1>Products Table</h1>
<ul>
{% for product in products %}
    <li>{{ product['id'] }} - {{ product['name'] }} - ${{ product['price'] }}</li>
{% endfor %}
</ul>
<a href="{{ url_for('index') }}">Users</a> | 
<a href="{{ url_for('login') }}">Login</a> | 
<a href="{{ url_for('xss_test') }}">XSS Test</a>
"""

LOGIN_HTML = """
<h1>Login</h1>
<form method="POST">
    Username: <input name="username"><br>
    Password: <input name="password" type="password"><br>
    <input type="submit" value="Login">
</form>
<p>{{ message }}</p>
<a href="{{ url_for('index') }}">Users</a> | 
<a href="{{ url_for('products') }}">Products</a> | 
<a href="{{ url_for('xss_test') }}">XSS Test</a>
"""

XSS_HTML = """
<h1>XSS Test</h1>
<form method="POST">
    Enter some text: <input name="text">
    <input type="submit" value="Submit">
</form>
<p>Your input: {{ user_input|safe }}</p>
<a href="{{ url_for('index') }}">Users</a> | 
<a href="{{ url_for('products') }}">Products</a> | 
<a href="{{ url_for('login') }}">Login</a>
"""

# -----------------------
# Routes
# -----------------------
@app.route('/', methods=['GET'])
def index():
    username_query = request.args.get('username', '')
    users = []

    if username_query:
        cur = conn.cursor(pymysql.cursors.DictCursor)
        # intentionally vulnerable to SQL injection
        sql = f"SELECT * FROM users WHERE username LIKE '%{username_query}%'"
        if DEBUG_SQL:
            print(f"[DEBUG SQL] Users search query: {sql}")
        cur.execute(sql)
        users = cur.fetchall()

    return render_template_string(INDEX_HTML, users=users)

@app.route('/products')
def products():
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    return render_template_string(PRODUCTS_HTML, products=products)

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')

        cur = conn.cursor(pymysql.cursors.DictCursor)
        # intentionally vulnerable to SQL injection
        sql = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        if DEBUG_SQL:
            print(f"[DEBUG SQL] Login query: {sql}")
        cur.execute(sql)
        user = cur.fetchone()

        if user:
            message = f"Welcome, {user['username']}! Login successful."
        else:
            message = "Login failed."

    return render_template_string(LOGIN_HTML, message=message)

@app.route('/xss', methods=['GET', 'POST'])
def xss_test():
    user_input = ""
    if request.method == 'POST':
        user_input = request.form.get('text', '')

        # DEBUG: show reflected input
        if DEBUG_SQL:
            print(f"[DEBUG XSS] User input reflected: {user_input}")

        # Displayed directly for XSS practice (vulnerable intentionally)
    return render_template_string(XSS_HTML, user_input=user_input)

# -----------------------
# Main
# -----------------------
if __name__ == '__main__':
    app.run(debug=True, port=5001)
