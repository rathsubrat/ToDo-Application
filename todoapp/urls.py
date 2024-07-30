from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from todoapp.views import *
urlpatterns = [
    path('api/create-task/', create_task, name='api-create-task'),#for creating task
    path('tasks/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),#delete task by id
    path('api/login/', LoginView.as_view(), name='login'),# user and super user login
    path('api/register/', register, name='api-register'),# user and super user SignUp
    path('users/', UserListView.as_view(), name='user_name_list'),# user and super user Details
    path('update-date/<int:pk>/', UpdateDateView.as_view(), name='update-date'),# Task Update Date
    path('update-desc/<int:pk>/', UpdateDescriptionView.as_view(), name='update-desc'),# Task Update Desc
    path('update-status/<int:pk>/', UpdateStatusView.as_view(), name='update-status'),# Task Update Status
    path('update-name/<int:pk>/', UpdateNameView.as_view(), name='update_taskname'),# Task Update Task Name
    # path('api/create-or-update-tasks/<int:pk>/', create_or_update_tasks.as_view(), name='create_or_update_tasks'),
    # path('api/create-or-update-tasks/', create_or_update_tasks, name='create_or_update_tasks'),
    path('save-data/<int:id>/', save_data_view, name='category_save_data'),# Task Update Checklist
    path('file-upload/<int:pk>/', ImageUpdateView.as_view(), name='image_update'),# Task Update fileupload
    path('userdelete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),# User Delete
    path('tasks/', TaskListView.as_view(), name='login'),# All Tasks
    path('task/<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),#Task Detail By ID
    path('cover_update/<int:pk>/',CoverUpdateView.as_view(),name='update_cover'),# Task Update Cover
    path('api/create_group/', create_group, name='api_create_group'),# Create Group
    path('users_update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_profile_update'),#Update UserDetails
    path('cardname/', CardListView.as_view(), name='card_name_list'),#sending card names to user get method
    path('api/createcard/', create_card, name='api_create_task'),#for storing card name into database,
    path('api/update_user/<int:user_id>/', UpdateUserView.as_view(), name='update_user'),#for updating User Details
    path('attachments/<int:pk>/download/', DownloadAttachmentView.as_view(), name='download_attachment'),#Download Attachment
    path('attachments/<int:pk>/delete/', attachment_delete_view.as_view(), name='delete_attachment'),# Delete attachment by Task ID
    path('api/create_project/', create_project, name='api-create-project'),#for creating project
    path('projects/', ProjectListView.as_view(), name='project_name'),# All Project Name and assigned Manager
    path('forgot_password/<str:username>/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('projectper/', ProjectListAPIView.as_view(), name='project_list_api'),#Find Percentage Completion in project and Task
    path('user/<int:user_id>/tasks/', UserProjectTasksView.as_view(), name='user-project-tasks'),#Users aligned with Task
    path('project/tasks/<str:projname>/', ProjectTasksView.as_view(), name='project-tasks'),#Filter Task Project Wise
    path('comment/tasks/<str:task_name>/', TaskMessagesView.as_view(), name='tasks_Comment'),#Comment App
    path('user/tasks/<str:user_name>/', UserTaskView.as_view(), name='tasks_user'),#User Specific Tasks



]