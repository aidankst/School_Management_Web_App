from app import *
from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
@requires_roles('student')
def dashboard():
    return render_template('/student/dashboard.html', logged_in=True)