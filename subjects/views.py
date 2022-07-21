from django.forms import ValidationError
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema

from .models import Assessment, AssessmentQuestion, AssessmentSubmission, QAGrade, Subject, LearningOutcome
from .serializers import AssessmentCreateSerializer, AssessmentDetailSerializer, AssessmentProgressGraphSerializer, AssessmentSubmitSerializer, LOImproveSerializer, LOSuggestSerializer, StudentAddSerailizer, SubjectCreateSerializer, LOCreateSerializer, SubjectDetailSerailizer, SubjectListSerializer
from users.models import Student
from .utils import suggest_lo


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

            sub_dict['learning_outcomes']  = [lo.__dict__ for lo in LearningOutcome.objects.filter(subject=subject).order_by('-created_on')]
            sub_dict['assessments'] = [ass.__dict__ for ass in Assessment.objects.filter(subject=subject).order_by('-created_on')]

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

'''
Assessment Creation
Checks:
If subject id is valid
If user owner of subject
'''
class AssessmentCreate(generics.GenericAPIView):
    serializer_class = AssessmentCreateSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Create an assessment for a subject",
                         responses={ 201: 'Created Successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})
    
    def post(self, request, id):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.data

            if (not Subject.objects.filter(pk=id).exists()):
                return Response({ "Error": "Invalid ID" , "Message": "The given subject does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

            subject = Subject.objects.get(pk=id)

            if (request.user != subject.created_by.user):
                return Response({ "Error": "Unauthorized" , "Message": "User not owner of the subject"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                assessment = Assessment(title=data['title'], description=data['description'], subject=subject)
                assessment.save()

                try:

                    for question in data['questions']:
                        ques = AssessmentQuestion(question=question['question'], assessment=assessment)
                        ques.save()
                        ques.learningoutcomes.add(*question['learningoutcomes'])
                
                except Exception as e:
                    assessment.delete()
                    return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)  

                return Response({'Success': "Assessment created successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)    

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
Assessment Detail API:
Checks:
Check if assessment id is valid
If user is owner of subject
'''
class AssessmentDetail(generics.GenericAPIView):
    serializer_class = AssessmentDetailSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Assessment Detail",
                         responses={ 200: 'Data Retrieved Successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})

    def get(self, request, id):

        try:
            if (not Assessment.objects.filter(pk=id).exists()):
                return Response({ "Error": "Invalid ID" , "Message": "The given assessment does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

            assessment = Assessment.objects.get(pk=id)

            if (request.user != assessment.subject.created_by.user):
                return Response({ "Error": "Unauthorized" , "Message": "User not owner of the subject"}, status=status.HTTP_401_UNAUTHORIZED)
            
            a_dict = assessment.__dict__

            questions = list()
            for question in assessment.questions.all():
                q_dict = question.__dict__
                q_dict['learningoutcomes'] = [lo.__dict__ for lo in question.learningoutcomes.all()]
                questions.append(q_dict)
            a_dict['questions'] = questions

            responses = list()
            for res in AssessmentSubmission.objects.filter(assessment=assessment).order_by('-submitted_on'):
                r_dict = res.__dict__
                r_dict['marks'] = sum(qa.mark for qa in QAGrade.objects.filter(submission=res))
                r_dict['id'] = res.id
                r_dict['user_id'] = res.student.user.id
                r_dict['admission_number'] = res.student.admission_number
                responses.append(r_dict)
            a_dict['responses'] = responses
                        
            serializer = self.serializer_class(data=a_dict)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)

'''
Assessment Submission API
Check:
If Assessment id is valid
If admission number is valid
If student member of subject
If user owner of subject
'''
class AssessmentSubmit(generics.GenericAPIView):
    serializer_class = AssessmentSubmitSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Submit an assessment for a subject using admission number",
                         responses={ 201: 'Submitted Successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})
    
    def post(self, request, id):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = serializer.data

            if (not Assessment.objects.filter(pk=id).exists()):
                return Response({ "Error": "Invalid ID" , "Message": "The given assessment does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

            if (not Student.objects.filter(admission_number=data['admission_number']).exists()):
                return Response({ "Error": "Invalid Admission Number" , "Message": "The given admission number is invalid !"}, status=status.HTTP_400_BAD_REQUEST)

            student = Student.objects.get(admission_number=data['admission_number'])
            assessment = Assessment.objects.get(pk=id)

            if (student not in assessment.subject.students.all()):
                return Response({ "Error": "Unauthorized" , "Message": "Student not added to subject"}, status=status.HTTP_401_UNAUTHORIZED)

            if (request.user != assessment.subject.created_by.user):
                return Response({ "Error": "Unauthorized" , "Message": "User not owner of the subject"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                submission = AssessmentSubmission(student=student, assessment=assessment)
                submission.save()

                try:

                    for question in data['questions']:
                        ques = AssessmentQuestion.objects.get(pk=question['question'])
                        if (ques.assessment != assessment):
                            raise ValidationError("Question ID does not belong to the given subject !")
                        else:
                            qa = QAGrade(question=ques, mark=question['mark'], submission=submission)
                            qa.save()
                
                except Exception as e:
                    submission.delete()
                    return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)  

                return Response({'Success': "Assessment submitted successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)    

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


'''
Generate a graph data for each student for each subject
Inputs admission number and gives subject id as param
Checks:
Subject ID
Admission Number
If user is faculty / is the owner of profile
If admission number part of profile
'''
class ProgressGraph(generics.GenericAPIView):
    serializer_class = AssessmentProgressGraphSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Assessment Progress Graph Data for each student by admission number",
                         responses={ 200: 'Data Retrieved Successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})

    def get(self, request, id, adm_num):

        try:
            if (not Subject.objects.filter(pk=id).exists()):
                return Response({ "Error": "Invalid ID" , "Message": "The given subject does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

            subject = Subject.objects.get(pk=id)

            if (not Student.objects.filter(admission_number=adm_num).exists()):
                return Response({ "Error": "Invalid Admission Number" , "Message": "The given admission number is invalid !"}, status=status.HTTP_400_BAD_REQUEST)
            
            student = Student.objects.get(admission_number=adm_num)

            if (student not in subject.students.all()):
                return Response({ "Error": "Unauthorized" , "Message": "Student not added to subject"}, status=status.HTTP_401_UNAUTHORIZED)

            if (request.user.is_student and request.user != student.user):
                return Response({ "Error": "Unauthorized" , "Message": "User not authorized to view progress"}, status=status.HTTP_401_UNAUTHORIZED)
            
            res = list()
            for sub in AssessmentSubmission.objects.filter(student=student, assessment__subject=subject).order_by('submitted_on'):
                ass = sub.assessment.__dict__
                ass['mark'] = sum(qa.mark for qa in QAGrade.objects.filter(submission=sub))
                res.append(ass)

            serializer = self.serializer_class(data=res, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)


'''
Suggest LO for each student for each subject
Inputs admission number and gives subject id as param
Checks:
Subject ID
Admission Number
If user is faculty / is the owner of profile
If admission number part of profile
'''
class LOImprove(generics.GenericAPIView):
    serializer_class = LOImproveSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Learning Outcomes to be improved for each student for each subject",
                         responses={ 200: 'Data Retrieved Successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})

    def get(self, request, id, adm_num):

        try:
            if (not Subject.objects.filter(pk=id).exists()):
                return Response({ "Error": "Invalid ID" , "Message": "The given subject does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

            subject = Subject.objects.get(pk=id)

            if (not Student.objects.filter(admission_number=adm_num).exists()):
                return Response({ "Error": "Invalid Admission Number" , "Message": "The given admission number is invalid !"}, status=status.HTTP_400_BAD_REQUEST)
            
            student = Student.objects.get(admission_number=adm_num)

            if (student not in subject.students.all()):
                return Response({ "Error": "Unauthorized" , "Message": "Student not added to subject"}, status=status.HTTP_401_UNAUTHORIZED)

            if (request.user.is_student and request.user != student.user):
                return Response({ "Error": "Unauthorized" , "Message": "User not authorized to view progress"}, status=status.HTTP_401_UNAUTHORIZED)
            
            res = list()
            for lo in LearningOutcome.objects.filter(subject=subject):
                for q in lo.questions.all():
                    if q.qagrades.filter(submission__student=student).exists():
                        if lo.id in [k['id'] for k in res]:
                            ind = next((index for (index, d) in enumerate(res) if d['id'] == lo.id), None)
                            res[ind]['mark'] += sum(qa.mark for qa in q.qagrades.filter(submission__student=student))
                        else:
                            lo_dict = lo.__dict__
                            lo_dict['mark'] = sum(qa.mark for qa in q.qagrades.filter(submission__student=student))
                            res.append(lo_dict)
            
            res = sorted(res, key=lambda k: k['mark'])

            serializer = self.serializer_class(data=res, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_409_CONFLICT)

'''
Suggest LOs for a question based on LOs of the given subject
Checks:
If subject ID is valid
'''
class LOSuggest(generics.GenericAPIView):
    serializer_class = LOSuggestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Learning Outcomes Suggestion",
                         responses={ 200: 'Data Retrieved Successfully',
                                400: 'Given data is invalid',
                                401: 'Unauthorized request'})
    
    def post(self, request, id):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            question = serializer.data['question']

            if (not Subject.objects.filter(pk=id).exists()):
                return Response({ "Error": "Invalid ID" , "Message": "The given subject does not exist!"}, status=status.HTTP_400_BAD_REQUEST)

            subject = Subject.objects.get(pk=id)

            if (request.user != subject.created_by.user):
                return Response({ "Error": "Unauthorized" , "Message": "User not owner of the subject"}, status=status.HTTP_401_UNAUTHORIZED)

            try:
                los = [{'name': lo.name, 'id': lo.id} for lo in LearningOutcome.objects.filter(subject=subject)]
                los_names = [lo['name'] for lo in los]
                los_names.insert(0, question)
                if len(los) > 1:
                    lo = los[suggest_lo(los_names)]
                else:
                    lo = None
                return Response({'Success': "Data Obtained Successfully", "Data": lo}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({ "Error": type(e).__name__ , "Message": str(e)}, status=status.HTTP_400_BAD_REQUEST)    

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
