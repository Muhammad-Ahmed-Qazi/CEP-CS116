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
                    window.location.href = '/';
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
        }).catch(err => {
            console.error('Error:', err);
        });
    // });
}

function register() {
    const form = document.getElementById('registerForm');

    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const name = document.getElementById('nameInp').value.trim();
    const email = document.getElementById('emailInp').value.trim();
    const newPassword = document.getElementById('newPasswordInp').value;
    const confirmPassword = document.getElementById('confirmPasswordInp').value;
    const role = document.getElementById('role').value;

    if (newPassword !== confirmPassword) {
        document.getElementById('confirmPasswordInp').classList.add("border", "border-danger");
        document.getElementById('invalidConfirmPassword').innerText = 'Passwords do not match';
        return;
    }

    document.getElementById('confirmPasswordInp').classList.remove("border", "border-danger");
    document.getElementById('invalidConfirmPassword').innerText = '';

    // Common to both roles
    const profileImageURL = document.getElementById('profileImageInp').value.trim();

    let userData = {
        name: name,
        email: email,
        password: newPassword,
        role: role,
        profile_image_url: profileImageURL
    };

    // Add extra user fields
    if (role === 'user') {
        userData.balance = document.getElementById('balanceInp').value;
        userData.license_number = document.getElementById('licenseNumberInp').value.trim();
        userData.license_expiry = document.getElementById('licenseExpiryInp').value;
    }

    fetch('/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                window.location.href = '/';  // redirect to login or home
            } else {
                document.getElementById('emailInp').classList.add("border", "border-danger");
                document.getElementById('invalidEmail').innerText = data.message;
            }
        });
}


function toggleCarFields(type) {
    document.getElementById("economy-fields").classList.add("d-none");
    document.getElementById("luxury-fields").classList.add("d-none");
    document.getElementById("commercial-fields").classList.add("d-none");

    if (type === "EconomyCar") {
        document.getElementById("economy-fields").classList.remove("d-none");
    } else if (type === "LuxuryCar") {
        document.getElementById("luxury-fields").classList.remove("d-none");
    } else if (type === "CommercialCar") {
        document.getElementById("commercial-fields").classList.remove("d-none");
    }
}

function handleEditButtonClick(button) {
    const car = JSON.parse(button.dataset.car);
    openEditCarModal(car); // your existing function
}

function openEditCarModal(car) {

    // Set modal fields
    document.getElementById("vin").value = car.vin;
    document.getElementById("model").value = car.model;
    document.getElementById("base_rate").value = car.base_rate;
    document.getElementById("img_url").value = car.img_url;
    document.getElementById("seating_capacity").value = car.seating_capacity;
    document.getElementById("colour").value = car.colour;
    document.getElementById("car_type").value = car.car_type;

    // Disable VIN input
    document.getElementById("vin").disabled = true;

    // Set features
    for (const [feature, value] of Object.entries(car.features)) {
        const checkbox = document.getElementById(feature);
        if (checkbox) checkbox.checked = value;
    }

    // Toggle category-specific fields
    toggleCarFields(car.car_type);
    if (car.car_type === "EconomyCar") {
        document.getElementById("fuel_efficiency").value = car.fuel_efficiency;
    } else if (car.car_type === "LuxuryCar") {
        document.getElementById("chauffeur_available").value = car.chauffeur_available ? "1" : "0";
    } else if (car.car_type === "CommercialCar") {
        document.getElementById("cargo_capacity").value = car.cargo_capacity;
    }

    // Update form action for editing
    document.querySelector("#carForm").action = `/admin/edit_car/${car.vin}`;

    // Set modal title
    document.getElementById("carModalLabel").innerText = "Edit Car";

    // Show the modal
    const modal = new bootstrap.Modal(document.getElementById('addCarModal'));
    modal.show();
    console.log(car);
}

function openAddCarModal() {
    // Clear all form fields
    document.getElementById("carForm").reset();

    // Re-enable VIN field
    const vinInput = document.getElementById("vin");
    vinInput.disabled = false;
    vinInput.value = "";

    // Reset all feature checkboxes
    const features = ["air_conditioning", "bluetooth", "gps", "usb_ports", "sunroof", "rear_camera"];
    features.forEach(f => {
        const cb = document.getElementById(f);
        if (cb) cb.checked = false;
    });

    // Hide category-specific fields
    toggleCarFields(""); // or manually hide all

    // Clear and reset category-specific inputs
    document.getElementById("fuel_efficiency").value = "";
    document.getElementById("chauffeur_available").value = "0";
    document.getElementById("cargo_capacity").value = "";

    // Set form action to add route
    document.getElementById("carForm").action = "/admin/add_car";

    document.getElementById("carModalLabel").innerText = "Add New Car";

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('addCarModal'));
    modal.show();
}

function openCarModal(car, start, end) {
    // Populate modal content
    document.getElementById('modalImg').src = car.img_url;
    document.getElementById('modalModel').innerText = car.model;
    document.getElementById('modalType').innerText = car.category.replace('Car', '');
    document.getElementById('modalVin').innerText = car.vin;
    document.getElementById('modalColour').innerText = car.colour;
    document.getElementById('modalSeats').innerText = car.seating_capacity;
    document.getElementById('modalRate').innerText = `${car.base_rate} PKR`;

    // Extra spec
    let extra = '';
    if (car.category === "EconomyCar") {
        extra = `<p class="mb-1 text-muted small">Fuel Efficiency:</p><p class="fw-semibold">${car.fuel_efficiency} km/l</p>`;
    } else if (car.category === "LuxuryCar") {
        extra = `<p class="mb-1 text-muted small">Chauffeur Available:</p><p class="fw-semibold">${car.chauffeur_available ? 'Yes' : 'No'}</p>`;
    } else if (car.category === "CommercialCar") {
        extra = `<p class="mb-1 text-muted small">Cargo Capacity:</p><p class="fw-semibold">${car.cargo_capacity} kg</p>`;
    }
    document.getElementById('modalExtraSpec').innerHTML = extra;

    // Features
    const featuresContainer = document.getElementById('modalFeatures');
    featuresContainer.innerHTML = '';
    for (const [feature, value] of Object.entries(car.features)) {
        const badge = document.createElement('span');
        badge.className = `badge ${value ? 'bg-success' : 'bg-secondary'}`;
        badge.innerText = feature.replace('_', ' ').toUpperCase();
        featuresContainer.appendChild(badge);
    }

    // Set Reserve Button Link
    const reserveUrl = `/reserve/${car.vin}?start=${start}&end=${end}`;
    document.getElementById('modalReserveBtn').href = reserveUrl;

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('carDetailsModal'));
    modal.show();
}