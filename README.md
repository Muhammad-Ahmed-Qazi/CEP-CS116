# AutoHire: Online Car Rental System

AutoHire is a Python + Flask-based web application that allows users to search, reserve, and manage car rentals with a clean user interface. Admins can manage the fleet, view customer activity, and generate reports.

---

## 📁 Project Structure

```bash
AutoHire/
│
├── app.py                  # Main Flask application
├── requirements.txt        # Required libraries
├── static/                 # CSS, JS, image files
│   ├── css/
│   ├── js/
│   └── images/
├── templates/              # HTML templates
│   ├── components/         # Shared template components
│   └── ...
├── classes/                # Python class files (Car, User, Fleet, etc.)
├── helpers/                # File handling and utilities
└── data/                   # JSON data files (users, reservations, cars)
```

---

## 🚀 Getting Started

### Installation

```bash
pip install -r requirements.txt
```

Make sure you have Python 3.9+ installed.

### Running the App

```bash
python app.py
```

* Visit `http://localhost:5000` in your browser.
* Please ensure a stable internet connection for the receipt generation upon car reservation to function. The `wkhtmltopdf` module requires an internet connection.

---

## 🛠 Features

* User authentication and profile management
* Fleet management (Add/Edit/Delete cars)
* Booking cars with availability filtering
* Reservation receipts (PDF)
* Admin dashboard with downloadable reports
* Flash messaging system for user feedback

---

## 👥 Roles

### User

* Can register, login, and book cars
* Can return cars and view booking history

### Admin

* Can add/edit/delete cars
* Can view reports of current rentals and reserved cars
* Cannot make reservations

---

## ✅ Requirements

The project requires:

* Python 3.9+
* Flask
* pdfkit
* wkhtmltopdf (for generating PDFs)

Install via `pip install -r requirements.txt`.

---

## 🔧 Troubleshooting

### 1. `wkhtmltopdf` Errors on PDF Receipt Generation (Windows)

The app uses `pdfkit` and `wkhtmltopdf` to generate reservation receipts in PDF format. If you're on Windows and encounter an error like:

```
OSError: No wkhtmltopdf executable found
```

✅ **Fix it by following these steps:**

1. **Download and Install `wkhtmltopdf`**:

   * Visit: [https://wkhtmltopdf.org/downloads.html](https://wkhtmltopdf.org/downloads.html)
   * Download the **Windows (MSI) Installer**.
   * During installation, allow it to add `wkhtmltopdf` to your system PATH (check the box when prompted).

2. **If PATH is not set automatically**:

   * Manually locate the `wkhtmltopdf.exe` file (usually found in `C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe`).
   * Add that path to your system’s **Environment Variables**:

     * Open Start → search "Environment Variables"
     * Edit **System Variables** → double-click `Path` → click **New** and paste the full directory path.

3. **Test it**:

   * Open Command Prompt and type: `wkhtmltopdf --version`
   * If it returns a version, it is correctly installed.

4. **Still not working in Flask?**
   Modify your app’s code to explicitly point to the executable:

   ```python
   import pdfkit
   config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
   pdf = pdfkit.from_string(html_string, False, configuration=config)
   ```

---

## 🧪 Testing

Make sure to:

* Register as a user and make a reservation
* Download receipt
* Attempt login as admin
* Add/remove/edit cars
* Generate and download reports

---

## 📄 License

This project is built for academic submission purposes only.

---

## 🤝 Contributors

* Muhammad Ahmed Qazi
* Mujtaba
* Zain

---
