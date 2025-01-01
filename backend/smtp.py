import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException

EMAIL_USER = ""
EMAIL_PASSWORD = ""
EMAIL_SERVER = "smtp.gmail.com"
EMAIL_PORT = 587


class EmailService:
    def __init__(
        self,
        smtp_user,
        smtp_password,
        smtp_server,
        smtp_port,
    ):
        """DocString"""
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    def send_email(self, receiver, body, subject=None):
        try:
            message = MIMEMultipart()
            message["From"] = self.smtp_user
            message["To"] = receiver
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                text = message.as_string()

                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_user, receiver, text)

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=500,
                detail="Failed to send email",
            )


smtp_service = EmailService(
    smtp_user=EMAIL_USER,
    smtp_password=EMAIL_PASSWORD,
    smtp_server=EMAIL_SERVER,
    smtp_port=EMAIL_PORT,
)
