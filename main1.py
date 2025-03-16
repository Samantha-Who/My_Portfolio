# app.py (your Flask backend)
from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    name = data['name']
    email = data['email']
    message = data['message']

    # Construct the email
    msg = MIMEText(f"Name: {name}\nEmail: {email}\n\n{message}")
    msg['Subject'] = 'Contact Form Submission'
    msg['From'] = 'your_email@gmail.com'  # Replace with your email
    msg['To'] = 'samantha.marian94@gmail.com'

    # Send the email (using SMTP)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('your_email@gmail.com', 'your_password') # Replace with your credentials
            server.send_message(msg)
        return jsonify({'message': 'Email sent successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main1__':
    app.run(debug=True)