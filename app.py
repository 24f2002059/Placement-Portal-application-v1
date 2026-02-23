from flask import Flask
from application.database import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement_portal.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()

from application.controllers import * 

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(role = 'admin').first()
        if not admin :
            admin = User(email="iitmadmin123@gmail.com", password="admin@123", role="admin")
            db.session.add(admin)
            db.session.commit()
    app.run(debug = True) 