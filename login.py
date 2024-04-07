from app import app
from app import *
from flask import request, flash, redirect, url_for
from flask_login import login_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email and password:
            user = User.query.filter_by(email=email).first()
            # result = db.session.execute(db.select(User).where(User.email == email))
            # user = result.scalar()
            

            if user and User.check_password(email, password):
                if user.is_verified:
                    if user.status == 'active':
                        login_user(user, remember=True)
                        if user.role == 'admin':
                            return redirect('/admin/dashboard')
                        elif user.role == 'student':
                            return redirect('/student/dashboard')
                    else:
                        flash('User is not active', 'danger')
                else:
                    flash('Admin has not verified yet!', 'danger')
            else:
                flash('Invalid email or password', 'danger')
        else:
            flash('Email and password are required', 'danger')
    # return redirect(url_for('index'))
    return render_template('/master/auth/login.html')