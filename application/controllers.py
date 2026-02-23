from .model import *
from flask import current_app as app
from flask import Flask,render_template ,request , redirect , url_for

@app.route('/')
def home():
    return render_template("home.html")

# admin backend  

@app.route('/admin-login' , methods = ['GET' , 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        admin = User.query.filter_by(email=email, role='admin').first()
        if admin and admin.password == password:
            return redirect("/admin-dashboard")
        else:
            return render_template("admin-login.html", error="Invalid credentials")
    return render_template("admin-login.html")

@app.route('/admin-dashboard')
def admin_dashboard():
    company = Company.query.all()
    unverified_company = Company.query.filter_by(status='unverified').all()
    student = Student.query.all()
    return render_template("/admin/dashboard.html", company=company, student=student, unverified_company=unverified_company)


@app.route('/company-verified/<int:company_id>')
def company_verified(company_id):
    company = Company.query.get(company_id)
    if company:
        company.status = 'verified'
        db.session.commit()
    return redirect("/admin-dashboard")

@app.route('/company-rejected/<int:company_id>')
def company_rejected(company_id):   
    company = Company.query.get(company_id)
    if company:
        company.status = 'rejected'
        db.session.commit()
    return redirect("/admin-dashboard")

# ----student backend ---- 

@app.route('/student-register' , methods = ['GET'  , 'POST'])
def student_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        academic_level = request.form['academic_level']
        phone = request.form['phone']
        github = request.form['github']
        password = request.form['password']
        resume = request.files.get('resume')
        if not resume or resume.filename == '':
            return render_template("student-register.html", error="Resume file is required")
        resume_data = resume.read()
        if User.query.filter_by(email=email).first():
            return render_template("student-register.html", error="Email already registered")
        new_user = User(email=email, password=password, role='student')
        db.session.add(new_user)    
        db.session.commit()
        new_student = Student(name=name, academic_level=academic_level, phone=phone, resume=resume_data, github_link=github, user_id=new_user.id)
        db.session.add(new_student)
        db.session.commit()
        return redirect("/student-login")
    return render_template("student-register.html")

@app.route('/student-login' , methods = ['GET'  , 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            return redirect(f"/student-dashboard/{user.student.id}")
        else:
            return render_template("student-login.html", error="Invalid credentials")
    return render_template("student-login.html")

@app.route('/student-dashboard/<int:student_id>')
def student_dashboard(student_id):
    return render_template("/student/dashboard.html", student_id=student_id)

# ---- company backend ----

@app.route('/company-register' , methods = ['GET'  , 'POST'])
def company_register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        hr_contact = request.form['hr_contact']
        website_link = request.form['website_link']
        field = request.form['field']   
        password = request.form['password']

        if User.query.filter_by(email=email,role='company').first():
            return render_template("company-register.html", error="Email already registered")
        new_user = User(email=email, password=password, role='company')
        db.session.add(new_user)    
        db.session.commit()
        new_company = Company(name=name, hr_contact=hr_contact, website_link=website_link, field=field, user_id=new_user.id)
        db.session.add(new_company)
        db.session.commit()
        return redirect("/company-login")
    return render_template("company-register.html")

@app.route('/company-login' , methods = ['GET'  , 'POST'])
def company_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, role='company').first()
        if user and user.password == password:
            company = Company.query.filter_by(user_id=user.id).first()
            return redirect(f"/company-dashboard/{company.id}")
        else:
            return render_template("company-login.html", error="Invalid credentials")
    return render_template("company-login.html")

@app.route('/company-dashboard/<int:company_id>')
def company_dashboard(company_id):
    company = db.session.get(Company, company_id)
    return render_template("/company/dashboard.html", company=company)
    