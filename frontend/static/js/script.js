// scripts.js

// Register Form Submission
document.getElementById('registerForm').addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent form from refreshing the page

    const data = {
        username: document.getElementById('username').value,
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
        confirmPassword: document.getElementById('confirmPassword').value,
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/api/register/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const result = await response.json();
        if (response.ok) {
            alert('Registration successful! Please login.');
            window.location.href = 'login.html';
        } else {
            alert(result.detail || 'Registration failed!');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

// Login Form Submission
document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const data = {
        email: document.getElementById('email').value,
        password: document.getElementById('password').value,
    };

    try {
        const response = await fetch('http://127.0.0.1:8000/api/login/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        const result = await response.json();
        if (response.ok) {
            alert('Login successful!');
            // Store the token or redirect as needed
        } else {
            alert(result.detail || 'Login failed!');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
