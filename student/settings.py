from app import *
from flask import Blueprint

settings_bp = Blueprint('settings', __name__)

@settings_bp.route('/settings')
@login_required
@requires_roles('student')
def settings():
    return render_template('/student/settings/account.html', logged_in=True)