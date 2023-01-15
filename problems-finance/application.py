import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]
    cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]['cash']
    cash_total = cash
    shares = db.execute("SELECT symbol, shares FROM purchases WHERE user_id = ? GROUP BY symbol", user_id)

    for share in shares:
        share['price'] = lookup(share['symbol'])['price']
        share['total'] = share['shares'] * share['price']
        cash += share['total']
        share['price'] = usd(share['price'])
        share['total'] = usd(share['total'])

    return render_template("index.html", cash_total=usd(cash_total), cash=usd(cash), shares=shares)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == 'POST':
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")
        quote = lookup(symbol)
        user_id = session["user_id"]

        if not symbol:
            return apology("must provide a stock's symbol")

        elif not quote:
            return apology("Stock not found")

        if not shares:
            return apology
         
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("invalid shares", 400)
            
        if not int(shares) > 0:
            return apology("invalid shares", 400)

        else:
            total = quote['price'] * int(shares)
            cash = db.execute("SELECT cash FROM users WHERE id = ?", user_id)[0]['cash']
            cash -= total

            if cash >= 0:
                db.execute("UPDATE purchases SET shares = shares + ? WHERE user_id = ? AND symbol = ?", 
                           shares, user_id, quote['symbol'])
                db.execute("INSERT or IGNORE INTO purchases (user_id, symbol, shares) VALUES(?, ?, ?)", 
                           user_id, quote['symbol'], shares)
                db.execute("INSERT INTO history (user_id, symbol, shares, price, transact) VALUES(?, ?, ?, ?, ?)", 
                           user_id, quote['symbol'], shares, quote['price'], 'bought')
                db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, user_id)
                return redirect("/")

            else:
                return apology("Can't afford :(")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT * FROM history WHERE user_id = ?", session["user_id"])
    for row in history:
        row['price'] = usd(row['price'])
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to log in
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")
        

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        quote = lookup(symbol)

        if not quote:
            return apology("Stock not found")

        return render_template('quoted.html', name=quote['name'], symbol=quote['symbol'], price=usd(quote['price']))

    return render_template('quote.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))
        # Ensure username was submitted
        if not name:
            return apology("must provide username")

        username_exists = db.execute("SELECT username FROM users WHERE username = ?", name)
        if username_exists:
            return apology("username already exists")

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password")

        if not request.form.get("confirmation"):
            return apology("confirm your password")

        if not request.form.get("password") == request.form.get("confirmation"):
            return apology("the passwords do not match")

        register = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", name, password)
        session["user_id"] = register

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session['user_id']

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = db.execute("SELECT symbol, shares FROM purchases WHERE user_id = ? GROUP BY symbol", user_id)[0]
        sell = int(request.form.get("shares"))
        available = shares['shares']

        if not symbol:
            return apology("select a symbol")

        if not sell > available:
            sell_price = lookup(request.form.get('symbol'))['price']
            db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", sell_price * sell, user_id)

        else:
            return apology("not enough shares")

        if sell == available:
            db.execute("DELETE FROM purchases WHERE user_id = ? AND symbol = ?", user_id, shares['symbol'])
        else:
            db.execute("UPDATE purchases SET shares = shares - ? WHERE user_id = ? AND symbol = ?", sell, user_id, shares['symbol'])

        sell = 0 - sell
        db.execute("INSERT INTO history (user_id, symbol, shares, price, transact) VALUES(?, ?, ?, ?, ?)", 
                   user_id, shares['symbol'], sell, sell_price, 'sold')

        return redirect("/")

    else:
        shares = db.execute("SELECT DISTINCT symbol FROM purchases WHERE user_id = ?", user_id)
        options = []
        for share in shares:
            options.append(share['symbol'])

        return render_template("sell.html", options=options)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
