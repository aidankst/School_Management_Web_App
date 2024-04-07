from flask import Blueprint

student_bp = Blueprint('student', __name__)

from . import dashboard

student_bp.register_blueprint(dashboard.dashboard_bp, url_prefix='/student')

from . import courses

student_bp.register_blueprint(courses.course_bp, url_prefix='/student')

from . import payments

student_bp.register_blueprint(payments.payment_bp, url_prefix='/student')

from . import settings

student_bp.register_blueprint(settings.settings_bp, url_prefix='/student')