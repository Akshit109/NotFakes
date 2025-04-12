# Deepfake Detection Web App — API Documentation

Welcome to the API documentation for the **Deepfake Detection Web App**. This web service allows users to sign up, log in, and upload video files to detect possible deepfake manipulations using basic blur artifact analysis.

This documentation is structured to help developers integrate and use the backend API effectively. Each route is explained with request types, expected data, and response examples in JSON or HTML format.

***

## 🌍 Base URL

```
http://localhost:5000/
```

All routes mentioned below are based on this default development URL. Change it accordingly if deployed in production.

***

## 📑 Endpoints Overview

| Method | Endpoint             | Description                                      |
| ------ | -------------------- | ------------------------------------------------ |
| GET    | `/`                  | Renders the login page                           |
| POST   | `/login`             | Authenticates a user and starts a session        |
| GET    | `/signup`            | Renders the signup page                          |
| POST   | `/signup`            | Registers a new user                             |
| GET    | `/home`              | Renders user home/dashboard (after login)        |
| POST   | `/upload`            | Uploads a video for deepfake analysis            |
| GET    | `/logout`            | Logs the user out and ends the session           |
| GET    | `/ststic/<filename>` | Serves static files from the `ststic/` directory |

***

📌 Expected Difference (based on research and experiments):

Type Avg Blue Intensity

Real \~110–130

Deepfake \~90–110

📉 Deepfakes often show lower blue levels and less blue contrast overall, especially in areas where the fake face is blended.

## 📝 Signup - `POST /signup`

Registers a new user with Gmail-only email validation.

### Request (form-data)

```json
{
  "username": "preeti",
  "email": "preeti@gmail.com",
  "password": "SecurePassword"
}
```

### Success Response (HTML - `signup_success.html`)

```html
<h3>Signup successful, welcome preeti!</h3>
```

### Failure Response (HTML - `signup_error.html`)

```html
<h3>Only Gmail addresses are allowed!</h3>
```

or

```html
<h3>Username or Gmail already exists!</h3>
```

***

## 🔐 Login - `POST /login`

Authenticates the user and stores a session.

### Request (form-data)

```json
{
  "username": "preeti",
  "password": "SecurePassword"
}
```

### Success

* Redirects to `/home`.

### Failure (HTML - `login_error.html`)

```html
<h3>Invalid credentials</h3>
```

***

## 🏠 Home - `GET /home`

Displays the dashboard after a successful login.

* 🔒 Requires user session (`session['user']`).
* Redirects to `/` if not logged in.

***

## 📤 Upload Video - `POST /upload`

Allows the user to upload a video file for blur-based deepfake detection.

### Request (multipart/form-data)

| Field | Type   | Description            |
| ----- | ------ | ---------------------- |
| video | `file` | The video file to test |

### Response (HTML - `result.html`)

```html
🛑 Deepfake Detected!
```

or

```html
✅ Video Looks Real.
```

***

## 🚪 Logout - `GET /logout`

Logs out the current user by clearing the session.

### Response

* Redirects to `/`.

***

## 🗂️ Serve Static Files - `GET /ststic/<filename>`

Serves CSS, JS, images, etc., from the `ststic/` directory.

> ⚠️ You have a typo in the folder name (`ststic` instead of `static`). Either fix it or document it properly for consistency.

***

Let me know when you're ready, and I’ll proceed with a **detailed security audit** covering:

* 🔐 Session management
* 🛡️ SQL injection
* 🗂️ File upload validation
* ❌ XSS and CSRF
* 📁 Directory traversal
* 🔄 Misc recommendations

Would you like me to start the **security audit** now?
