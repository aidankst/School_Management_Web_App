from app import *
from flask import Blueprint

payment_bp = Blueprint ('payments', __name__)

@payment_bp.route('/invoices')
@login_required
@requires_roles('student')
def invoices():
    student = Student.query.filter_by(id=current_user.id).first()
    invoices = student.invoices
    return render_template('/student/payments/invoices.html', logged_in=True, invoices=invoices)