import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.leaflogic.logger import logging
from src.leaflogic.exception import CustomException
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class SendReport2Email:
    @staticmethod
    def send_email_via_smtp(email, subject, body):
        """
        Sends an email using SMTP.

        Args:
            email (str): The recipient's email address.
            subject (str): The subject of the email.
            body (str): The body/content of the email.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        try:
            # SMTP server configuration for Gmail
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = os.getenv("SENDER_EMAIL")  # Use environment variable
            sender_password = os.getenv("SENDER_PASSWORD")  # Use environment variable

            # Validate sender email and password
            if not sender_email or not sender_password:
                logging.error("Sender email or password not found in environment variables.")
                return False

            # Create the email
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = email
            msg['Subject'] = subject

            # Attach the body to the email
            msg.attach(MIMEText(body, 'plain'))

            # Connect to the SMTP server
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Upgrade the connection to secure
                server.login(sender_email, sender_password)  # Log in to the SMTP server
                server.sendmail(sender_email, email, msg.as_string())  # Send the email

            logging.info(f"Email sent successfully to {email}.")
            return True
        except Exception as e:
            logging.exception(f"Error sending email to {email}: {str(e)}")  # Log full traceback
            return False