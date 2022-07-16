from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from .models import Subject, LearningOutcome
from .serializers import StudentAddSerailizer, SubjectCreateSerializer, LOCreateSerializer, SubjectDetailSerailizer, SubjectListSerializer
from users.models import Student

'''
Subject create
User must be faculty
'''
class SubjectCreate(generics.GenericAPIView):
    serializer_class = SubjectCreateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Subject Creation",
                         responses={ 201: 'Created Successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            if (request.user.is_student):
                return Response({ "Error": "Unauthorized" , "Message": "Only faculty can create subject!"}, status=status.HTTP_401_UNAUTHORIZED)

            data = serializer.data
            try:
                subject = Subject(name=data['name'], description=data['description'], created_by=request.user.faculty)
                subject.save()

                return Response({'Success': "Subject Created Successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
Learning Outcomes create for a subject
subject id in parameter
data is given in list ie. multiple LOs.
Checks:
If id is valid
If user is the one who created the subject
'''
class LOCreate(generics.GenericAPIView):
    serializer_class = LOCreateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Learning Outcomes Creation (List)",
                         responses={ 201: 'Created Successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})
    
    def post(self, request, id):
        serializer = self.serializer_class(data=request.data, many=True)

        if serializer.is_valid():
            data = serializer.data

            if (not Subject.objects.filter(pk=id).exists()):
                return Response({ "Error": "Invalid ID" , "Message": "The given subject does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

            subject = Subject.objects.get(pk=id)

            if (request.user != subject.created_by.user):
                return Response({ "Error": "Unauthorized" , "Message": "User not owner of the subject"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                for lo in data:
                    lo = LearningOutcome(name=lo['name'], subject=subject)
                    lo.save()
                
                return Response({'Success': "Learning outcomes added successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)    

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
Subjects list for a faculty:
List the basic subject details for a faculty
Checks:
If user is faculty
'''
class SubjectList(generics.GenericAPIView):
    serializer_class = SubjectListSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Subjects List",
                         responses={ 200: 'Data Retrieved Successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})
    
    def get(self, request):

        try:
            if (request.user.is_student):
                return Response({ "Error": "Unauthorized" , "Message": "User not faculty !!"}, status=status.HTTP_401_UNAUTHORIZED)
            
            subs = Subject.objects.filter(created_by=request.user.faculty).order_by('-created_on')
            sub_dicts = [s.__dict__ for s in subs]
            
            serializer = self.serializer_class(data=sub_dicts, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)

'''
Subject detail api
Checks:
If subject id is valid
If the user is owner of subject
'''
class SubjectDetail(generics.GenericAPIView):
    serializer_class = SubjectDetailSerailizer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Subjects Detail",
                         responses={ 200: 'Data Retrieved Successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})

    def get(self, request, id):

        try:
            if (not Subject.objects.filter(pk=id).exists()):
                return Response({ "Error": "Invalid ID" , "Message": "The given subject does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

            subject = Subject.objects.get(pk=id)

            if (request.user != subject.created_by.user):
                return Response({ "Error": "Unauthorized" , "Message": "User not owner of the subject"}, status=status.HTTP_401_UNAUTHORIZED)
            
            sub_dict = subject.__dict__

            sub_dict['learning_outcomes']  = [lo.__dict__ for lo in LearningOutcome.objects.filter(subject=subject)]

            students = list()
            for s in subject.students.all():
                u_dict = s.user.__dict__
                u_dict['admission_number'] = s.admission_number
                students.append(u_dict)
            sub_dict['students'] = students    
            
            serializer = self.serializer_class(data=sub_dict)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)

'''
Add students to subject with admission_number
Checks:
If subject ID is valid
If user owner of subject
If given admission_number is valid
'''
class SubjectStudentAdd(generics.GenericAPIView):
    serializer_class = StudentAddSerailizer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Add student to a subject with admission number",
                         responses={ 201: 'Added Successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})
    
    def post(self, request, id):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            adm_num = serializer.data['admission_number']

            if (not Subject.objects.filter(pk=id).exists()):
                return Response({ "Error": "Invalid ID" , "Message": "The given subject does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

            subject = Subject.objects.get(pk=id)

            if (request.user != subject.created_by.user):
                return Response({ "Error": "Unauthorized" , "Message": "User not owner of the subject"}, status=status.HTTP_401_UNAUTHORIZED)

            if (not Student.objects.filter(admission_number=adm_num).exists()):
                return Response({ "Error": "Invalid Admission Number" , "Message": "The given admission number is invalid !"}, status=status.HTTP_400_BAD_REQUEST)

            student = Student.objects.get(admission_number=adm_num)
            try:
                subject.students.add(student)             
                return Response({'Success': "Student added successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)    

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

