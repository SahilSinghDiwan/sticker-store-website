import os
from typing import Dict, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template

# Email configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
FROM_EMAIL = os.getenv('FROM_EMAIL', 'noreply@stickershop.com')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

# Email templates
WELCOME_EMAIL_TEMPLATE = """
<html>
<body>
    <h2>Welcome to Sticker Shop!</h2>
    <p>Hi {{ user.name }},</p>
    
    <p>Thank you for joining Sticker Shop! We're excited to have you as part of our community.</p>
    
    <p>With your account, you can:</p>
    <ul>
        <li>Browse our collection of unique stickers</li>
        <li>Save your favorite items</li>
        <li>Track your orders</li>
        <li>Get exclusive offers and updates</li>
    </ul>
    
    <p>Start shopping now by visiting our <a href="{{ frontend_url }}">store</a>!</p>
    
    <p>If you have any questions, feel free to reply to this email.</p>
    
    <p>Best regards,<br>Sticker Shop Team</p>
</body>
</html>
"""

PASSWORD_RESET_TEMPLATE = """
<html>
<body>
    <h2>Reset Your Password</h2>
    <p>Hi {{ user.name }},</p>
    
    <p>We received a request to reset your password. If you didn't make this request, you can safely ignore this email.</p>
    
    <p>To reset your password, click the link below (valid for 1 hour):</p>
    
    <p><a href="{{ frontend_url }}/reset-password?token={{ reset_token }}">Reset Password</a></p>
    
    <p>Or copy and paste this URL into your browser:</p>
    <p>{{ frontend_url }}/reset-password?token={{ reset_token }}</p>
    
    <p>For security reasons, this link will expire in 1 hour.</p>
    
    <p>If you didn't request this reset, please contact us immediately.</p>
    
    <p>Best regards,<br>Sticker Shop Team</p>
</body>
</html>
"""

ORDER_CONFIRMATION_TEMPLATE = """
<html>
<body>
    <h2>Order Confirmation - Order #{{ order._id }}</h2>
    <p>Thank you for your order!</p>
    
    <h3>Order Details:</h3>
    <ul>
    {% for item in order.items %}
        <li>{{ item.product_details.name }} - Quantity: {{ item.quantity }} - ${{ "%.2f"|format(item.price) }}</li>
    {% endfor %}
    </ul>
    
    <p><strong>Total:</strong> ${{ "%.2f"|format(order.total) }}</p>
    
    <h3>Shipping Address:</h3>
    <p>
    {{ order.shipping_address.street }}<br>
    {{ order.shipping_address.city }}, {{ order.shipping_address.state }} {{ order.shipping_address.zip }}<br>
    {{ order.shipping_address.country }}
    </p>
    
    <p>We'll notify you when your order ships.</p>
    
    <p>Best regards,<br>Sticker Shop Team</p>
</body>
</html>
"""

async def send_email(
    to_email: str,
    subject: str,
    html_content: str
) -> None:
    """Send an email using SMTP"""
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = FROM_EMAIL
        msg['To'] = to_email

        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)

    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise ValueError("Failed to send email")

async def send_welcome_email(user: Dict[str, Any]) -> None:
    """Send welcome email to new users"""
    if not user.get('email'):
        raise ValueError("User missing email")

    template = Template(WELCOME_EMAIL_TEMPLATE)
    html_content = template.render(
        user=user,
        frontend_url=FRONTEND_URL
    )

    await send_email(
        to_email=user['email'],
        subject="Welcome to Sticker Shop!",
        html_content=html_content
    )

async def send_password_reset_email(user: Dict[str, Any], reset_token: str) -> None:
    """Send password reset email"""
    if not user.get('email'):
        raise ValueError("User missing email")

    template = Template(PASSWORD_RESET_TEMPLATE)
    html_content = template.render(
        user=user,
        reset_token=reset_token,
        frontend_url=FRONTEND_URL
    )

    await send_email(
        to_email=user['email'],
        subject="Reset Your Password - Sticker Shop",
        html_content=html_content
    )

async def send_order_confirmation(order: Dict[str, Any]) -> None:
    """Send order confirmation email"""
    # Get user email from order
    user_email = order.get('user_email')
    if not user_email:
        raise ValueError("Order missing user email")

    # Render email template
    template = Template(ORDER_CONFIRMATION_TEMPLATE)
    html_content = template.render(order=order)

    # Send email
    await send_email(
        to_email=user_email,
        subject=f"Order Confirmation - Order #{order['_id']}",
        html_content=html_content
    ) 