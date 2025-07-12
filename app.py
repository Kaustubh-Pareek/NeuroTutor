import os
from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, unset_jwt_cookies
)
from dotenv import load_dotenv
from pdf_exporter import export_to_pdf
from word_exporter import export_to_word
from summarizer import summarize
from question_generator import generate_questions
from key_concepts import generate_concepts
from utils import extract_text_from_file
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import decode_token
from models import db, User

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)

app.config["JWT_TOKEN_LOCATION"] = ["cookies"]# this tell that look in browser cookies for JWT
app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
app.config["JWT_COOKIE_SECURE"] = False # means the cookie can be sent over plain HTTP not only HTTPS

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db.init_app(app)
jwt = JWTManager(app)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        hashed_pw = generate_password_hash(password)

        if User.query.filter_by(email=email).first():
            return "Email already exists.", 409

        new_user = User(username=username, email=email, hashed_pw=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        # for auto login after signup
        access_token = create_access_token(identity=str(new_user.id))
        resp = make_response(redirect("/"))
        set_access_cookies(resp, access_token)  
        return resp

    return render_template("signup.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        email = data.get("email")
        password = data.get("password")
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=str(user.id))
            resp = make_response(redirect("/")) #response obj that is sent to the browser along with the cookie(contains JWT)
            set_access_cookies(resp, access_token)  
            return resp
        else:
            return "Invalid credentials", 401

    return render_template("login.html")


# identify the currently logged-in user
def require_auth():
    token = request.cookies.get("access_token")
    if not token:
        return None
    try:
        decoded = decode_token(token, allow_expired=False)
        user_id = str(decoded.get("sub"))
        current_logged_in_user = User.query.get(int(user_id))   
        return current_logged_in_user
    except Exception as e:
        print(" decode error:", e)
        return None


@app.route("/")
def home():
    user = require_auth()
    if not user:
        return redirect("/login")
    return render_template("index.html", user=user)  


@app.route("/generate", methods=["POST"])
def generate():
# checking user identity again
# Because every route in your Flask app is a separate request from the browser.
# HTTP is stateless, which means:server doesn’t remember the previous page.
# It needs to re-check the authentication on every request.
    user = require_auth()
    if not user:
        return redirect("/login")                

    input_method = request.form.get("input_method")
    difficulty = request.form.get("difficulty")
    file = request.files.get("file")
    text_input = request.form.get("text_input")

    if input_method == "text":
        content = text_input
        filename = "Text Input"
    elif input_method == "file" and file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        content = extract_text_from_file(filepath)
        filename = file.filename
    else:
        return "No file or text provided.", 400

    summary = summarize(content, difficulty)
    questions = generate_questions(content, difficulty)
    concepts = generate_concepts(summary, difficulty)

    return render_template(
        "guide.html",
        filename=filename,
        summary=summary,
        questions=questions,
        concepts=concepts,
        difficulty=difficulty
    )


@app.route("/exportpdf", methods=["POST"])
def pdf_export():
    return export_to_pdf(request.form)

@app.route("/export/word", methods=["POST"])
def export_word():
    return export_to_word(request.form)



@app.route("/logout")
def logout():
    resp = make_response(redirect("/login"))
    unset_jwt_cookies(resp)
    return resp

if __name__ == "__main__":
    app.run(debug=True)


