from cs50 import SQL
from flask import Flask, redirect,  render_template, request, session, url_for
from flask_session import Session
from email_validator import validate_email, EmailNotValidError




app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///Bardstudents.db")

students = {}

GROUPS = [
    "Class of 2026"
    "Class of 2027"
]


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")

    if not name or not email or not password:
        return render_template("register.html")
    else:
        try:
            valid = validate_email(email)
            email = valid.email  # normalized email
        except EmailNotValidError as e:
            return f"Invalid email: {str(e)}", 400
        db.execute("INSERT INTO studentlog (name, email, password) VALUES(?, ?, ?)", name, email, password)
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    name = request.form.get("name")
    password = request.form.get("password")
    check = db.execute("SELECT 1 FROM studentlog WHERE name = ? AND password = ?", name, password)
    if len (check) > 0:
        session["name"] = request.form.get("name")
        return redirect("/homepage")
    elif not check:
        return render_template("login.html")

@app.route("/homepage", methods=["GET", "POST"])
def homepage():
    name=session.get("name")
    anounce = db.execute("SELECT * FROM Posts")
    author = db.execute("SELECT student FROM Posts")
    if request.method == "POST":
        loud = request.form.get("anouncement")
        if loud != "":
            db.execute("INSERT INTO Posts (anouncements, student) VALUES(?,?)", loud, name)
            return redirect(url_for("homepage"))
    elif request.method == "GET":
        db.execute("DELETE FROM Posts WHERE student = ?", name)
    return render_template("homepage.html", name=session.get("name"), anounce=anounce)


