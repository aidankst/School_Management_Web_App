from app import app
from app import *
from login import *
from register import *
from admin import admin_bp
from student import student_bp

app.register_blueprint(admin_bp)
app.register_blueprint(student_bp)

application = app
if __name__ == '__main__':
    # Create database tables if they don't exist
    application.run(debug=True)