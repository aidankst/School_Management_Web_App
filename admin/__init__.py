from flask_login import login_required
from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__)

from . import dashboard

admin_bp.register_blueprint(dashboard.dashboard_bp, url_prefix='/admin')

from . import user_management

admin_bp.register_blueprint(user_management.usr_manage_bp, url_prefix='/admin')

from . import course_management

admin_bp.register_blueprint(course_management.course_bp, url_prefix='/admin')

from . import payments

admin_bp.register_blueprint(payments.payment_bp, url_prefix='/admin')


@admin_bp.route('/coming_soon')
@login_required
def coming_soon():
    return render_template('/master/index/coming_soon.html')