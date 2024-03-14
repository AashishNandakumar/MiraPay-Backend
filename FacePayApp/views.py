import os
from rest_framework.response import Response
from . import serializers
from rest_framework.views import APIView
from rest_framework import status
import uuid
import boto3
from botocore.exceptions import NoCredentialsError
from . import models
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv

load_dotenv()


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
        # print("uuid for S3: ", object_name)
        bucket_name = os.getenv('BUCKET_NAME')
        region = os.getenv('REGION')

        s3Client = boto3.client('s3', region_name=region,)

        try:
            presigned_url = s3Client.generate_presigned_url('put_object',  # permission on the bucket
                                                            Params={'Bucket': bucket_name, 'Key': object_name, 'ContentType': 'image/png'},  # the content type should match both on the backend and the frontend
                                                            ExpiresIn=3600)  # 1 hr expiry time for the URL

            return Response({'url': presigned_url}, status.HTTP_200_OK)

        except NoCredentialsError:  # trigger when the backend has no proper cred. to interact wit AWS
            return Response({'error': 'Credentials not available'}, status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
class GenerateSignedURLsForVerification(APIView):
    def get(self, request):
        object_name = request.query_params.get('fileName', 'UUID-Absent')

        bucket_name = 'mpay-user-verification-bucket'
        region = 'us-east-1'

        s3Client = boto3.client('s3', region_name=region)

        try:
            presigned_url = s3Client.generate_presigned_url('put_object',
                                                            Params={'Bucket': bucket_name, 'Key': object_name, 'ContentType': 'image/png'},
                                                            ExpiresIn=3600)

            return Response({'url': presigned_url}, status.HTTP_200_OK)

        except NoCredentialsError:  # trigger when the backend has no proper cred. to interact wit AWS
            return Response({'error': 'Credentials not available'}, status.HTTP_500_INTERNAL_SERVER_ERROR)
"""


class VerifyUser(APIView):
    def post(self, request):
        try:
            if 'file' not in request.FILES:
                return Response({'error': 'No file part'}, status.HTTP_400_BAD_REQUEST)

            file = request.FILES['file']

            image_bytes = file.read()

            rekognition_client = boto3.client('rekognition')
            collection_id = 'user_faces'
            search_response = rekognition_client.search_faces_by_image(
                CollectionId=collection_id,
                Image={'Bytes': image_bytes},
                FaceMatchThreshold=90,  # for testing only
                MaxFaces=1
            )

            face_matches = search_response.get('FaceMatches', [])
            if face_matches:
                match = face_matches[0]
                matched_face_id = match['Face']['FaceId']
                matched_external_image_id = match['Face']['ExternalImageId'].split('.')[0]
                confidence = match['Face']['Confidence']

                print(f"Match found: FaceId = {matched_face_id}, ExternalImageId = {matched_external_image_id}, Confidence = {confidence}")

                return Response({'userId': matched_external_image_id}, status.HTTP_200_OK)
            else:
                return Response({"Error": "User not found!"}, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Failed to fetch user facial data: ", e)
            return Response({"Error": "Failed in fetching User Facial Data"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserData(APIView):
    def get(self, request):
        try:
            user_id = request.query_params.get('userId')

            userInfo = get_object_or_404(models.UserInformation, userId=user_id)
            financialInfo = get_object_or_404(models.FinancialInformation, userId_id=user_id)

            serializer1 = serializers.UserInformationSerializer(userInfo)
            serializer2 = serializers.FinancialInformationSerializer(financialInfo)
            # print(serializer1, serializer2)

            if serializer1 and serializer2:
                return Response({
                    'userInfo': serializer1.data,
                    'financialInfo': serializer2.data
                }, status.HTTP_200_OK)
            else:
                return Response({"Error": "Error in fetching user details"}, status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("Failed to fetch user details: ", e)
            return Response({"Error": "Failed in fetching User Data"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class BillUserAndSendReceipt(APIView):

    def post(self, request):
        try:
            invoice_pdf = request.data.get('file')
            payload = request.data.get('payload')

            invoice_meta_data = payload.get('invoice_meta_data')
            invoice_item_data = payload.get('invoice_item_data')
            user_upi_id = payload.get('user_upi_id')
            user_email = payload.get('user_email')

            invoice_meta_data_serializer = serializers.InvoiceInformationSerializer(data=invoice_meta_data)
            invoice_meta_data_serializer.is_valid(raise_exception=True)
            invoice_meta_data_serializer.save()

            # logic to push data into 'ItemInformation'

        except Exception as e:
            print("Error while Billing User: ", e)
