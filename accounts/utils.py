import random
import string
from django.conf import settings
from django.urls import reverse
from django.core.mail import EmailMessage
import smtplib
def code_slug_generator(size=12, chars=string.ascii_letters):
    """
    Generates a random code of characters.

    Arguments:
    size -- The length of the generated code (default 12).
    chars -- The collection of characters from which the code is generated (default is all letters).

    Returns:
    A random string of length `size`, composed of characters chosen from `chars`.
    """
    return ''.join(random.choice(chars) for _ in range(size))

def create_slug_shortcode(size, model_):
    """
    Creates a unique slug for a model by checking that it does not already exist in the database.

    Arguments:
    size -- The length of the slug to generate.
    model_ -- The Django model for which the slug is generated.

    Returns:
    A unique slug for the model.
    """
    new_code = code_slug_generator(size=size)
    qs_exists = model_.objects.filter(slug=new_code).exists()
    if qs_exists:
        return create_slug_shortcode(size, model_)
    return new_code

def generate_code(size=6, chars=string.digits):
    """
    Generates a random numeric code.

    Arguments:
    size -- The length of the code (default 6).
    chars -- The characters from which the code is generated (default is digits only).

    Returns:
    A random string of digits of length `size`.
    """
    return ''.join(random.choice(chars) for _ in range(size))

def create_activation_code(model_, size=6):
    """
    Creates a unique activation code for a model.

    Arguments:
    model_ -- The model for which the activation code is generated.
    size -- The length of the code (default 6).

    Returns:
    A unique activation code for the model.
    """
    code = generate_code(size)
    if model_.objects.filter(activation_code=code).exists():
        return create_activation_code(size)
    return code

# def send_email(to_email, token, domain, email_type="register"):
#     """
#     Sends an email with a given token and type.

#     Arguments:
#     to_email -- The recipient's email address.
#     token -- The token to include in the email.
#     domain -- The domain to prepend to the activation link.
#     email_type -- The type of email to send (default is "register").

#     This function generates the activation link and sends an email with the appropriate content.
#     """
#     activation_link = reverse('accounts:activate', args=[token])
#     print(activation_link)
#     if email_type == "register":
#         title = 'Activate Your Account'
#         content = f'Click the following link to activate your account: {domain}{activation_link}'
#     elif email_type == "forgot_pass":
#         title = 'Reset your password'
#         content = f'Click the following link to reset your password: {domain}{activation_link}'
#     print(content,to_email)  
#     with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as connection:
#             connection.starttls()
#             connection.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
#             connection.sendmail(settings.EMAIL_HOST_USER, to_email, f"Subject: {title}\n\n{content}")

def send_activation_email(to_email, token, domain, email_type="register"):
    """
    Sends an email with a given token and type.

    Arguments:
    to_email -- The recipient's email address.
    token -- The token to include in the email.
    domain -- The domain to prepend to the activation link.
    email_type -- The type of email to send (default is "register").

    This function generates the activation link and sends an email with the appropriate content.
    """
    activation_link = f"http://{domain}/accounts/activate/{token}/"
    print(activation_link)
    
    if email_type == "register":
        title = 'Activate Your Account'
        content = f'Click the following link to activate your account: {activation_link}'
    elif email_type == "forgot_pass":
        title = 'Reset your password'
        content = f'Click the following link to reset your password: {activation_link}'
    
    # For local development, the email will be captured by the console backend.
    print(content, to_email)
    
    # The email sending code using Django's email functionality.
    
    email = EmailMessage(
        subject=title,
        body=content,
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email]
    )
    email.send()
