import json
import time

import requests
from django.http import FileResponse,HttpResponseRedirect,HttpResponse
from django.core.serializers import serialize
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser
from rest_framework import status
from rest_framework.decorators import api_view
from todoapp.serializers import *
from django.contrib.auth.decorators import login_required, user_passes_test
from todoapp.models import Task,Card
from .utils import save_project_data_as_text
from .decorators import manager_required,teamlead_required
from rest_framework import permissions
from django.core.mail import send_mail,EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Count,Q
from urllib.parse import urlencode
# Create your views here.
@api_view(['POST'])
def create_task(request):
    if request.method == 'POST':
        data = request.data
        auto_assign = data.get('auto_assign', False)

        assigned_user_id = None
        if auto_assign:
            project_name = data.get('project')
            tech_stack = data.get('tech_stack', [])

            # Find project
            try:
                project = Project.objects.get(projname=project_name)
            except Project.DoesNotExist:
                return Response({"detail": "Project not found."}, status=status.HTTP_404_NOT_FOUND)

            # Create a Q object for tech stack filtering
            tech_stack_filter = Q()
            for tech in tech_stack:
                tech_stack_filter |= Q(userprofile__tech_stack__icontains=tech)

            # Find users related to the project with matching tech stack
            project_users = User.objects.filter(assigned_project=project).filter(tech_stack_filter)

            if project_users.exists():
                # Find users with matching tech stack in the project with the least number of tasks assigned
                assigned_user = project_users.annotate(task_count=Count('tasks')).order_by('task_count').first()
            else:
                # Find users with matching tech stack in UserProfile
                tech_stack_users = User.objects.filter(tech_stack_filter)

                if tech_stack_users.exists():
                    # Find users with matching tech stack in the whole system with the least number of tasks assigned
                    assigned_user = tech_stack_users.annotate(task_count=Count('tasks')).order_by('task_count').first()
                else:
                    # Find users with the least number of tasks assigned if no matching tech stack users found
                    assigned_user = User.objects.annotate(task_count=Count('tasks')).order_by('task_count').first()

            # Get the user ID of the assigned user
            if assigned_user:
                assigned_user_id = assigned_user.id

        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            task = serializer.save()  # Save the Task object first

            # Add the assigned user to the many-to-many relationship
            if assigned_user_id:
                task.assignedTo.set([assigned_user_id])
                task.save()  # Save again to ensure changes persist

            # Serialize the task again to include the updated assigned user
            task.refresh_from_db()
            serializer = TaskSerializer(task)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response({"detail": "Method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # permission_classes = [permissions.IsAdminUser]  # Only admin users can delete tasks
    # @method_decorator(manager_required) #for manager
    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class UserListView(generics.ListAPIView):
    # permission_classes = [permissions.IsAdminUser]  # Only admin users can delete tasks
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_mail(
                'User Created Successfully',
                f'''Hi {user.username},

Welcome to Bourntec ToDo Application!

We’re excited to have you on board. Below are your login credentials:

Username: {user.username}


Please make sure to change your password upon your first login for security purposes. If you have any questions or need assistance, feel free to reach out to our support team.

Thank you for choosing Bourntec!

Best regards,
The Bourntec Team''',

                'Bourntec Solutions',
                [user.email],
                fail_silently=False,
            )
            time.sleep(1)
            forgot_password_url = f'http://127.0.0.1:8000/todo/forgot_password/{user.username}/'
            requests.post(forgot_password_url)

            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

admin_required = user_passes_test(lambda user: user.is_superuser)
class LoginView(APIView):
    # permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user is not None:
            try:
                user_profile = user.userprofile
                tech_stack = user_profile.tech_stack
                role = user_profile.role
            except AttributeError:
                return Response({'error': 'User profile data is incomplete'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if user.is_superuser:
                query_params = urlencode({
                    'userid': user.username,
                    'email': user.email,
                    'techstack': tech_stack,
                })
                redirect_url = f'https://www.bourntec.com/'
            elif role == "Manager":
                query_params = urlencode({
                    'userid': user.id,
                    'email': user.email,
                    'techstack': tech_stack,
                })
                redirect_url = f'http://localhost:3000/manager/?{query_params}'
            else:
                query_params = urlencode({
                    'userid': user.id,
                    'email': user.email,
                    'techstack': tech_stack,
                })
                redirect_url = f'http://localhost:3000/user/?{query_params}'

            # Return JavaScript to open the URL
            response_html = f'<script>window.location="{redirect_url}";</script>'
            return HttpResponse(response_html, content_type='text/html')
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
class UpdateDateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = MyModelSerializer
class UpdateDescriptionView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = Update_Description

class UpdateStatusView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = Update_Status

class UpdateNameView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = Update_Name

# @api_view(['PUT'])
# def create_or_update_tasks(request):
#     if request.method == 'PUT':
#         data = json.loads(request.body)  # Assuming JSON data is sent in the request body
#         task = Task.objects.get(pk=data["project_id"])
#         d = {}
#         for k,v in data.items():
#             d[k]=v
#         task.checklist = str(d)
#         task.save()
#     return JsonResponse({'message': 'Tasks created/updated successfully'}, status=200)
# # else:
#     return JsonResponse({'error': 'Invalid request method'}, status=400)
# class create_or_update_tasks(generics.UpdateAPIView):
#     queryset = Task.objects.all()
#     serializer_class = Update_Checklist
#views for save checklists
@api_view(['POST'])
def save_data_view(request,id):
    if request.method == 'POST':
        try:
            # Assume the JSON data is sent in the body of the request
            json_data = json.loads(request.body)
            save_project_data_as_text(id,json_data)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)})
    else:
        return JsonResponse({'status': 'failed', 'message': 'Only POST requests are allowed'})

class ImageUpdateView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def put(self, request, pk):
        try:
            image_instance = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UploadedFileSerializer(image_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#Delete User
class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDeleteSerializer
    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response({"msg":"User Deleted Successfully"},status=status.HTTP_204_NO_CONTENT)
class TaskListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            # Return all tasks for superusers
            return Task.objects.all()
        else:
            # Return only approved tasks for regular users
            return Task.objects.filter(approvals='approved')
class TaskDetailView(APIView):
    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task)
        return Response(serializer.data)
class CoverUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = UpdateCoverColorSerializer

@api_view(['POST'])
# @admin_required
# @login_required
def create_group(request):
    if request.method == 'POST':
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CardListView(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

@api_view(['POST'])
# @login_required
def create_card(request):
    if request.method == 'POST':
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUserView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DownloadAttachmentView(APIView):

    def get(self, request, pk, format=None):
        attachment = get_object_or_404(Task, pk=pk)
        response = FileResponse(attachment.file.open(), as_attachment=True, filename=attachment.name)
        return response

class attachment_delete_view(APIView):
    def delete(self, request, pk, format=None):
        attachment = get_object_or_404(Task, pk=pk)
        attachment.file.delete()  # Delete the file from the storage
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['POST'])
def create_project(request):
    if request.method == 'POST':
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ForgotPasswordView(APIView):
    def post(self, request, username):
        try:
            user = User.objects.get(username=username)
            token = default_token_generator.make_token(user)
            reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': user.pk, 'token': token}))
            send_mail(
                'Password Reset Request',
                f'Use the link below to reset your password:\n{reset_url}',
                'Password Reset Bourntec ToDo',
                [user.email],
                fail_silently=False,
            )
            return Response({"message": "Password reset link sent to your email."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

class PasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):
        serializer = PasswordResetConfirmSerializer(data={
            'uidb64': uidb64,
            'token': token,
            'new_password': request.data.get('new_password')
        })
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectListAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        project_data = []

        for project in projects:
            # Filter tasks related to this project
            tasks = Task.objects.filter(project=project)

            # Count the total number of tasks
            total_tasks = tasks.count()

            # Count tasks by status
            completed_tasks = tasks.filter(taskStatus__card_name='Done').count()
            # in_progress_tasks = tasks.filter(taskStatus__card_name='In Progress').count()
            # test_tasks = tasks.filter(taskStatus__card_name='Test').count()
            # other_tasks = tasks.filter(taskStatus__card_name='Other').count()

            # Calculate completion percentage
            if total_tasks == 0:
                completion_percentage = 0
            else:
                completion_percentage = round((completed_tasks / total_tasks) * 100.0)

            # Append project data to the list
            project_data.append({
                'id': project.id,
                'name': project.projname,
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                # 'in_progress_tasks': in_progress_tasks,
                # 'test_tasks': test_tasks,
                # 'other_tasks': other_tasks,
                'completion_percentage': completion_percentage,
            })

        return Response(project_data, status=status.HTTP_200_OK)


class UserProjectTasksView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        tasks = Task.objects.filter(assignedTo=user)

        task_data = []

        for task in tasks:
            task_serializer = TaskSerializer(task)
            task_info = task_serializer.data
            task_info['project_name'] = task.project.projname
            task_data.append(task_info)

        return Response(task_data, status=status.HTTP_200_OK)



