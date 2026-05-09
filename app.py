from flask import Flask, request, render_template, session, redirect
from db import Base, engine, SessionLocal
from utils import generate_hash_password, check_password_hash
from ai import analyze_resume

import models
import PyPDF2
import docx
import json
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

Base.metadata.create_all(bind=engine)  # create all tables if not exist


@app.route("/")
def home():
    if "user" in session:
        return redirect("/dashboard")
    return redirect("/login")

# ------------ AUTH Routes -----------  

# Login Route   
@app.route("/login", methods=["GET", "POST"])
def login():        
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        with SessionLocal() as db:
            user = db.query(models.User).filter_by(email = email).first()

            if not user or not check_password_hash(user.hashed_password, password):
                return "Invalid credentials"
            
            session["user"] = {
                "id": str(user.id),
                "email": user.email
            }

        return redirect("/dashboard")

    return render_template("login.html")

# Signup Route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        with SessionLocal() as db:
            existing_user = db.query(models.User).filter_by(email = email).first()
            if existing_user:
                return "User already exists"

            hashed_password = generate_hash_password(password)

            new_user = models.User(email = email, hashed_password = hashed_password)
            db.add(new_user)
            db.commit()

        return redirect("/login")
        

    return render_template("signup.html")

# Logout route
@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect("/login")

# ------------ DASHBOARD Routes ----------- 

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login")
    
        
    result = None

    if request.method == "POST":
        role = request.form.get("role")
        experience = request.form.get("experience")
        resume_text = request.form.get("resume_text")
        file = request.files["file"]

        # File handling for pdf and docx files
        if file and file.name != "":
            if file.filename.endswith(".pdf"):
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""
                    resume_text = text
                except Exception as e:
                    result = {"error": f"PDF Error: {str(e)}"}
            elif file.filename.endswith(".docx"):
                try:
                    doc = docx.Document(file)
                    text = ""
                    for para in doc.paragraphs:
                        text += para.text + "\n"
                    resume_text = text
                except Exception as e:
                    result = {"error": f"DOCX Error: {str(e)}"}
            else:
                result = {"error": "Unsupported file type"}

        # AI Evaluation
        if resume_text and role:
            try:
                ai_result = analyze_resume(resume_text, role, experience)
                result = ai_result # Pass dict to template
                
                # Serialize for DB storage
                db_result = json.dumps(ai_result)

                import uuid
                with SessionLocal() as db:
                    user_id_str = session["user"]["id"]
                    user_id_obj = uuid.UUID(user_id_str)
                    
                    new_report = models.Report(
                        user_id=user_id_obj, 
                        resume_text=resume_text, 
                        role=role, 
                        experience=experience,
                        result=db_result
                    )
                    db.add(new_report)
                    db.commit()
                    
                    report_id = new_report.id

            except Exception as e:
                result = {"error": f"Internal Error: {str(e)}"}
        
        
        return render_template("dashboard.html", user=session["user"], result=result)
    
    return render_template("dashboard.html", user=session["user"], result=result)
     

# History

@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")

    import uuid
    with SessionLocal() as db:
        # Get the UUID object from the session string
        user_id_obj = uuid.UUID(session["user"]["id"])
        
        # Query using the UUID object
        reports = db.query(models.Report).filter_by(user_id=user_id_obj).order_by(models.Report.created_at.desc()).all()
        
        parsed_reports = []
        for report in reports:
            try:
                parsed_result = json.loads(report.result) if report.result else {}
            except json.JSONDecodeError:
                parsed_result = {}

            parsed_reports.append({
                "id": str(report.id),
                "role": report.role,
                "resume": report.resume_text,
                "result": parsed_result,
                "date": report.created_at.strftime("%Y-%m-%d %H:%M")
            })

        return render_template("history.html", reports=parsed_reports)

@app.route("/report/<uuid:report_id>")
def view_report(report_id):
    if "user" not in session:
        return redirect("/login")

    with SessionLocal() as db:
        report = db.query(models.Report).filter_by(id=report_id).first()
        if not report or str(report.user_id) != session["user"]["id"]:
            return "Report not found or unauthorized", 404
        
        try:
            result = json.loads(report.result) if report.result else {}
        except:
            result = {"error": "Could not parse analysis result"}

        return render_template("report_detail.html", report=report, result=result)


if __name__ == "__main__":
    app.run(debug=True)