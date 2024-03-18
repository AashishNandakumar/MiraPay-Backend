import os
import razorpay


def generate_payment_link(**kwargs):
    try:
        client = razorpay.Client(auth=(os.getenv('RAZORPAY_KEY_ID'), os.getenv('RAZORPAY_KEY_SECRET')))
        client.set_app_details({"title": "Django", "version": "5.0.2"})

        financial_information = kwargs['financial_information']

        data = {
            "type": "link",
            "amount": financial_information.get('total_bill') * 100,  # Amount in 'paisa'
            "currency": "INR",
            "accept_partial": False,
            "description": f"Payment for Invoice no: {financial_information.get('invoice_number')}",
            "customer": {
                "name": financial_information.get('user_name'),
                "email": financial_information.get('user_email'),
                "contact": financial_information.get('user_phone_number')
            },
            "notify": {
                "sms": True,
                "email": True
            },
            "reminder_enable": True,
            "notes": {
                "upi_id": financial_information.get('user_upi_id')
            },

        }
        # Create a payment link/invoice
        response = client.invoice.create(data=data)

        return response['short_url']  # just return the invoice link

    except Exception as e:
        print(f"Error while creating a payment link: {e}")
        return None
