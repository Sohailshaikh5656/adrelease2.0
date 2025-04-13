from django.core.mail import send_mail
from datetime import datetime  # This imports the datetime class directly
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from datetime import datetime




WELCOME_EMAIL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 0;
        }}
        .header-bar {{
            background-color: #D2B48C;
            padding: 20px;
            text-align: center;
            color: white;
            font-size: 24px;
            font-weight: bold;
        }}
        .content {{
            padding: 20px;
            background-color: #f9f9f9;
        }}
        .footer {{
            padding: 15px;
            text-align: center;
            font-size: 12px;
            color: #777;
            background-color: #eee;
        }}
        .button {{
            display: inline-block;
            padding: 10px 20px;
            background-color: #D2B48C;
            color: white !important;
            text-decoration: none;
            border-radius: 4px;
            margin: 15px 0;
            font-weight: bold;
        }}
        .user-info {{
            background: white;
            padding: 15px;
            border-radius: 4px;
            margin: 15px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
    </style>
</head>
<body>
    <div class="header-bar">
        Welcome to Our Community!
    </div>
    <div class="content">
        <h2>Hello {first_name}!</h2>
        <p>We're thrilled to have you join us. Here's your account information:</p>
        
        <div class="user-info">
            <p><strong>Username:</strong> {username}</p>
            <p><strong>Email:</strong> {email}</p>
        </div>
        
        <p>To get started, you can:</p>
        <a href="{login_url}" class="button">Login to Your Account</a>
        
        <p>If you have any questions, don't hesitate to contact our support team.</p>
    </div>
    <div class="footer">
        &copy; {current_year} Your Company Name. All rights reserved.<br>
        <a href="{unsubscribe_url}" style="color: #777;">Unsubscribe</a>
    </div>
</body>
</html>
"""
ORDER_APPROVAL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            background-color: #f8f9fa;
        }}
        .header-bar {{
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            padding: 30px;
            text-align: center;
            font-size: 24px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .content {{
            padding: 30px;
            max-width: 600px;
            margin: 20px auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        .footer {{
            padding: 20px;
            text-align: center;
            font-size: 12px;
            color: #777;
            background-color: #f1f3f5;
            margin-top: 30px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 30px;
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white !important;
            text-decoration: none;
            border-radius: 25px;
            margin: 20px 0;
            font-weight: bold;
            transition: all 0.3s ease;
        }}
        .button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }}
        .order-info {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            border-left: 4px solid #4CAF50;
        }}
        .order-info p {{
            margin: 8px 0;
            color: #444;
        }}
        .order-info strong {{
            color: #333;
        }}
        h2 {{
            color: #2c3e50;
            margin-bottom: 20px;
        }}
        p {{
            color: #555;
        }}
    </style>
</head>
<body>
    <div class="header-bar">
        🎉 Your Advertisement Has Been Approved!
    </div>
    <div class="content">
        <h2>Hello {first_name},</h2>
        <p>We're excited to let you know that your advertisement has been successfully approved and is now live on our platform!</p>
        
        <div class="order-info">
            <p><strong>Advertisement Title:</strong> {ad_title}</p>
            <p><strong>Order ID:</strong> #{order_id}</p>
            <p><strong>Approval Date:</strong> {approval_date}</p>
            <p><strong>News Agency:</strong> {agency}</p>
            <p><strong>Agency Email:</strong> {agency_email}</p>
        </div>
        
        <p>You can now view your live advertisement:</p>
        <a href="{ad_url}" class="button">View My Advertisement</a>
        
        <p style="margin-top: 20px;">If you have any questions or need assistance, our support team is always here to help.</p>
    </div>
    <div class="footer">
        &copy; {current_year} Your Company Name. All rights reserved.<br>
        <a href="{unsubscribe_url}" style="color: #777; text-decoration: none;">Unsubscribe</a>
    </div>
</body>
</html>
"""

def send_order_approval_email(user, order,agency):
    subject = f"🎉 Congratulations! Your Ad is Approved - Order #{order.id}"
    
    # Prepare context variables
    context = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'order_id': order.id,
        'order_date': order.order_date.strftime('%B %d, %Y') if order.order_date else 'N/A',
        'ad_title': order.subject,
        'ad_description': order.description,
        'approval_date': datetime.now().strftime('%B %d, %Y %I:%M %p'),
        'current_year': datetime.now().year,
        'agency' : agency.username,
        'agency_email' : agency.email,
        'ad_url': f"https://yourdomain.com/ads/{order.id}",
        'unsubscribe_url': 'https://yourdomain.com/unsubscribe'
    }
    
    # Create HTML content
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .header {{ background: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .order-details {{ background: #f5f5f5; padding: 20px; border-radius: 5px; margin: 20px 0; }}
            .button {{ 
                display: inline-block; 
                background: #4CAF50; 
                color: white; 
                padding: 10px 20px; 
                text-decoration: none; 
                border-radius: 5px; 
                margin: 20px 0;
            }}
            .footer {{ 
                margin-top: 30px; 
                padding-top: 20px; 
                border-top: 1px solid #eee; 
                color: #666; 
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Your Ad is Live!</h1>
        </div>
        <div class="content">
            <h2>Hi {context['first_name']} {context['last_name']},</h2>
            <p>We're excited to let you know that your advertisement has been approved and is now live on our platform!</p>
            
            <div class="order-details">
                <h3>Order Details</h3>
                <p><strong>Order ID:</strong> #{context['order_id']}</p>
                <p><strong>Ad Title:</strong> {context['ad_title']}</p>
                <p><strong>Description:</strong> {context['ad_description']}</p>
                <p><strong>Order Date:</strong> {context['order_date']}</p>
                <p><strong>Approval Date:</strong> {context['approval_date']}</p>
            </div>
            
            <a href="{context['ad_url']}" class="button">View Your Ad</a>
            
            <p>If you have any questions or need assistance, our support team is here to help!</p>
        </div>
        <div class="footer">
            &copy; {context['current_year']} Your Company Name. All rights reserved.<br>
            <a href="{context['unsubscribe_url']}">Unsubscribe</a>
        </div>
    </body>
    </html>
    """
    
    # Create plain text version
    text_content = f"""
    Hi {user.first_name} {user.last_name},

    We're excited to let you know that your advertisement has been approved!

    Order Details:
    - Order ID: #{order.id}
    - Ad Title: {order.subject}
    - Description: {order.description}
    - Order Date: {context['order_date']}
    - Approval Date: {context['approval_date']}

    View your ad: {context['ad_url']}

    If you have any questions, our support team is here to help!

    © {context['current_year']} Your Company Name
    """
    
    # Send email
    email = EmailMultiAlternatives(
        subject,
        text_content.strip(),
        'noreply@yourdomain.com',
        [user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

AD_PRINTED_EMAIL_HTML = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background-color: #f8f9fa; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .footer {{ text-align: center; padding: 20px; font-size: 0.8em; color: #666; }}
        .button {{
            display: inline-block; padding: 10px 20px; background-color: #007bff; 
            color: white; text-decoration: none; border-radius: 5px; margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Your Ad Has Been Printed!</h2>
        </div>
        <div class="content">
            <p>Dear {user_first_name},</p>
            <p>We're pleased to inform you that your advertisement has been successfully printed and will be published soon.</p>
            
            <h3>Order Details</h3>
            <p><strong>Order ID:</strong> #{order_id}</p>
            <p><strong>Ad Title:</strong> {ad_title}</p>
            <p><strong>Description:</strong> {ad_description}</p>
            <p><strong>Agency:</strong> {agency}</p>
            <p><strong>Agency Email:</strong> {agency_email}</p>
            <p><strong>Order Date:</strong> {order_date}</p>
            <p><strong>Print Date:</strong> {print_date}</p>
        </div>
        
        <p>If you have any questions or need assistance, our support team is here to help!</p>
    </div>
    <div class="footer">
        &copy; {current_year} Your Company Name. All rights reserved.<br>
        <a href="{unsubscribe_url}">Unsubscribe</a>
    </div>
</body>
</html>
"""

def send_ad_printed_email(user, order, agency):
    subject = f"Your Ad Has Been Printed - Order #{order.id}"
    
    # Prepare context variables
    context = {
        'user_first_name': user.first_name,
        'order_id': order.id,
        'ad_title': order.subject,
        'ad_description': order.description,
        'agency': agency.username,
        'agency_email': agency.email,
        'order_date': order.order_date.strftime('%Y-%m-%d'),
        'print_date': datetime.now().strftime('%Y-%m-%d'),
        'unsubscribe_url': 'https://yourdomain.com/unsubscribe',
        'current_year': datetime.now().year
    }
    
    # Render HTML content using the AD_PRINTED_EMAIL_HTML template
    html_content = AD_PRINTED_EMAIL_HTML.format(**context)
    
    # Create plain text version
    text_content = f"""
    Dear {user.first_name},

    We're pleased to inform you that your advertisement has been successfully printed and will be published soon.

    Order Details:
    - Order ID: #{order.id}
    - Ad Title: {order.subject}
    - Description: {order.description}
    - Agency: {agency.username}
    - Agency Email: {agency.email}
    - Order Date: {context['order_date']}
    - Print Date: {context['print_date']}

    If you have any questions, our support team is here to help!

    © {context['current_year']} Your Company Name
    """
    
    # Send email
    email = EmailMultiAlternatives(
        subject,
        text_content.strip(),
        'noreply@yourdomain.com',
        [user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


def send_test_email():
    send_mail(
        'Test Email Subject',
        'This is a simple test email body.',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )

def send_welcome_email(user):
    subject = f"Welcome {user.first_name}!"
    
    # Prepare context variables
    context = {
        'first_name': user.first_name,
        'username': user.username,
        'email': user.email,
        'login_url': 'https://yourdomain.com/login',
        'unsubscribe_url': 'https://yourdomain.com/unsubscribe',
        'current_year': datetime.now().year  # Fixed: using datetime directly
    }
    
    # Render HTML content
    html_content = WELCOME_EMAIL_HTML.format(**context)
    
    # Create plain text version
    text_content = f"""
    Welcome {user.first_name}!
    
    Thank you for registering with us. Here are your account details:
    
    Username: {user.username}
    Email: {user.email}
    
    You can login here: {context['login_url']}
    
    © {context['current_year']} Your Company Name. All rights reserved.
    """
    
    # Send email
    email = EmailMultiAlternatives(
        subject,
        text_content.strip(),
        'welcome@yourdomain.com',
        [user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()


def send_user_block_email(user):
    subject = f"Account Blocked - {user.first_name}"
    
    # Prepare context variables
    context = {
        'first_name': user.first_name,
        'username': user.username,
        'email': user.email,
        'support_email': 'support@yourdomain.com',
        'current_year': datetime.now().year
    }
    
    # Create HTML content
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .header {{ background: #dc3545; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .footer {{ 
                margin-top: 30px; 
                padding-top: 20px; 
                border-top: 1px solid #eee; 
                color: #666; 
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Account Blocked</h1>
        </div>
        <div class="content">
            <p>Dear {user.first_name},</p>
            <p>We regret to inform you that your account has been blocked due to violation of our terms of service.</p>
            <p>If you believe this is a mistake or have any questions, please contact our support team at {context['support_email']}.</p>
        </div>
        <div class="footer">
            &copy; {context['current_year']} Your Company Name. All rights reserved.
        </div>
    </body>
    </html>
    """
    
    # Create plain text version
    text_content = f"""
    Account Blocked Notification
    
    Dear {user.first_name},
    
    We regret to inform you that your account has been blocked due to violation of our terms of service.
    
    If you believe this is a mistake or have any questions, please contact our support team at {context['support_email']}.
    
    © {context['current_year']} Your Company Name. All rights reserved.
    """
    
    # Send email
    email = EmailMultiAlternatives(
        subject,
        text_content.strip(),
        'noreply@yourdomain.com',
        [user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
def send_agency_block_email(agency):
    """
    Sends an email notification to an agency when their account is blocked
    """
    subject = "Your Agency Account Has Been Blocked"
    
    # Create context for email
    context = {
        'support_email': 'support@yourdomain.com',
        'current_year': datetime.now().year
    }
    
    # HTML email content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .header {{ background: #dc3545; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .footer {{ 
                margin-top: 30px; 
                padding-top: 20px; 
                border-top: 1px solid #eee; 
                color: #666; 
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Agency Account Blocked</h1>
        </div>
        <div class="content">
            <p>Dear {agency.username},</p>
            <p>We regret to inform you that your agency account has been blocked due to violation of our terms of service.</p>
            <p>If you believe this is a mistake or have any questions, please contact our support team at {context['support_email']}.</p>
        </div>
        <div class="footer">
            &copy; {context['current_year']} Your Company Name. All rights reserved.
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    text_content = f"""
    Agency Account Blocked Notification
    
    Dear {agency.username},
    
    We regret to inform you that your agency account has been blocked due to violation of our terms of service.
    
    If you believe this is a mistake or have any questions, please contact our support team at {context['support_email']}.
    
    © {context['current_year']} Your Company Name. All rights reserved.
    """
    
    # Send email
    email = EmailMultiAlternatives(
        subject,
        text_content.strip(),
        'noreply@yourdomain.com',
        [agency.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
def send_agency_unblock_email(agency):
    subject = "Your Agency Account Has Been Unblocked"
    
    # Prepare context variables
    context = {
        'username': agency.username,
        'support_email': 'support@yourdomain.com',
        'current_year': datetime.now().year
    }
    
    # HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .header {{ background: #28a745; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .footer {{ 
                margin-top: 30px; 
                padding-top: 20px; 
                border-top: 1px solid #eee; 
                color: #666; 
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Agency Account Unblocked</h1>
        </div>
        <div class="content">
            <p>Dear {agency.username},</p>
            <p>We're pleased to inform you that your agency account has been unblocked and is now active again.</p>
            <p>You can now login and access all features. If you have any questions, please contact our support team at {context['support_email']}.</p>
        </div>
        <div class="footer">
            &copy; {context['current_year']} Your Company Name. All rights reserved.
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    text_content = f"""
    Agency Account Unblocked Notification
    
    Dear {agency.username},
    
    We're pleased to inform you that your agency account has been unblocked and is now active again.
    
    You can now login and access all features. If you have any questions, please contact our support team at {context['support_email']}.
    
    © {context['current_year']} Your Company Name. All rights reserved.
    """
    
    # Send email
    email = EmailMultiAlternatives(
        subject,
        text_content.strip(),
        'noreply@yourdomain.com',
        [agency.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_user_unblock_email(user):
    subject = "Your Account Has Been Unblocked"
    
    # Prepare context variables
    context = {
        'username': user.username,
        'support_email': 'support@yourdomain.com',
        'current_year': datetime.now().year
    }
    
    # HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .header {{ background: #28a745; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .footer {{ 
                margin-top: 30px; 
                padding-top: 20px; 
                border-top: 1px solid #eee; 
                color: #666; 
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Account Unblocked</h1>
        </div>
        <div class="content">
            <p>Dear {user.username},</p>
            <p>We're pleased to inform you that your account has been unblocked and is now active again.</p>
            <p>You can now login and access all features. If you have any questions, please contact our support team at {context['support_email']}.</p>
        </div>
        <div class="footer">
            &copy; {context['current_year']} Your Company Name. All rights reserved.
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    text_content = f"""
    Account Unblocked Notification
    
    Dear {user.username},
    
    We're pleased to inform you that your account has been unblocked and is now active again.
    
    You can now login and access all features. If you have any questions, please contact our support team at {context['support_email']}.
    
    © {context['current_year']} Your Company Name. All rights reserved.
    """
    
    # Send email
    email = EmailMultiAlternatives(
        subject,
        text_content.strip(),
        'noreply@yourdomain.com',
        [user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_order_confirmation_email(user, order, agency):
    subject = f"Order Confirmation - {order.subject}"
    
    # Prepare context variables
    context = {
        'first_name': user.first_name,
        'email': user.email,
        'order_date': order.order_date,
        'date': order.date,
        'subject': order.subject,
        'description': order.description,
        'price': order.price,
        'poster': f"{settings.MEDIA_URL}order/{order.poster}" if order.poster else None,
        'height': order.height,
        'width': order.width,
        'ad_color': order.ad_color,
        'any_preferance': order.any_preferance,
        'agency_name': agency.username,
        'agency_email': agency.email,
        'current_year': datetime.now().year
    }
    
    # HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .header {{ background: #4CAF50; color: white; padding: 20px; text-align: center; }}
            .content {{ padding: 20px; }}
            .receipt {{ 
                border: 1px solid #ddd;
                padding: 20px;
                margin: 20px 0;
                background: #f9f9f9;
            }}
            .receipt-item {{ margin: 10px 0; }}
            .footer {{ 
                margin-top: 30px; 
                padding-top: 20px; 
                border-top: 1px solid #eee; 
                color: #666; 
                font-size: 0.9em;
            }}
            .poster-img {{ max-width: 100%; height: auto; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Order Confirmation</h1>
        </div>
        <div class="content">
            <p>Dear {user.first_name},</p>
            <p>Thank you for your order! Here are the details:</p>
            
            <div class="receipt">
                <div class="receipt-item"><strong>Order Date:</strong> {order.order_date}</div>
                <div class="receipt-item"><strong>Subject:</strong> {order.subject}</div>
                <div class="receipt-item"><strong>Description:</strong> {order.description}</div>
                <div class="receipt-item"><strong>Price:</strong> ${order.price}</div>
                {f'<div class="receipt-item"><strong>Poster:</strong><br><img src="{context["poster"]}" class="poster-img"></div>' if context["poster"] else ''}
                {f'<div class="receipt-item"><strong>Dimensions:</strong> {order.height} x {order.width}</div>' if order.height and order.width else ''}
                <div class="receipt-item"><strong>Ad Color:</strong> {order.ad_color}</div>
                {f'<div class="receipt-item"><strong>Preferences:</strong> {order.any_preferance}</div>' if order.any_preferance else ''}
                <div class="receipt-item"><strong>Agency:</strong> {agency.username}</div>
                <div class="receipt-item"><strong>Agency Email:</strong> {agency.email}</div>
            </div>
            
            <p>If you have any questions, please contact the agency or our support team.</p>
        </div>
        <div class="footer">
            &copy; {context['current_year']} Your Company Name. All rights reserved.
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    text_content = f"""
    Order Confirmation
    
    Dear {user.first_name},
    
    Thank you for your order! Here are the details:
    
    Order Date: {order.order_date}
    Subject: {order.subject}
    Description: {order.description}
    Price: ${order.price}
    {f'Poster: {context["poster"]}' if context["poster"] else ''}
    {f'Dimensions: {order.height} x {order.width}' if order.height and order.width else ''}
    Ad Color: {order.ad_color}
    {f'Preferences: {order.any_preferance}' if order.any_preferance else ''}
    Agency: {agency.username}
    Agency Email: {agency.email}
    
    If you have any questions, please contact the agency or our support team.
    
    © {context['current_year']} Your Company Name. All rights reserved.
    """
    
    # Send email
    email = EmailMultiAlternatives(
        subject,
        text_content.strip(),
        'noreply@yourdomain.com',
        [user.email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_inquiry_received_email(name, contact, email, message):
    subject = "Inquiry Received - Ad Release"
    current_year = datetime.now().year
    
    # HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 0;
            }}
            .header-bar {{
                background-color: #D2B48C;
                padding: 20px;
                text-align: center;
                color: white;
                font-size: 24px;
                font-weight: bold;
            }}
            .content {{
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .footer {{
                padding: 15px;
                text-align: center;
                font-size: 12px;
                color: #777;
                background-color: #eee;
            }}
        </style>
    </head>
    <body>
        <div class="header-bar">
            Inquiry Received - Ad Release
        </div>
        <div class="content">
            <p>Dear {name},</p>
            <p>Thank you for reaching out to us! We have received your inquiry and our team will get back to you shortly.</p>
            
            <div class="inquiry-details">
                <p><strong>Your Inquiry Details:</strong></p>
                <p>Name: {name}</p>
                <p>Contact: {contact}</p>
                <p>Email: {email}</p>
                <p>Message: {message}</p>
            </div>
            
            <p>We appreciate your interest in our services and look forward to assisting you.</p>
        </div>
        <div class="footer">
            &copy; {current_year} Ad Release. All rights reserved.
        </div>
    </body>
    </html>
    """
    
    # Plain text content
    text_content = f"""
    Inquiry Received - Ad Release
    
    Dear {name},
    
    Thank you for reaching out to us! We have received your inquiry and our team will get back to you shortly.
    
    Your Inquiry Details:
    Name: {name}
    Contact: {contact}
    Email: {email}
    Message: {message}
    
    We appreciate your interest in our services and look forward to assisting you.
    
    © {current_year} Ad Release. All rights reserved.
    """
    
    # Send email
    email = EmailMultiAlternatives(
        subject,
        text_content.strip(),
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()

def send_password_reset_email(email, name,token):
    subject = "Password Reset Request - Ad Release"
    current_year = datetime.now().strftime('%B %d, %Y %I:%M %p')
    
    # HTML content
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 5px;">
            <h2 style="color: #333;">Password Reset Request</h2>
            <p>Dear {name},</p>
            <p>We received a request to reset your password. Please click the button below to change your password:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <a href="http://localhost/resetemailpassword.php?token={token}" 
                    style="background-color: #007bff; color: white; padding: 10px 20px; 
                            text-decoration: none; border-radius: 5px; display: inline-block;">
                    Change Password
                </a>
            </div>
            
            <p>If you didn't request this password reset, you can safely ignore this email.</p>
            <p style="margin-top: 30px; color: #666; font-size: 0.9em;">
                &copy; {current_year} Ad Release. All rights reserved.
            </p>
        </div>
    </body>
    </html>
    """
    
    # Plain text content
    text_content = f"""
    Password Reset Request - Ad Release
    
    Dear {name},
    
    We received a request to reset your password. Please visit the following link to change your password:
    
    https:/localhost/forgetPassword.php
    
    If you didn't request this password reset, you can safely ignore this email.
    
    © {current_year} Ad Release. All rights reserved.
    """
    
    # Send email
    email = EmailMultiAlternatives(
        subject,
        text_content.strip(),
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
