from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from .serializers import FacultyRegisterSerializer, UserLoginSerializer, StudentDetailSerializer
from .models import User, Faculty, Student
from subjects.models import QAGrade, Subject, LearningOutcome

class FacultyRegister(generics.GenericAPIView):
    serializer_class = FacultyRegisterSerializer

    @swagger_auto_schema(operation_description="Faculty Register",
                         responses={ 201: 'Registered Successfully',
                                409: 'Given data conflict with existing users',
                                400: 'Given data is invalid'})
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user_data = serializer.data
            try:
                user = User(username=user_data['username'], first_name=user_data['first_name'],
                                last_name=user_data['last_name'], email=user_data['email'])
                user.set_password(user_data['password'])
                user.save()
                try:
                    faculty = Faculty(user=user, **user_data['faculty'])
                    faculty.save()
                except Exception as e:
                    user.delete()
                    return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)
                return Response({'Success': "Faculty Created Successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FacultyLogin(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_student and user.is_approved:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)
        elif not user.is_approved:
            return Response({"Error": "Unauthorized", "Message": "The account has not been approved yet!"}, 
            status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"Error": "Unauthorized", "Message": "The account is not a faculty account !!"}, 
            status=status.HTTP_401_UNAUTHORIZED)

class StudentLogin(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user.is_student:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'username': user.username,
                'email': user.email,
                'admission_number': user.student.admission_number
            }, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "Unauthorized", "Message": "The account is not a student account !!"}, 
            status=status.HTTP_401_UNAUTHORIZED)

'''
Gets details of current student user
User must be student
ASSUMES that student has a profile created
ADD subject details later
'''
class StudentDetail(generics.GenericAPIView):
    serializer_class = StudentDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Get details of current student user, gives user id",
                         responses={ 200: 'Data retrieved successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})

    def get(self, request, id):

        try:
            if (not User.objects.filter(pk=id).exists()):
                return Response({ "Error": "Invalid ID" , "Message": "The given user does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(pk=id)

            if (not user.is_student):
                return Response({"Error": "Unauthorized", "Message": "The account is not a student account !!"}, 
                    status=status.HTTP_401_UNAUTHORIZED)
            
            if (request.user != user and request.user.is_student):
                return Response({"Error": "Unauthorized", "Message": "The account is not a permitted to view the details !!"}, 
                    status=status.HTTP_401_UNAUTHORIZED)

            data = user.__dict__
            data['profile'] = user.student.__dict__

            subjects = list()
            for sub in user.student.subjects.all():
                s_dict = sub.__dict__
                s_dict['learning_outcomes']  = [lo.__dict__ for lo in LearningOutcome.objects.filter(subject=sub).order_by('-created_on')]
                
                assessments = list()
                for ass in sub.assessments.all().order_by('-created_on'):
                    a_dict = ass.__dict__
                    if (ass.submissions.filter(student=user.student).exists()):
                        submission = ass.submissions.get(student=user.student)
                        a_dict['submitted_on'] = submission.submitted_on
                        
                        qas = list()
                        for qa in submission.assessment.questions.all():
                            qa_dict = qa.__dict__
                            qa_dict['learning_outcomes'] = [lo.__dict__ for lo in qa.learningoutcomes.all()]
                            if (qa.qagrades.filter(submission=submission).exists()):
                                qa_dict['mark'] = qa.qagrades.get(submission=submission).mark
                            else:
                                qa_dict['mark'] = 0
                            qas.append(qa_dict)
                        a_dict['response'] = qas
                    else:
                        a_dict['submitted_on'] = None
                        a_dict['response'] = []
                    assessments.append(a_dict)

                s_dict['assessments'] = assessments                       
                subjects.append(s_dict)
            data['subjects'] = subjects

            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)