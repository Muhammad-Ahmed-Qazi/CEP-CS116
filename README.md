### CEP-CS116
# AUTOHIRE – ONLINE CAR RENTAL SYSTEM
------------------------------------

This is a Python-Flask web application developed as part of our Object-Oriented Programming CEP project. It allows users to register, log in, view and reserve cars, manage rentals, and enables administrators to manage the fleet and generate reports.

--------------------
▶ HOW TO RUN
--------------------
1. Make sure you have Python 3.8+ installed.
2. Clone or download this project folder.
3. Install required packages:
   pip install -r requirements.txt

4. (Important) Install wkhtmltopdf for PDF generation:
   - Linux: sudo apt install wkhtmltopdf
   - Windows: https://wkhtmltopdf.org/downloads.html
   - Mac: brew install wkhtmltopdf

5. Run the app:
   python app.py

6. Open in browser: http://127.0.0.1:5000

--------------------
▶ TEST ACCOUNTS
--------------------
Admin:
  Email: admin@auto-hire.com
  Password: 123456

User:
  You can register a new user with any non-company email.

--------------------
▶ PROJECT STRUCTURE
--------------------
- app.py: Main Flask application
- /templates: HTML templates
- /static: CSS, JS, images
- /classes: Core app classes (User, Car, RentalSystem, etc.)
- /helpers: File handling and utilities
- requirements.txt: Required Python packages

--------------------
▶ NOTES
--------------------
- All data is stored in JSON files.
- Only users with @auto-hire.com domain can register as admins.
- Balance is deducted upon reservation and updated on early/late return.
- Flash alerts are used to notify users of system events and issues.

--------------------
▶ CONTRIBUTED BY
--------------------
- Muhammad Ahmed Qazi (Lead Developer)
- Mujtaba Jawaid Rao
- Muhammad Zain Rizvi
