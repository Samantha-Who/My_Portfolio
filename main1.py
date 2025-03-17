from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText
from fastapi.middleware.cors import CORSMiddleware  # Import the middleware

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://samantha-who.github.io/My_Portfolio/", "http://127.0.0.1:5500", "http://localhost:5500"],  # Replace with your frontend domain
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Allow OPTIONS for preflight requests
    allow_headers=["*"],
)

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.post("/send_email")
async def send_email(form_data: ContactForm):
    print("Received data:", form_data)  # Add this line
    try:
        # Construct the email
        msg = MIMEText(f"Name: {form_data.name}\nEmail: {form_data.email}\n\n{form_data.message}")
        msg['Subject'] = 'Contact Form Submission'
        msg['From'] = 'your_email@gmail.com'  # Replace with your email
        msg['To'] = 'samantha.marian94@gmail.com'


import os

EMAIL_USER = os.getenv("EMAIL_USER")  # Store your email in environment variables
EMAIL_PASS = os.getenv("EMAIL_PASS")  # Store your email password in environment variables
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
