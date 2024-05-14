import os
import random
import string

from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__)

# Function to generate random HTML file name
def generate_file_name():
    characters = string.ascii_letters + string.digits
    file_name = ''.join(random.choice(characters) for _ in range(9)) + '.html'
    return file_name

# Function to log incorrect password attempts to Discord webhook

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tempaltes/users/ahmss')
def ahmss():
    return render_template('users/!rm-rf/ahmss.html')

# Route for submitting the form
@app.route('/submit', methods=['POST'])
def submit():
    # Define the correct password
    correct_password = "w"

    # Get form data
    html_code = request.form['htmlCode']
    user_id = request.form['userId']
    password = request.form['password']

    # Check if password is correct
    if password != correct_password:
        # Log incorrect password attempt (not implemented in this example)

        # Return error message
        return "Incorrect password", 400
    else:
        # Create 'users' directory if it doesn't exist
        users_dir = os.path.join('templates', 'users', 'ids')
        if not os.path.exists(users_dir):
            os.makedirs(users_dir)

        # Create user's directory if it doesn't exist
        user_dir = os.path.join(users_dir, user_id)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        # Generate random file name
        file_name = generate_file_name()

        # Write HTML code to the file
        file_path = os.path.join(user_dir, file_name)
        with open(file_path, 'w') as file:
            file.write(html_code)

        # Return the file name
        full_url = request.host_url + ('users/ids/' + user_id + '/' + file_name)
        return full_url

@app.route('/users/ids/<user_id>/<filename>')
def serve_file(user_id, filename):
    users_dir = os.path.join('templates', 'users', 'ids')
    return send_from_directory(os.path.join(users_dir, user_id), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
