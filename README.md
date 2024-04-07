# School Management System
***A web-based application to streamline student, course, and payment management.***

**By**: Kaung Sithu (front-end, back-end), Min Khant Soe Oke (Database)

## Project Description

This Flask application provides a robust school management system for the Ayar Yadanar Education Center. Key features include:

- **Role-based Access**: Secure login with distinct roles for students, administrators, and potentially other staff.
  
- **Course Management**: Admins can add, edit, suspend, and manage courses, subjects, and relevant schedules.
  
- **Student Enrollment**: Streamlined registration process for students to enroll in courses.
  
- **Invoice Generation**: Automated invoice creation for student fees, with clear payment deadlines. Students will get invoice based on the attended days. (If a student registers in the half of the month, we will only calculate half amount based on attended days).
  
- **Payment Tracking**: Records of payments for efficient tracking and reporting.
  
- **User Management**: Handles user registration, verification, approval, and suspension.

## Technologies

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Email**: Zoho SMTP Server
- **Other**: Flask-Migrate, SQLAlchemy, Flask-Login

## Installation and Setup

1 Clone the project
```
git clone https://github.com/aidankst/School_Management_Web_App.git
```

2 Create a virtual environment
```
python3 -m venv env
source env/bin/activate
```

3 Install necessary dependencies

4 Setup database:

- Create a PostgreSQL database
- Update DATABASE_URL in config.py or set as an environment variable.

5 Run database migrations
```
flask db init
flask db migrate
flask db upgrade
```

6 Run the application

## Example Usage

**Admin**:

- Create courses, and add subjects.
- Manage student registration and enrollment in courses.
- Generate and review invoices and payment history.
- Manage user accounts (approve, verify, suspend).
  
**Student**:

- Register for and enroll in courses.
- View invoices and payment status.
- Check personal information.
- Contribution

## Disclaimer

This project is intended for demonstration purposes.
