from cs50 import SQL
from flask import Flask, render_template, redirect, request,flash,session
from flask_session import Session
## from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///users.db")

def apology(message, code=400):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("error.html", top=code, bottom=escape(message)), code

@app.route("/")# Mi ruta principal
def index():
    return render_template("index.html")


@app.route("/inicio")
def inicio():
    return render_template("inicio.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":


        if not request.form.get("username"):
            return apology("Error en el nombre de usuario", 403)


        elif not request.form.get("password"):
            return apology("Error en la contraseña", 403)


        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))


        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology("Usuario invalido and/or contraseña", 403)

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


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        usuario = request.form.get("username")
        contraseña = request.form.get("password")
        confirmar =  request.form.get("confirmation")

        if contraseña != confirmar:
            return apology("contraseña no conincide",400)

        if not contraseña or not confirmar or not usuario:
            return apology("campos vacios",400)


        if db.execute("select * from users where username = :usuario",usuario = usuario):
            return apology("Usuario existe",400)

        else:
            passw = generate_password_hash(contraseña)
            insertar = db.execute(f"INSERT INTO users(username,password) values('{usuario}','{passw}')")
            session["user_id"] = insertar
            return redirect("/")
    else:

        return render_template("register.html")
