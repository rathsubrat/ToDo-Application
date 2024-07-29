from django.contrib import admin
from .models import Task,Card,UserProfile,Project,Message
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','taskName', 'taskStatus','description','file','cover')  # Fields to display in the list view
    list_filter = ('taskStatus','task_wallet')          # Filters for the list view
    search_fields = ('taskName',)          # Fields to search in the list view
    filter_horizontal = ('assignedTo','assigned_groups')  # Use a filter horizontal widget for many-to-many fields


admin.site.register(Task,TaskAdmin)
class CardAdmin(admin.ModelAdmin):
    list_display = ['id','card_name']
admin.site.register(Card,CardAdmin)

class AccountInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Details'

class UserAdmin(UserAdmin):
    inlines = (AccountInline,)


admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(UserProfile)
admin.site.site_header = "To Do Application"
admin.site.index_title = "To Do Application"
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id','projname']
    filter_horizontal = ('assignedTo',)

admin.site.register(Project,ProjectAdmin)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['id','user','task']
admin.site.register(Message,MessageAdmin)

