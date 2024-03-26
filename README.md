# Password Management System (PMS)

Password Management System is an open-source password manager that allows you to store your passwords securely. It is a
simple and easy-to-use tool that helps you keep your passwords safe and organized.

## Features
* Multi-tenant.
* Personal and shared passwords.
* Different encryption keys for each tenant.

## Installation
1. Clone the repository.
```bash
git clone git@github.com:elkhayyat/PasswordManagementSystem.git
```
2. Create a virtual environment.
```bash
python -m venv venv
```
3. Install the dependencies.
```bash
pip install -r requirements.txt
```
4. Copy the `.env.example` file to `.env` and update the values.
```bash
cp .env.example .env
```
5. Run the migrations.
```bash
python manage.py migrate
```
6. Create a superuser.
```bash
python manage.py createsuperuser
```
7. Run the application.
```bash
python manage.py runserver
```
8. Open the browser and navigate to `http://127.0.0.1:8000`.
