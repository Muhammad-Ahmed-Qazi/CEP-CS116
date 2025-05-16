// Login Form Validation and Submission
function login() {
    // document.getElementById('loginForm').addEventListener('submit', function (e) {
    //     e.preventDefault();  // prevent traditional submission

        const form = document.getElementById('loginForm');

        if (!form.checkValidity()) {
            form.reportValidity();  // Show browser's validation popup
            return;  // Stop if form is invalid
        }

        const email = document.getElementById('emailInp').value.trim();
        const password = document.getElementById('passwordInp').value;

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email: email, password: password })
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    if (data.isAdmin) {
                        window.location.href = '/dashboard';
                    } else {
                        window.location.href = '/'
                    }
                } else {
                    console.log(data)
                    if (data.error == 'email') {

                        document.getElementById('passwordInp').classList.remove("border", "border-danger")
                        document.getElementById('invalidPassword').innerText = ''
                        document.getElementById('emailInp').classList.add("border", "border-danger")
                        document.getElementById('invalidEmail').innerText = data.message
                    } else {
                        document.getElementById('emailInp').classList.remove("border", "border-danger")
                        document.getElementById('invalidEmail').innerText = ''
                        document.getElementById('passwordInp').classList.add("border", "border-danger")
                        document.getElementById('invalidPassword').innerText = data.message
                    }
                }
            });
    // });
}

// Registration Form Validation and Submission
function register() {
    // document.getElementById('registerForm').addEventListener('submit', function (e) {
    //     e.preventDefault();  // prevent traditional submission

        const form = document.getElementById('registerForm');
        console.log("Getting!")

        if (!form.checkValidity()) {
            form.reportValidity();  // Show browser's validation popup
            return;  // Stop if form is invalid
        }

        const name = document.getElementById('nameInp').value.trim();
        const email = document.getElementById('emailInp').value.trim();
        const newPassword = document.getElementById('newPasswordInp').value;
        const confirmPassword = document.getElementById('confirmPasswordInp').value;

        if (newPassword !== confirmPassword) {
            document.getElementById('confirmPasswordInp').classList.add("border", "border-danger");
            document.getElementById('invalidConfirmPassword').innerText = 'Passwords do not match';
            return;
        }
        document.getElementById('confirmPasswordInp').classList.remove("border", "border-danger");
        document.getElementById('invalidConfirmPassword').innerText = '';

        // Check role
        const role = document.getElementById('role').value;
        if (role == 'user') {
            var balance = document.getElementById('balanceInp').value;
        } else {
            var balance = 0;
        }

        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: name, email: email, password: newPassword, role: role, balance: balance })
        })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    console.log(data);
                    window.location.href = '/'; //login
                } else {
                    console.log(data);
                    document.getElementById('emailInp').classList.add("border", "border-danger");
                    document.getElementById('invalidEmail').innerText = data.message;
                }
            });
    // });
}