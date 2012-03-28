from models import Registration
from django.core.mail import EmailMessage,EmailMessage, EmailMultiAlternatives
import hashlib
from routeme import settings 

def send_activation_mail(user):
    
    subject, from_email, to = 'Activation Mail', settings.EMAIL_HOST_USER, user.email
    text_content = "Routeme"
    html_content = '<a href="http://www.drivefor.me/email/activate/'+ user.registration.activation_key +'>Click Here to Activete</a>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return True
    
