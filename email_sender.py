import smtplib
from email.message import EmailMessage
import mimetypes
import os

def send_emails(sender, app_password, recipients, subject, body, attachment_path=None):
    success = 0
    failed = 0

    for email in recipients:
        try:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = email
            msg.set_content(body)

            # Attachment (optional)
            if attachment_path and os.path.exists(attachment_path):
                with open(attachment_path, 'rb') as f:
                    file_data = f.read()
                    mime_type, _ = mimetypes.guess_type(attachment_path)
                    main_type, sub_type = mime_type.split('/')
                    msg.add_attachment(file_data, maintype=main_type, subtype=sub_type, filename=os.path.basename(attachment_path))

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender, app_password)
                smtp.send_message(msg)

            success += 1
        except Exception as e:
            failed += 1

    return success, failed
