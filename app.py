import os
import random
import string

from flask import Flask, render_template, request, send_from_directory, render_template_string
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the model for storing HTML content
class HtmlContent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), nullable=False)
    file_name = db.Column(db.String(120), unique=True, nullable=False)
    html_code = db.Column(db.Text, nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Function to generate random HTML file name
def generate_file_name():
    characters = string.ascii_letters + string.digits
    file_name = ''.join(random.choice(characters) for _ in range(9)) + '.html'
    return file_name

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/templates/users/ahmss')
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
        return "Incorrect password", 400
    else:
        # Generate random file name
        file_name = generate_file_name()

        # Save HTML content to the database
        html_content = HtmlContent(user_id=user_id, file_name=file_name, html_code=html_code)
        db.session.add(html_content)
        db.session.commit()

        # Return the file URL
        full_url = request.host_url + 'view/' + file_name
        return full_url

# Route to serve HTML content
@app.route('/view/<file_name>')
def view_file(file_name):
    content = HtmlContent.query.filter_by(file_name=file_name).first_or_404()
    return render_template_string(content.html_code)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
