from fastapi import FastAPI, HTTPException, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import smtplib
from email.mime.text import MIMEText

app = FastAPI()

class ContactForm(BaseModel):
    name: str
    email: str
    message: str

@app.post("/send_email")
async def send_email(form_data: ContactForm):
    try:
        # Construct the email
        msg = MIMEText(f"Name: {form_data.name}\nEmail: {form_data.email}\n\n{form_data.message}")
        msg['Subject'] = 'Contact Form Submission'
        msg['From'] = 'your_email@gmail.com'  # Replace with your email
        msg['To'] = 'samantha.marian94@gmail.com'

        # Send the email (using SMTP)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login('samantha.marian94@gmail.com', 'Iloveyou33!')  # Replace with your credentials
            server.send_message(msg)

        return JSONResponse(content={"message": "Email sent successfully!"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
