from django.conf import settings
from django.core.mail import send_mail, EmailMessage


def send_payment_link_email(payment_link, financial_information):
    to_email = financial_information.get('user_email')

    subject = "Your payment link"
    message = f"Please use the following link to make a payment: {payment_link}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [to_email, ]

    send_mail(subject, message, email_from, recipient_list)


def send_email_with_pdf_attachment(invoice_pdf, financial_information):
    try:
        recipient_email = financial_information.get('user_email')
        subject = "Your Invoice for Purchase ID: " + financial_information.get('invoice_number')
        body_text = "Please find the attached Invoice PDF for your purchase."

        email = EmailMessage(
            subject=subject,
            body=body_text,
            from_email=settings.EMAIL_HOST_USER,
            to=[recipient_email]
        )

        email.attach(invoice_pdf.name, invoice_pdf.read(), 'application/pdf')

        email.send()

        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}")
