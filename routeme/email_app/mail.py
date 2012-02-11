from models import Registration
from django.core.mail import EmailMultiAlternatives
import hashlib
from routeme import settings 

def compute_hash(key):
    m = hashlib.md5() 
    m.update(key)
    return m.hexdigest()

def send_activation_mail(user):
    hash = compute_hash(user.username + user.email)
    reg = Registration.objects.create(user = user, activation_key = hash)
    
    subject, from_email, to = 'Activation Mail', settings.EMAIL_HOST_USER, user.email
    text_content = "Routeme"
    html_content = '<a href="http://127.0.0.1:8000/email/activate/'+ hash +'>Click Here to Activete'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return True
    
