from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from .models import *
from subjects.models import Subject
from users.models import Student, User
from .serializers import FeedbackCreateSerializer, FeedbackSubmitSerializer, FeedbackViewSerializer, FeedbackResponseViewSerializer

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

                if (request.user != subject.created_by.user):
                    return Response({ "Error": "Unauthorized" , "Message": "User not owner of the subject !"}, status=status.HTTP_401_UNAUTHORIZED)
                
                feedback = Feedback(title=data['title'], subject=subject, created_by=request.user.faculty)
                feedback.save()

                return Response({'Success': "Feedback Created Successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
Checks:
If Feedback ID is valid : tested
If account is student : tested
If student is eligible : tested
'''
class FeedbackSubmit(generics.GenericAPIView):
    serializer_class = FeedbackSubmitSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Feedback Submition",
                         responses={ 201: 'Submitted Successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})
    
    def post(self, request, id):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.data

            if (not Feedback.objects.filter(pk=id).exists()):
                return Response({ "Error": "Invalid ID" , "Message": "The given feedback does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
            
            if (not request.user.is_student):
                return Response({ "Error": "Unauthorized" , "Message": "Only students can submit feedback!"}, status=status.HTTP_401_UNAUTHORIZED)

            feedback = Feedback.objects.get(pk=id)
            # assumes that student user will have a student profile
            if (not request.user.student in feedback.subject.students.all()):
                return Response({ "Error": "Unauthorized" , "Message": "You are not eligible to submit feedback!"}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                feed_response = FeedbackResponse(student=request.user.student, feedback=feedback, response=data['response'])
                feed_response.save()

                return Response({'Success': "Feedback Submitted Successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
ID: Subject ID
Checks:
If subject ID is valid
If user is the owner of subject
If user is faculty (can be assume if above true)
'''
class FeedbackList(generics.GenericAPIView):
    serializer_class = FeedbackViewSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Feedbacks list for a subject, parameter is subject id",
                         responses={ 200: 'Data retrieved successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})

    def get(self, request, id):

        try:
            if (not Subject.objects.filter(pk=id).exists()):
                return Response({ "Error": "Invalid ID" , "Message": "The given subject does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
            
            subject = Subject.objects.get(pk=id)

            if (request.user != subject.created_by.user):
                return Response({ "Error": "Unauthorized" , "Message": "User not owner of the subject"}, status=status.HTTP_401_UNAUTHORIZED)
            
            feedbacks = Feedback.objects.filter(created_by=request.user.faculty, subject=subject).order_by('-created_on')
            feed_dicts = [f.__dict__ for f in feedbacks]

            serializer = self.serializer_class(data=feed_dicts, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)

'''
ID: Feedback ID
Checks:
If ID is valid
If user is the one who created the feedback
'''
class FeedbackResponseList(generics.GenericAPIView):
    serializer_class = FeedbackResponseViewSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Feedback responses list for a feedback",
                         responses={ 200: 'Data retrieved successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})

    def get(self, request, id):

        try:
            if (not Feedback.objects.filter(pk=id).exists()):
                return Response({ "Error": "Invalid ID" , "Message": "The given feedback does not exist!"}, status=status.HTTP_400_BAD_REQUEST)
            
            feedback = Feedback.objects.get(pk=id)

            if (request.user != feedback.created_by.user):
                return Response({ "Error": "Unauthorized" , "Message": "User not owner of the feedback"}, status=status.HTTP_401_UNAUTHORIZED)
            
            feed_responses = FeedbackResponse.objects.filter(feedback=feedback).order_by('-submitted_on')
            feedres_dicts = [f.__dict__ for f in feed_responses]
            
            for f in feedres_dicts:
                s_user = Student.objects.get(pk=f['student_id'])
                f['student_name'] = f"{s_user.user.first_name} {s_user.user.last_name}"

            serializer = self.serializer_class(data=feedres_dicts, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)