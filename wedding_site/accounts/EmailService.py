
import smtplib
import ssl
import random
from email.message import EmailMessage
from farshiPoject import settings

class EmailService():
    @staticmethod
    def send_reset_link(receiver_email, link):
        sender_email = settings.ORGANIZATION_EMAIL
        app_password = settings.EMAIL_PASSWORD
        
        msg = EmailMessage()
        msg['Subject'] = "Password Reset Request"
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.set_content(f"Click the link below to reset your password:\n{link}")

        context = ssl.create_default_context()
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, app_password)
                server.send_message(msg)
            return True
        except Exception as e:
            print(f"SMTP Error: {e}")
            return False



















# import smtplib
# import ssl
# import random
# from email.message import EmailMessage
# from farshiPoject import settings

# class EmailService():

#     def send_otp_via_email(receiver_email,otp):
#         # 1. Setup credentials
#         sender_email = settings.ORGANIZATION_EMAIL
#         app_password = settings.EMAIL_PASSWORD
#         msg = EmailMessage()
#         msg['Subject'] = "Your Verification Code"
#         msg['From'] = sender_email
#         msg['To'] = receiver_email
#         msg.set_content(f"Your OTP for verification is: {otp}. It expires in 5 minutes.")


#         context = ssl.create_default_context()
        
#         try:
#             with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
#                 server.login(sender_email, app_password)
#                 server.send_message(msg)
#             return otp  
#         except Exception as e:
#             print(f"Error sending email: {e}")
#             return None