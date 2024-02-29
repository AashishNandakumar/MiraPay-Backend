from rest_framework.response import Response
from . import serializers
from rest_framework.views import APIView
from rest_framework import status
import uuid
import boto3
from botocore.exceptions import NoCredentialsError


# Create your views here.
class AddData(APIView):
    def post(self, request):
        try:
            user_info = request.data.get("UserInformation")
            # print("user_info: ", user_info)

            serialized_user_info = serializers.UserInformationSerializer(data=user_info)
            serialized_user_info.is_valid(raise_exception=True)
            serialized_user_info.save()

            financial_info = request.data.get("FinancialInformation")
            # print("finance_info: ", financial_info)

            serialized_financial_info = serializers.FinancialInformationSerializer(data=financial_info)
            serialized_financial_info.is_valid(raise_exception=True)
            serialized_financial_info.save()

            return Response({"message": "data saved successfully"}, status.HTTP_201_CREATED)

        except Exception as e:
            print("Error in Adding data to RDS", e)
            return Response({"error", "Error saving data"}, status.HTTP_400_BAD_REQUEST)


class GenerateUUID(APIView):
    def get(self, request):
        try:
            new_uuid = uuid.uuid4()  # 4th version + more random

            return Response(new_uuid, status.HTTP_200_OK)
        except Exception as e:
            print("Error in generating UUID ", e)
            return Response({"error": "Error in generating UUID"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class GenerateSignedURLs(APIView):
    def get(self, request):
        object_name = request.query_params.get('fileName', 'UUID-Absent')
        print("uuid for S3: ", object_name)
        bucket_name = 'mpay-user-image-bucket'
        region = 'us-east-1'

        s3Client = boto3.client('s3', region_name=region)

        try:
            presigned_url = s3Client.generate_presigned_url('put_object',  # permission on the bucket
                                                            Params={'Bucket': bucket_name, 'Key': object_name, 'ContentType': 'image/png'},  # the content type should match both on the backend and the frontend
                                                            ExpiresIn=3600)  # 1 hr expiry time for the URL

            return Response({'url': presigned_url}, status.HTTP_200_OK)

        except NoCredentialsError:  # trigger when the backend has no proper cred. to interact wit AWS
            return Response({'error': 'Credentials not available'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
