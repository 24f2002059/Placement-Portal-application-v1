from .database import db

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer , primary_key = True)
    email = db.Column(db.String(100) ,nullable = False , unique = True)
    password = db.Column(db.String(150) , nullable = False)
    role = db.Column(db.String(20) , nullable = False)

    student = db.relationship('Student' , backref = 'user' , uselist = False , cascade = 'all, delete-orphan') 
    company = db.relationship('Company' , backref = 'user' , uselist = False , cascade = 'all, delete-orphan')


class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer , primary_key = True)
    user_id = db.Column(db.Integer ,db.ForeignKey('user.id'),nullable = False)
    name = db.Column(db.String(50) , nullable = False)
    hr_contact = db.Column(db.String(150) , nullable = False , unique = True)
    website_link = db.Column(db.String(500) , nullable = False)
    field = db.Column(db.String(50) , nullable = False)
    status = db.Column(db.String(50) , nullable = False , default = "unverified")

    placement_drive = db.relationship('PlacementDrive' , backref = 'company' , cascade = 'all, delete-orphan')


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer , primary_key = True)
    user_id = db.Column(db.Integer ,db.ForeignKey('user.id'),nullable = False)
    name = db.Column(db.String(50) , nullable = False)
    academic_level = db.Column(db.String(100) , nullable = False)
    phone = db.Column(db.String(50) , nullable = False)
    resume = db.Column(db.LargeBinary , nullable = False)
    github_link = db.Column(db.String(300))
    
    student_applications = db.relationship('Applications',backref = "student" , cascade = "all, delete-orphan")

class PlacementDrive(db.Model):
    __tablename__ = "placementdrive"
    id = db.Column(db.Integer , primary_key = True)
    company_id = db.Column(db.Integer , db.ForeignKey('company.id') , nullable = False)
    job_title = db.Column(db.String(100), nullable=False)  
    mode = db.Column(db.String(50), nullable=False) 
    package = db.Column(db.Float, nullable=False)
    eligibility = db.Column(db.Text , nullable = False)
    description = db.Column(db.Text,  nullable = False)
    deadline = db.Column(db.Date , nullable = False)
    status = db.Column(db.String(50), nullable=False, default='Pending')

    drive_application = db.relationship('Applications' , backref = 'placementdrive' ,cascade = "all, delete-orphan")


class Applications(db.Model):
    __tablename__ = "applications"
    id = db.Column(db.Integer , primary_key = True)
    drive_id = db.Column(db.Integer , db.ForeignKey('placementdrive.id') , nullable = False)
    student_id = db.Column(db.Integer , db.ForeignKey('student.id') , nullable = False)
    application_date =  db.Column(db.Date, nullable=False , default=db.func.current_date())
    status = db.Column(db.String(50), nullable=False, default='Applied')

    
