import os
import boto3


def send_payment_link_sms(**kwargs):
    financial_information = kwargs['fi']
    payment_link = kwargs['pl']

    sns_client = boto3.client('sns',
                              aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID1'),
                              aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY1'),
                              region_name=os.getenv('REGION'))

    sns_client.publish(
        PhoneNumber=financial_information.get('user_phone_number'),  # E.164 format
        Message=f"Please find your payment link here: {payment_link}",
        MessageAttributes={
            'AWS.SNS.SMS.SMSType': {
                'DataType': 'String',
                'StringValue': 'Transactional'
            }
        }
    )
