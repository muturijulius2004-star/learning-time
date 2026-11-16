
import os
import secrets
import hmac

from flask import (
    Flask, request, redirect, url_for,
    session, render_template_string, abort
)
from werkzeug.security import (
    generate_password_hash, check_password_hash
)

app = Flask(__name__)

# Set SECRET_KEY in Vercel Environment Variables before deployment.
app.secret_key = os.environ.get(
    "SECRET_KEY", "novatech-local-development-only"
)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.environ.get("VERCEL") == "1"
)

# --------------------------------------------------
# 10 TEST ACCOUNTS
# These are public demonstration credentials.
# Do not use these accounts for private information.
# --------------------------------------------------

TEST_ACCOUNTS = {
    "Martin01": "Test@4821",
    "Erick02": "Test@5932",
    "Kevin03": "Test@6143",
    "Brian04": "Test@7254",
    "Daniel05": "Test@8365",
    "James06": "Test@9476",
    "Peter07": "Test@1587",
    "Alex08": "Test@2698",
    "David09": "Test@3719",
    "John10": "Test@4820"
}

PASSWORDS = {
    username: generate_password_hash(password)
    for username, password in TEST_ACCOUNTS.items()
}


# --------------------------------------------------
# SECURITY HELPERS
# --------------------------------------------------

def get_csrf_token():
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_urlsafe(32)
    return session["csrf_token"]


def check_csrf():
    submitted = request.form.get("csrf_token", "")
    stored = session.get("csrf_token", "")

    if not stored or not hmac.compare_digest(submitted, stored):
        abort(400, description="Invalid form security token.")


# --------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------

LOGIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NovaTech Solutions | Login</title>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, sans-serif;
    min-height: 100vh;
    background: linear-gradient(135deg, #092747, #1769bb);
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
}

.login-card {
    background: white;
    width: 100%;
    max-width: 420px;
    padding: 35px 28px;
    border-radius: 16px;
    box-shadow: 0 15px 45px rgba(0,0,0,.2);
}

.logo {
    text-align: center;
    margin-bottom: 30px;
}

.logo h1 {
    color: #123d70;
    font-size: 27px;
}

.logo p {
    color: #718096;
    font-size: 13px;
    margin-top: 9px;
}

h2 {
    text-align: center;
    color: #253247;
    margin-bottom: 10px;
}

.subtitle {
    text-align: center;
    color: #718096;
    font-size: 14px;
    margin-bottom: 25px;
}

label {
    display: block;
    color: #253d5b;
    font-weight: bold;
    margin: 17px 0 8px;
}

input {
    width: 100%;
    padding: 14px;
    border: 1px solid #cbd4df;
    border-radius: 7px;
    font-size: 15px;
}

input:focus {
    outline: none;
    border-color: #1769bb;
}

.password-wrap {
    position: relative;
}

.password-wrap input {
    padding-right: 75px;
}

.show-password {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    border: none;
    background: transparent;
    color: #1769bb;
    font-weight: bold;
    cursor: pointer;
}

.login-button {
    width: 100%;
    padding: 15px;
    background: #1769bb;
    color: white;
    border: none;
    border-radius: 7px;
    font-size: 16px;
    font-weight: bold;
    margin-top: 25px;
    cursor: pointer;
}

.login-button:hover {
    background: #123d70;
}

.error {
    background: #fff0f0;
    color: #b42318;
    padding: 13px;
    border-radius: 7px;
    text-align: center;
    font-size: 13px;
    margin-top: 15px;
}

footer {
    text-align: center;
    color: #9aa6b5;
    font-size: 12px;
    margin-top: 25px;
}
</style>
</head>

<body>

<div class="login-card">

    <div class="logo">
        <h1>NovaTech Solutions</h1>
        <p>Innovation • Quality • Customer Satisfaction</p>
    </div>

    <h2>Welcome Back</h2>
    <p class="subtitle">Please log in to continue.</p>

    <form method="POST" action="/login">

        <input type="hidden" name="csrf_token"
               value="{{ csrf_token }}">

        <label for="username">Username</label>

        <input
            type="text"
            id="username"
            name="username"
            placeholder="Enter your username"
            autocomplete="username"
            maxlength="40"
            required
        >

        <label for="password">Password</label>

        <div class="password-wrap">
            <input
                type="password"
                id="password"
                name="password"
                placeholder="Enter your password"
                autocomplete="current-password"
                required
            >

            <button
                type="button"
                class="show-password"
                onclick="togglePassword()"
            >SHOW</button>
        </div>

        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}

        <button type="submit" class="login-button">
            LOGIN
        </button>

    </form>

    <footer>
        © 2026 NovaTech Solutions
    </footer>

</div>

<script>
function togglePassword() {
    const field = document.getElementById("password");
    const button = document.querySelector(".show-password");

    if (field.type === "password") {
        field.type = "text";
        button.textContent = "HIDE";
    } else {
        field.type = "password";
        button.textContent = "SHOW";
    }
}
</script>

</body>
</html>
"""


# --------------------------------------------------
# MAIN SIX-PAGE WEBSITE
# --------------------------------------------------

MAIN_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>NovaTech Solutions</title>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, sans-serif;
    background: #f2f5fa;
    color: #253247;
}

header {
    background: #123d70;
    color: white;
    padding: 25px 15px;
    text-align: center;
}

header h1 {
    font-size: 27px;
    margin-bottom: 8px;
}

header p {
    font-size: 14px;
    color: #dceaff;
}

.account-bar {
    max-width: 650px;
    margin: 15px auto;
    padding: 0 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
    color: #536174;
    font-size: 13px;
}

.logout {
    background: #e4eaf2;
    color: #253d5b;
    padding: 10px 15px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: bold;
}

.container {
    max-width: 650px;
    margin: 25px auto;
    padding: 0 15px;
}

.page {
    display: none;
    background: white;
    padding: 30px 22px;
    border-radius: 12px;
    box-shadow: 0 4px 18px rgba(0,0,0,.07);
    min-height: 390px;
}

.page.active {
    display: block;
}

.page h2 {
    color: #123d70;
    margin-bottom: 18px;
    font-size: 25px;
}

.page p {
    line-height: 1.7;
    margin-bottom: 15px;
    color: #536174;
}

.hero {
    background: #e8f1ff;
    padding: 30px 15px;
    border-radius: 10px;
    text-align: center;
    margin-bottom: 20px;
}

.hero h2 {
    font-size: 28px;
}

.feature {
    background: #f4f7fc;
    padding: 15px;
    margin: 12px 0;
    border-radius: 8px;
    border-left: 4px solid #246dc0;
}

label {
    display: block;
    margin: 17px 0 8px;
    font-weight: bold;
    color: #253d5b;
}

input, textarea {
    width: 100%;
    padding: 13px;
    border: 1px solid #cbd4df;
    border-radius: 7px;
    font-size: 15px;
}

input:focus, textarea:focus {
    outline: none;
    border-color: #246dc0;
}

textarea {
    resize: vertical;
    min-height: 125px;
}

.navigation {
    display: flex;
    justify-content: space-between;
    gap: 12px;
    margin-top: 30px;
}

button {
    border: none;
    padding: 13px 25px;
    border-radius: 7px;
    font-size: 15px;
    font-weight: bold;
    cursor: pointer;
}

.next {
    background: #1769bb;
    color: white;
    margin-left: auto;
}

.back {
    background: #e4eaf2;
    color: #253d5b;
}

.submit {
    background: #16834b;
    color: white;
    width: 100%;
    margin-top: 22px;
}

button:hover {
    opacity: .88;
}

.progress {
    text-align: center;
    color: #64748b;
    margin-top: 20px;
    font-size: 13px;
}

.success {
    display: none;
    text-align: center;
    background: #e8f8ef;
    padding: 22px;
    border-radius: 9px;
    margin-top: 20px;
    color: #176b3c;
}

footer {
    text-align: center;
    padding: 25px;
    color: #748094;
    font-size: 13px;
}

@media(max-width:480px) {
    .page {
        padding: 23px 17px;
    }

    .page h2 {
        font-size: 22px;
    }

    header h1 {
        font-size: 23px;
    }
}
</style>

</head>

<body>

<header>
    <h1>NovaTech Solutions</h1>
    <p>Innovation • Quality • Customer Satisfaction</p>
</header>

<div class="account-bar">

    <span>
        Logged in as:
        <strong>{{ username }}</strong>
    </span>

    <form method="POST" action="/logout">
        <input type="hidden" name="csrf_token"
               value="{{ csrf_token }}">
        <button type="submit" class="logout">LOG OUT</button>
    </form>

</div>

<div class="container">

<!-- PAGE 1 -->

<section class="page active">

    <div class="hero">
        <h2>Welcome to NovaTech Solutions</h2>
        <p>Your trusted business partner.</p>
    </div>

    <h2>Welcome</h2>

    <p>
        We are committed to providing quality services,
        innovative solutions and excellent customer support.
    </p>

    <div class="feature">
        <strong>Our Commitment</strong>
        <p>Delivering reliable and professional business services.</p>
    </div>

    <div class="navigation">
        <button class="next" onclick="nextPage()">NEXT →</button>
    </div>

</section>


<!-- PAGE 2 -->

<section class="page">

    <h2>About Us</h2>

    <p>
        NovaTech Solutions is a business focused on providing
        dependable services and creating value for customers.
    </p>

    <div class="feature">
        <strong>Our Mission</strong>
        <p>To provide excellent services and customer experiences.</p>
    </div>

    <div class="feature">
        <strong>Our Vision</strong>
        <p>To become a trusted and respected business.</p>
    </div>

    <div class="feature">
        <strong>Our Values</strong>
        <p>Integrity, professionalism, innovation and quality.</p>
    </div>

    <div class="navigation">
        <button class="back" onclick="prevPage()">← BACK</button>
        <button class="next" onclick="nextPage()">NEXT →</button>
    </div>

</section>


<!-- PAGE 3 -->

<section class="page">

    <h2>Our Services</h2>

    <p>Discover the services we offer to our customers.</p>

    <div class="feature">
        <strong>Business Consulting</strong>
        <p>Professional guidance and business support.</p>
    </div>

    <div class="feature">
        <strong>Digital Solutions</strong>
        <p>Modern digital tools and technology services.</p>
    </div>

    <div class="feature">
        <strong>Customer Support</strong>
        <p>Dedicated assistance and customer care.</p>
    </div>

    <div class="navigation">
        <button class="back" onclick="prevPage()">← BACK</button>
        <button class="next" onclick="nextPage()">NEXT →</button>
    </div>

</section>


<!-- PAGE 4 -->

<section class="page">

    <h2>Contact Us</h2>

    <p>
        Have a question? Our team is ready to hear from you.
    </p>

    <div class="feature">
        <strong>Phone</strong>
        <p>+254 700 000 000</p>
    </div>

    <div class="feature">
        <strong>Email</strong>
        <p>info@novatech.example</p>
    </div>

    <div class="feature">
        <strong>Location</strong>
        <p>Kenya</p>
    </div>

    <div class="navigation">
        <button class="back" onclick="prevPage()">← BACK</button>
        <button class="next" onclick="nextPage()">NEXT →</button>
    </div>

</section>


<!-- PAGE 5 -->

<section class="page">

    <h2>Get Started</h2>

    <p>
        Thank you for your interest in NovaTech Solutions.
        We welcome you to explore our services and connect with us.
    </p>

    <div class="feature">
        <strong>Start Your Journey</strong>
        <p>
            Continue to our customer feedback page
            and tell us about your experience.
        </p>
    </div>

    <div class="navigation">
        <button class="back" onclick="prevPage()">← BACK</button>
        <button class="next" onclick="nextPage()">NEXT →</button>
    </div>

</section>


<!-- PAGE 6 -->

<section class="page">

    <h2>Customer Feedback</h2>

    <p>
        We value your opinion. Help us improve the quality
        of our services by completing the form below.
    </p>

    <form id="feedbackForm">

        <label for="customerName">1. Your Name</label>

        <input
            type="text"
            id="customerName"
            placeholder="Enter your full name"
            required
        >

        <label for="customerPhone">2. Phone Number</label>

        <input
            type="tel"
            id="customerPhone"
            placeholder="Enter your phone number"
            required
        >

        <label for="customerFeedback">
            3. How can we improve our services?
        </label>

        <textarea
            id="customerFeedback"
            placeholder="Tell us how we can serve you better..."
            required
        ></textarea>

        <button type="submit" class="submit">
            SUBMIT FEEDBACK
        </button>

    </form>

    <div class="success" id="successMessage">
        <h3>Thank You!</h3>
        <p>Your feedback has been completed successfully.</p>
    </div>

    <div class="navigation">
        <button class="back" onclick="prevPage()">← BACK</button>
    </div>

</section>


<div class="progress" id="progress">
    Page 1 of 6
</div>

</div>

<footer>
    © 2026 NovaTech Solutions. All rights reserved.
</footer>


<script>

let currentPage = 0;

const pages = document.querySelectorAll(".page");

function showPage(index) {

    pages.forEach((page, i) => {
        page.classList.toggle("active", i === index);
    });

    currentPage = index;

    document.getElementById("progress").textContent =
        "Page " + (currentPage + 1) + " of 6";

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

function nextPage() {

    if (currentPage < pages.length - 1) {
        showPage(currentPage + 1);
    }

}

function prevPage() {

    if (currentPage > 0) {
        showPage(currentPage - 1);
    }

}

document.getElementById("feedbackForm")
.addEventListener("submit", function(event) {

    event.preventDefault();

    if (!this.reportValidity()) return;

    document.getElementById("successMessage").style.display = "block";

    this.style.display = "none";

});

</script>

</body>
</html>
"""


# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@app.route("/")
def home():

    if not session.get("authenticated"):
        return redirect(url_for("login"))

    return render_template_string(
        MAIN_PAGE,
        username=session.get("username"),
        csrf_token=get_csrf_token()
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    if session.get("authenticated"):
        return redirect(url_for("home"))

    error = None

    if request.method == "POST":

        check_csrf()

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        password_hash = PASSWORDS.get(username)

        if password_hash and check_password_hash(
            password_hash, password
        ):

            session.clear()
            session["authenticated"] = True
            session["username"] = username

            return redirect(url_for("home"))

        error = "Invalid username or password. Please try again."

    return render_template_string(
        LOGIN_PAGE,
        error=error,
        csrf_token=get_csrf_token()
    )


@app.route("/logout", methods=["POST"])
def logout():

    check_csrf()
    session.clear()

    return redirect(url_for("login"))


# --------------------------------------------------
# LOCAL DEVELOPMENT
# Vercel imports the app object above.
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
