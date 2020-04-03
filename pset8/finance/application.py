import os

from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
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

    # Accessing data base
    users = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    stocks = db.execute("SELECT * FROM owned WHERE username = :name ", name=users[0]["username"])
    index = []
    sum = 0
    # Storing relevent info in list of dict
    for stock in stocks:
        owned = {"symbol": stock["symbol"],
                 "name": lookup(stock["symbol"])["name"],
                 "shares": stock["shares"],
                 "price": lookup(stock["symbol"])["price"],
                 "total": int(lookup(stock["symbol"])["price"])*int(stock["shares"])}
        index.append(owned)
        sum += int(owned["total"])

    sum += users[0]["cash"]

    return render_template("index.html", stocks = index, cash=users[0]["cash"], total=sum)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

     # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        quote = lookup(request.form.get("symbol"))
        share = int(request.form.get("shares"))
        cost = int(quote["price"])*share
        user = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])


        # User didn't input a symbol
        if not request.form.get("symbol"):
            return apology("Please input symbol", 403)

        # Cannot find the symbol user want
        elif quote["symbol"] is None:
            return apology("Cannot look up symbol", 403)

        # Amount of share is not larger than one
        elif share < 1:
            return apology("invalid amount of shares", 403)

        # check if user were able to purchase stock
        elif cost > user[0]["cash"] :
            return apology("Not sufficient amount of cash", 403)

        check = db.execute("SELECT * FROM owned WHERE symbol = ? AND username = ?",quote["symbol"], user[0]["username"])
        if len(check) != 1:
            # Update user newly owned stocks
            db.execute("INSERT INTO owned (symbol, username) VALUES (:symbol, :username)", symbol=quote["symbol"], username=user[0]["username"])

        # Update share amount
        db.execute("UPDATE owned SET shares = shares + :share WHERE symbol = :symbol AND username = :name", share=share, symbol=quote["symbol"], name=user[0]["username"])

        # Update purchase history
        db.execute("INSERT INTO buy VALUES ((SELECT id FROM owned WHERE username = :name AND symbol = :symbol), (SELECT id FROM users WHERE username = :user), :time, :price, :shares, :sym)",
                    name=user[0]["username"], symbol=quote["symbol"], user=user[0]["username"], time=datetime.now(), price=quote["price"], shares=share, sym=quote["symbol"])

        # Update user's cash
        db.execute("UPDATE users SET cash = cash - :cost WHERE id = :user_id", cost=cost, user_id=session["user_id"])

        # Return to home page
        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Accessing data base
    records = db.execute("SELECT * FROM buy WHERE users_id = ?", session["user_id"])
    index = []
    sum = 0
    # Storing relevent info in list of dict
    for record in records:

        owned = {"symbol": record["symbol"],
                 "shares": record["shares"],
                 "price": record["price"],
                 "transacted": record["time"]}
        index.append(owned)


    return render_template("history.html", records = index)


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
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
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
    # User reach out via POST (as by submitting a form via POST)
    if request.method == "POST":
        quote = lookup(request.form.get("quote"))
        if quote is None:
            return apology("Cannot look up symbol",403)
        else:
            return render_template("postquote.html", name=quote["name"], symbol=quote["symbol"], price=quote["price"])

    else:
        return render_template("getquote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reach out via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)

        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        if not (password == confirm):
            return apology("password doesn't match", 403)

        # update database database for username
        db.execute("INSERT INTO users (username , hash) VALUEs (:username, :hash)",
                          username = request.form.get("username"), hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8))

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("Registered")
        return redirect("/")

    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
         # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        quote = lookup(request.form.get("symbol"))
        share = int(request.form.get("shares"))
        user = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
        symbol = db.execute("SELECT * FROM owned WHERE symbol = :symbol AND username = :name", symbol=quote["symbol"], name=user[0]["username"])
        gain = int(quote["price"])*share

        # User didn't input a symbol
        if not request.form.get("symbol"):
            return apology("Please input symbol", 403)

        # Amount of share is not larger than one
        elif share > int(symbol[0]["shares"]):
            return apology("invalid amount of shares", 403)


        # Update share amount
        db.execute("UPDATE owned SET shares = shares - :share WHERE symbol = :symbol AND username = :name", share=share, symbol=quote["symbol"], name=user[0]["username"])

        # Update purchase history
        db.execute("INSERT INTO buy VALUES ((SELECT id FROM owned WHERE username = :name AND symbol = :symbol), (SELECT id FROM users WHERE username = :user), :time, :price, :shares, :sym)",
                    name=user[0]["username"], symbol=quote["symbol"], user=user[0]["username"], time=datetime.now(), price=quote["price"], shares=(-share), sym=quote["symbol"])

        # Update user's cash
        db.execute("UPDATE users SET cash = cash + :gain WHERE id = :user_id", gain=gain, user_id=session["user_id"])

        # Return to home page
        flash("Sold!")
        return redirect("/")

    else:
        user = db.execute("SELECT * FROM users WHERE id = :user_id", user_id=session["user_id"])
        symbol = db.execute("SELECT symbol FROM owned WHERE username = :name", name=user[0]["username"])

        return render_template("sell.html",symbols=symbol)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
