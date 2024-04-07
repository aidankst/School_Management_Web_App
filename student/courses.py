from app import *
from flask import Blueprint

course_bp = Blueprint('courses', __name__)

@course_bp.route('/courses')
@login_required
@requires_roles('student')
def courses():
    student = Student.query.filter_by(id=current_user.id).first()
    registered_courses = student.courses.all()
    return render_template('/student/courses/courses.html', logged_in=True, courses=registered_courses)
    # return redirect('/')