from .model import *
from flask import current_app as app
from flask import Flask,render_template ,request , redirect , url_for
from sqlalchemy import or_

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
    placement_drives = PlacementDrive.query.all()
    applications = Applications.query.all()
    return render_template("/admin/dashboard.html", company=company, student=student, unverified_company=unverified_company, placement_drives=placement_drives, applications=applications)


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

@app.route('/admin-students')
def admin_students():
    students = Student.query.all()
    return render_template("/admin/student.html", students=students)

@app.route('/admin-student-details/<int:student_id>')
def admin_student_details(student_id):
    student = Student.query.get(student_id)
    applications = Applications.query.filter_by(student_id=student_id).all()
    return render_template("/admin/student-details.html", student=student, applications=applications)

@app.route('/admin-deactivated-students/<int:student_id>')
def admin_deactivated_students(student_id):
    student = Student.query.get(student_id)
    student.status = 'deactivated'
    db.session.commit()
    return redirect(f"/admin-student-details/{student_id}")

@app.route('/search-students', methods=['GET'])
def search_students():
    search = request.args.get('search')

    if search:
        # Try to search by ID if search query is a number
        if search.isdigit():
            students = Student.query.filter(
                or_(
                    Student.name.ilike(f"%{search}%"),
                    Student.id == int(search),
                    Student.phone.ilike(f"%{search}%")
                )
            ).all()
        else:
            students = Student.query.filter(
                or_(
                    Student.name.ilike(f"%{search}%"),
                    Student.phone.ilike(f"%{search}%")
                )
            ).all()
    else:
        students = Student.query.all()

    return render_template("/admin/student.html", students=students)

@app.route('/admin-companies')
def admin_companies():
    companies = Company.query.all()
    return render_template("/admin/company.html", companies=companies)

@app.route('/admin-company-details/<int:company_id>')
def admin_company_details(company_id):  
    company = Company.query.get(company_id)
    placement_drives = PlacementDrive.query.filter_by(company_id=company_id).all()
    return render_template("/admin/company-details.html", company=company, placement_drives=placement_drives)

@app.route('/admin-deactivated-companies/<int:company_id>')
def admin_deactivated_companies(company_id):   
    company = Company.query.get(company_id)
    company.status = 'deactivated'
    db.session.commit()
    return redirect(f"/admin-company-details/{company_id}") 

@app.route('/search-companies', methods=['GET'])
def search_companies():
    search = request.args.get('search')

    if search:
        companies = Company.query.filter(
            or_(
                Company.name.ilike(f"%{search}%"),
                Company.field.ilike(f"%{search}%")
            )
        ).all()
    else:
        companies = Company.query.all()

    return render_template("/admin/company.html", companies=companies)

@app.route('/admin-placement-drives')
def admin_placement_drives():
    placement_drives = PlacementDrive.query.all()
    return render_template("/admin/placement-drive.html", placement_drives=placement_drives)

@app.route('/admin-applications')
def admin_applications():
    applications = Applications.query.all()
    return render_template("/admin/application.html", applications=applications)

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
    