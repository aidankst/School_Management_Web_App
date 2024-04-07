from app import *
from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
@requires_roles('admin')
def dashboard():
    # return render_template('/admin/dashboard.html')
    return redirect('/coming_soon')