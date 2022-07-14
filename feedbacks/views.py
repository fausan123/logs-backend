from turtle import title
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from .models import *
from subjects.models import Subject
from .serializers import FeedbackCreateSerializer, FeedbackSubmitSerializer

class FeedbackCreate(generics.GenericAPIView):
    serializer_class = FeedbackCreateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Feedback Creation",
                         responses={ 201: 'Created Successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.data
            try:
                if (not Subject.objects.filter(pk=data['subject']).exists()):
                    return Response({ "Error": "Invalid ID" , "Message": "The given subject does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
                subject = Subject.objects.get(pk=data['subject'])

                if (request.user.is_student):
                    return Response({ "Error": "Unauthorized" , "Message": "Only faculty can create feedback!"}, status=status.HTTP_401_UNAUTHORIZED)
                
                feedback = Feedback(title=data['title'], subject=subject, created_by=request.user.faculty)
                feedback.save()

                return Response({'Success': "Feedback Created Successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)