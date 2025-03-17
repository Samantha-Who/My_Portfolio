import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://samantha-who.github.io/My_Portfolio/", "http://127.0.0.1:5500", "http://localhost:5500"],  # Your frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Allow OPTIONS for CORS preflight
    allow_headers=["*"],
)

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.post("/send_email")
async def send_email(form_data: ContactForm):
    print("Received data:", form_data)

    try:
        # Construct the email
        msg = MIMEText(f"Name: {form_data.name}\nEmail: {form_data.email}\n\n{form_data.message}")
        msg['Subject'] = 'Contact Form Submission'
        msg['From'] = os.getenv("EMAIL_USER")  # Environment variable
        msg['To'] = 'samantha.marian94@gmail.com'

        # Get email credentials from environment variables
        EMAIL_USER = os.getenv("EMAIL_USER")
        EMAIL_PASS = os.getenv("EMAIL_PASS")

        if not EMAIL_USER or not EMAIL_PASS:
            raise HTTPException(status_code=500, detail="Email credentials are not set")

        # Send email using SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        return JSONResponse(content={"message": "Email sent successfully!"})

    except Exception as e:
        print("Error:", e)  # Print error for debugging
        raise HTTPException(status_code=500, detail=str(e))
