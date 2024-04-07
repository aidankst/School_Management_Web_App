import calendar
from datetime import datetime, timedelta
from app import *
from flask import Blueprint, render_template, request, flash
from sqlalchemy import asc, extract
from emails import *

payment_bp = Blueprint('payments', __name__)

months = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}

@payment_bp.route('/payments', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def payments():
    courses = Course.query.order_by(asc(Course.name)).all()
    now = datetime.now()
    invoices = Invoice.query.filter(
        extract('month', Invoice.date) == now.month,
        extract('year', Invoice.date) == now.year
    )
    return render_template('/admin/payments/manage.html', courses=courses, months=months, invoices=invoices)

@payment_bp.route('/invoice', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def invoice():
    if request.method == 'POST':
        user_id = request.form['student_id']
        course_id = request.form['course_id']
        month = int(request.form['month_name'])
        year = int(request.form['year'])

        user = User.query.filter_by(id=user_id).first()
        if user:
            student = Student.query.filter_by(id=user_id).first()
            if student:
                course = Course.query.filter_by(id=course_id).first()
                if course in student.courses.all():
                    invoice_id = int(str(course.id) + str(student.id) + str(month) + str(year))
                    invoice = Invoice.query.filter_by(id = invoice_id).first()
                    if invoice:
                        flash(f'Invoice for {user.name}, {course.name} already exists.', 'danger')
                    else:
                        if year >= course.start_date.year:
                            if month >= course.start_date.month:
                                if month >= user.start_date.month and year >= user.start_date.year:
                                    data = calculate_fees(course, user, month, year)
                                    print(data)
                                    date = datetime(int(year), int(month), 12)
                                    new_invoice = Invoice(id=invoice_id, student_id=user_id, course_id=course_id, amount=data['fees'], date=date, issuer=current_user.name, deadline = date + timedelta(days=3), status='unpaid', attending_days=data['attending_days'])
                                    db.session.add(new_invoice)
                                    student.invoices.append(new_invoice)
                                    course.invoices.append(new_invoice)
                                    db.session.commit()
                                    invoice_email(user.email, user.name, course.name, course.fees, data['fees'], month.strftime('%B'), course.start_date.strftime("%Y-%m-%d"), data['attending_days'], invoice_id)
                                    flash(f'Invoice for {course.name} created.', 'info')
                                else:
                                    flash(f'Student has not registered yet in {month}, {year}', 'danger')
                            else:
                                flash(f'Course has not started yet in {month}, {year}', 'danger')
                        else:
                            flash(f'Course has not started yet in {year}', 'danger')
                else:
                    flash(f'Student is not registered in {course.name}.', 'danger')
            else:
                flash('User is not a student!', 'danger')
        else:
            flash('User not found!', 'danger')
    return redirect('/admin/payments')


def calculate_fees(course, student, month, year):
    _, num_days = calendar.monthrange(year, month)
    if student.start_date.month != course.start_date.month and month > student.start_date.month:
        fees = course.fees
        attending_days = num_days
    else:
        unit_fees_per_day = course.fees / num_days
        if course.start_date.day <= student.start_date.day and course.start_date.year == student.start_date.year:
            attending_days = num_days - student.start_date.day
            fees = round(unit_fees_per_day * attending_days, 2 )
        elif course.start_date.day > student.start_date.day and course.start_date.year == student.start_date.year:
            attending_days = num_days - course.start_date.day
            fees = round(unit_fees_per_day * attending_days, 2 )
        
    data = {
        'fees': fees,
        'attending_days': attending_days,
    }

    return data

@payment_bp.route('/check_payments', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def check_payments():
    if request.method == 'GET':
        course_id = request.args.get('course_id')
        month = int(request.args.get('month_name'))
        year = int(request.args.get('year'))

        total_amount = 0

        course = Course.query.filter_by(id=course_id).first()
        if month >= course.start_date.month and year >= course.start_date.year:
            invoices = [
                invoice for invoice in course.invoices
                if invoice.date.month == month and invoice.date.year == year
            ]
            if invoices:
                for invoice in invoices:
                    if invoice.date.month == month and invoice.date.year == year:
                        if invoice.status == 'paid':
                            total_amount += invoice.amount
                return render_template('/admin/payments/show_payments.html', course=course, invoices=invoices, month=month, year=year, total_amount=total_amount)
            else:
                flash(f'No invoices found for {course.name}.', 'danger')
        else:
            flash('Course has not started yet!', 'danger')
    return redirect('/admin/payments')

@payment_bp.route('/pay_invoice/<int:invoice_id>', methods=['GET', 'POST'])
@login_required
@requires_roles('admin')
def pay_invoice(invoice_id):
    if request.method == 'POST':
        invoice = Invoice.query.filter_by(id = invoice_id).first()
        if invoice:
            if invoice.status == 'unpaid':
                invoice.status = 'paid'
                student = Student.query.filter_by(id=invoice.student_id).first()

                now = datetime.now()
                current_date = now.strftime("%Y-%m-%d")

                payment = Payment(id=invoice.id, student_id=invoice.student_id, amount=invoice.amount, date=current_date, attending_days=invoice.attending_days, payment_registerer=current_user.name)
                db.session.add(payment)

                student.payments.append(payment)

                db.session.commit()
                record_payment_email(user.email, user.name, invoice.id, invoice.amount, invoice.attending_days)
                flash(f'Invoice {invoice.id} paid.', 'info')
            else:
                flash(f'Invoice {invoice.id} already paid.', 'danger')
        else:
            flash('Invoice not found!', 'danger')
    return redirect('/admin/payments')