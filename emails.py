import os
from dotenv import load_dotenv

load_dotenv()

email_user = os.getenv('email_user')
email_password = os.getenv('email_password')


def registration_email(user_email, username, userID):
    html_body = f"""
    <html>
        <body>
            <p>Dear { username }, <br>
            <br>Greetings from the Leveling Academy!<br>
            <br>We have successfully registered you at the Leveling Academy. Please wait for the approval from the admins.<br>
            <br>Your UserID is { userID }.
            <br>Your email : { user_email }.<br>
            <br>If you have any problems accessing your account, please contact to our admins anytime.<br>
            <br>Best regards,<br>Ayar Yadanar Education Center<br>kontakt@leveling.pl</p>
        </body>
    </html>
    """

    send_email(user_email, html_body)

def approval_email(user_email, username, userID):
    html_body = f"""
    <html>
        <body>
            <p>Dear { username } | User ID: { userID }, <br>
            <br>Greetings from the Leveling Academy!<br>
            <br>We have approved your account. You can now login using your email: { user_email }.<br>
            <br>If you have any problems accessing your account, please contact to our admins anytime.<br>
            <br>Best regards,<br>Ayar Yadanar Education Center<br>kontakt@leveling.pl</p>
        </body>
    </html>
    """

    send_email(user_email, html_body)


def course_registration_email(user_email, username, course_name, starting_date, fees):
    html_body = f"""
    <html>
        <body>
            <p>Dear { username }, <br>
            <br>Greetings from the Ayar Yadanar Education Center!<br>
            <br>We have successfully registered you to {course_name}.<br>
            <br><b>Course Details</b>
            <br>Course : { course_name }
            <br>Starting Date : { starting_date }
            <br>Fees : { fees } MMK<br>
            <br>If you have any concerns, please contact to our admins anytime.<br>
            <br>Best regards,<br>Ayar Yadanar Education Center<br>kontakt@leveling.pl</p>
        </body>
    </html>
    """
    send_email(user_email, html_body)


def invoice_email(user_email, username, course_name, fees, amount, month, starting_date, attending_days, invoice_id):
    html_body = f"""
    <html>
        <body>
            <p>Dear { username } | Invoice ID : {invoice_id}, <br>
            <br>Greetings from the Ayar Yadanar Education Center!<br>
            <br>You have <b>{amount} MMK</b> outstanding to pay for {month}.<br>
            <br><b>Course Details</b>
            <br>Course : { course_name }
            <br>Starting Date : { starting_date }
            <br>Attending Days : {attending_days}
            <br>Fees : { fees } MMK<br>
            <br>If you have any concerns, please contact to our admins anytime.<br>
            <br>Best regards,<br>Ayar Yadanar Education Center<br>kontakt@leveling.pl</p>
        </body>
    </html>
    """
    send_email(user_email, html_body)


def record_payment_email(user_email, username, id, amount, attending_days):
    html_body = f"""
    <html>
        <body>
            <p>Dear { username }, <br>
            <br>Greetings from the Leveling Academy!<br>
            <br>We have received { amount } MMK for Invoice ID: { id }. You have attended { attending_days }.<br>
            <br>If you have any concerns, please contact to our admins anytime.<br>
            <br>Best regards,<br>Leveling Academy<br>kontakt@leveling.pl</p>
        </body>
    </html>
    """
    send_email(user_email, html_body)


def send_email(user_email, html_body):

    msg = MIMEMultipart()
    msg['Subject'] = "Welcome to the Ayar Yadanar Education Center!"
    msg['From'] = email_user
    msg['To'] = user_email

    part = MIMEText(html_body, 'html')
    msg.attach(part)


    server = smtplib.SMTP('smtp.zoho.eu', 587)  
    server.starttls() 
    server.login(email_user, email_password)
    server.send_message(msg)
    server.quit()