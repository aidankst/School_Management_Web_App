from app import *
from flask import Blueprint, render_template, request, flash
from sqlalchemy import asc

usr_manage_bp = Blueprint('user_management', __name__)

@usr_manage_bp.route('/user_management')
@login_required
@requires_roles('admin')
def user_management():
    pending_users = User.query.filter_by(is_verified=False).all()
    users = User.query.order_by(asc(User.role)).all()
    return render_template('/admin/user_management/manage.html', pending_users=pending_users, users=users)

@usr_manage_bp.route('/edit_user', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def edit_user():
    user_id = request.args.get('user_id')
    
    result = db.session.execute(db.select(User).where(User.id == user_id))
    user = result.scalar()
    
    if not user:
        flash('User does not exist', 'danger')
        return redirect('/admin/user_management')
    
    if user.role == 'employee':
        employee = Employee.query.filter_by(id=user.id).first()
        return render_template('/admin/user_management/edit_user.html', user=user, employee=employee)
    elif user.role == 'student':
        student = Student.query.filter_by(id=user.id).first()
        return render_template('/admin/user_management/edit_user.html', user=user, student=student)
    return render_template('/admin/user_management/edit_user.html', user=user)

@usr_manage_bp.route('/change_user_data', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def change_user_data():
    try:
        if request.method == 'POST':
            result = db.session.execute(db.select(User).where(User.id == request.form['user_id']))
            user = result.scalar()

            user.name = request.form['name']
            user.email = request.form['email']
            user.phone = request.form['phone']
            
            try:
                if user.role == 'employee':
                    salary = float(request.form['salary'])

                    employee = Employee.query.filter_by(id=user.id).first()

                    if not employee:
                        new_employee = Employee(id=user.id, salary=salary)
                        db.session.add(new_employee)
                        db.session.commit()
                    else:
                        employee.salary = salary
                        db.session.commit()
                    flash('User updated', 'success')

                elif user.role == 'student':
                    father_name = request.form['father_name']
                    mother_name = request.form['mother_name']

                    student = Student.query.filter_by(id=user.id).first()
                    if not student:
                        new_student = Student(id=user.id, father_name=father_name, mother_name=mother_name)
                        print(new_student.father_name)
                        db.session.add(new_student)
                        db.session.commit()
                        flash('User updated', 'success')
                    else:
                        student.father_name = father_name
                        student.mother_name = mother_name
                        db.session.commit()
                        flash('User updated', 'success')

                else:
                    flash('Invalid role', 'danger')
                return redirect('/admin/user_management')
            except Exception as e:
                flash(str(e), 'danger')
                return redirect('/admin/user_management')
    except Exception as e:
        flash(str(e), 'danger')
        return redirect('/admin/user_management')
    

@usr_manage_bp.route('/suspend_user', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def suspend_user():
    user_id = request.form['user_id']

    result = db.session.execute(db.select(User).where(User.id == user_id))
    user = result.scalar()

    if not user:
        flash('User does not exist', 'danger')

    if user.status != 'suspended':
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")

        user.end_date = current_date
        user.status ='suspended'
        db.session.commit()
        flash('User suspended','success')
    else:
        flash('User already suspended', 'danger')
    return redirect('/admin/user_management')

@usr_manage_bp.route('/approve/<int:user_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def approve(user_id):
    result = db.session.execute(db.select(User).where(User.id == user_id))
    user = result.scalar()
    
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")

    user.start_date = current_date
    user.is_verified = True
    user.status = 'active'
    db.session.commit()
    approval_email(user.email, user.name, user.id)
    flash('User approved!', 'success')
    return redirect('/admin/user_management')

@usr_manage_bp.route('/decline/<int:user_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def decline(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    flash('User declined!', 'danger')
    return redirect('/admin/user_management')