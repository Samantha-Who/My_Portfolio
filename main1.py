import os
import logging
import smtplib
from email.mime.text import MIMEText
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://samantha-who.github.io/", 
        "http://127.0.0.1:5500", 
        "http://localhost:5500"
    ],  # Allowed frontend URLs
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],  # Allow OPTIONS for CORS preflight
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Contact form data model
class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.post("/send_email")
async def send_email(form_data: ContactForm):
    logger.info(f"Received contact form submission: {form_data}")

    # Fetch email credentials once
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    RECIPIENT_EMAIL = "samantha.marian94@gmail.com"

    if not EMAIL_USER or not EMAIL_PASS:
        logger.error("Email credentials are not set in environment variables.")
        raise HTTPException(status_code=500, detail="Email credentials are not set")

    # Construct the email
    email_body = f"""
    Name: {form_data.name}
    Email: {form_data.email}

    Message:
    {form_data.message}
    """
    msg = MIMEText(email_body.strip())  # Strip removes unnecessary new lines
    msg["Subject"] = "Contact Form Submission"
    msg["From"] = EMAIL_USER
    msg["To"] = RECIPIENT_EMAIL

    try:
        # Send email using SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)

        logger.info("Email sent successfully!")
        return JSONResponse(content={"message": "Email sent successfully!"})

    except smtplib.SMTPException as smtp_error:
        logger.error(f"SMTP error: {smtp_error}")
        raise HTTPException(status_code=500, detail="Failed to send email due to SMTP error.")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while sending the email.")
