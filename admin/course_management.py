from app import *
from flask import Blueprint, request, flash
from sqlalchemy import asc
from emails import *

course_bp = Blueprint('course_management', __name__)

@course_bp.route('/course_management')
@login_required
@requires_roles('admin')
def course_management():
    courses = Course.query.order_by(asc(Course.name)).all()
    subjects = Subject.query.order_by(asc(Subject.name)).all()
    users = User.query.order_by(asc(User.name)).all()
    return render_template('/admin/course_management/manage.html', courses=courses, subjects=subjects, users=users)

@course_bp.route('/add_new_course', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def add_new_course():
    if request.method == 'POST':
        name = request.form['name']
        start_date = request.form['start_date']
        fees = request.form['fees']
        description = request.form['description']

        course = Course.query.filter_by(name = name).first()

        if not course:
            new_course = Course(name=name, start_date=start_date, fees=fees, description=description, status='active')
            db.session.add(new_course)
            db.session.commit()
            flash('Course added.','success')
            return redirect('/admin/course_management')
        else:
            flash('Course already exists.', 'danger')
        
    return redirect('/admin/course_management')

@course_bp.route('/edit_course', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def edit_course():
    if request.method == 'GET':
        course_name = request.args.get('name')
        course = Course.query.filter_by(name = course_name).first()
        if course:
            if course.start_date:
                start_date = course.start_date.strftime('%Y-%m-%d')
            else:
                start_date = ''

            if course.end_date:
                end_date = course.end_date.strftime('%Y-%m-%d')
            else:
                end_date = ''
        else:
            flash('Course does not exist.', 'danger')
            return redirect('/admin/course_management')
        return render_template('/admin/course_management/edit_course.html', course=course, start_date=start_date, end_date=end_date) 

    
@course_bp.route('/change_course_data', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def change_course_data():
    if request.method == 'POST':
        course_id = request.form['course_id']
        course = Course.query.filter_by(id = course_id).first()
        try:
            course.name = request.form['name']
            if request.form['start_date']:
                course.start_date = request.form['start_date']
            if request.form['end_date']:
                course.end_date = request.form['end_date']
            course.fees = request.form['fees']
            course.description = request.form['description']
            db.session.commit()
            flash('Course updated.','success')
            return redirect('/admin/course_management')
        except Exception as e:
            flash(e, 'danger')
            return redirect('/admin/edit_course')
        
@course_bp.route('/suspend_course', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def suspend_course():
    course_name = request.args.get('name')
    course = Course.query.filter_by(name = course_name).first()

    if course:
        if course.status != 'suspended':
            course.status = 'suspended'
            course.end_date = now = datetime.now()
            db.session.commit()
            flash('Course suspended.','success')
        else:
            flash('Course already suspended.', 'danger')
    else:
        flash('Course does not exist.', 'danger')
        
    return redirect('/admin/course_management')

@course_bp.route('/register_student_in_course', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def register_student_in_course():
    if request.method == 'GET':
        student_id = request.args.get('student_id')
        course_id = request.args.get('course_id')
        
        student = Student.query.filter_by(id = student_id).first()
        user = User.query.filter_by(id=student_id).first()
        if student:
            if user.status == 'active':
                course = Course.query.filter_by(id = course_id).first()
                if not course in student.courses.all():
                    student.courses.append(course)
                    db.session.commit()
                    course_registration_email(user.email, user.name, course.name, course.start_date.strftime("%Y-%m-%d"), course.fees)
                    flash('Student registered in course.', 'success')
                else:
                    flash('Student already registered in course.', 'danger')
            else:
                flash('Student is not active.', 'danger')
        else:
            flash('Student does not exist.', 'danger')
        return redirect('/admin/course_management')

@course_bp.route('/remove_student_from_course', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def remove_student_from_course():
    if request.method == 'GET':
        student_id = request.args.get('student_id')
        course_id = request.args.get('course_id')
        
        student = Student.query.filter_by(id = student_id).first()

        if student:
            course = Course.query.filter_by(id = course_id).first()
            if course in student.courses:
                student.courses.remove(course)
                db.session.commit()
                flash('Student removed from course.', 'success')
            else:
                flash('Student is not registered in course.', 'danger')
        else:
            flash('Student does not exist.', 'danger')
    return redirect('/admin/course_management')

@course_bp.route('/add_subject', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def add_subject():
    if request.method == 'GET':
        course_id = request.args.get('course_id')
        subject_name = request.args.get('subject_name')
        description = request.args.get('description')

        course = Course.query.filter_by(id = course_id).first()

        subject = Subject.query.filter_by(name=subject_name).first()
        if not subject in course.subjects:
            subject = Subject(name=subject_name, description=description, course_id = course.id)
            course.subjects.append(subject)
            db.session.commit()
            flash('Subject added.', 'success')
        else:
            flash('Subject already exists.', 'danger')
    return redirect('/admin/course_management')