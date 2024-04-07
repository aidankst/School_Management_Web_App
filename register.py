from app import *
from flask import render_template, request, redirect, url_for, flash


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        phone = request.form['phone']

        user_id = User.generate_user_id()

        if not User.check_exists(email):
            user = User(id=user_id, name=name, email=email, password=User.create_password(password), role=role, phone=phone, is_verified=False, status='pending')
            db.session.add(user)
            db.session.commit()
            flash('You have successfully registered', 'success')
        else:
            flash('Email already exists', 'danger')
    return render_template('/master/auth/register.html')