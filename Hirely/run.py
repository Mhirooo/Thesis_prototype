from app import create_app  # Import your factory function from app/__init__.py
from flask import Flask, render_template, request, redirect
import os

# Create the Flask app instance
app = create_app()

from flask import render_template

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/create-first-admin')
def create_first_admin_page():
    return render_template('create_first_admin.html')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # TODO: Validate against database here
        # For now, just redirect to /apply
        return redirect('/apply')
    return render_template('login.html')


if __name__ == '__main__':
    # Print all routes for debugging
    with app.app_context():
        print("\n=== Registered Routes ===")
        for rule in app.url_map.iter_rules():
            print(f"{rule.endpoint:30s} -> {rule}")

    # Ensure upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Run Flask server
    app.run(debug=True, host='0.0.0.0', port=5000)
