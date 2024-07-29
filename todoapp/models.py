from django.db import models
from django.contrib.auth.models import User,Group
from django.db.models import Count
from django.db.models import JSONField
# Create your models here.


class Project(models.Model):
    projname = models.CharField(max_length=100)
    assignedTo = models.ManyToManyField(User, related_name='assigned_project')
    proj_date = models.DateField(blank=True,null=True)
    def __str__(self):
        return self.projname
class Card(models.Model):
    card_name = models.CharField(max_length=30)
    def __str__(self):
        return self.card_name
class Task(models.Model):
    taskName = models.CharField(max_length=255,null=True, blank=True)
    # status = models.CharField(max_length=50,null=True, blank=True) this used in version 1.0 for making simple text field
    taskStatus = models.ForeignKey(Card, on_delete=models.CASCADE)
    assignedTo = models.ManyToManyField(User, related_name='tasks')
    assigned_groups = models.ManyToManyField(Group, related_name='group_tasks',blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True)
    description = models.CharField(max_length=100,null=True)
    start_date = models.DateField(null=True, blank=True)
    done_date = models.DateField(null=True, blank=True)
    file = models.FileField(max_length=100, upload_to="media/", null=True, blank=True)
    Priority_High = 'high'
    Priority_Medium = 'medium'
    Priority_Low = 'low'

    MY_CHOICES = [
        (Priority_High, 'high'),
        (Priority_Medium, 'medium'),
        (Priority_Low, 'low'),
    ]

    # Define the model field with choices

    priority = models.CharField(
        max_length=20,
        choices=MY_CHOICES,
        default=Priority_Low,
    )
    checklist = models.TextField(default="Not Available",null=True, blank=True)
    cover = models.CharField(max_length=100, default='#ffffff', null=True, blank = True)
    tech_stack = models.CharField(max_length=50, null=True, blank=True)
    task_wallet = models.IntegerField(null=True,blank=True)
    is_flaged = models.BooleanField('Flaged',default=False)
    approvals = models.BooleanField('Approved',default=False)
    ETA = JSONField(default=list, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if done_date has changed
        if self.pk is not None:
            orig = Task.objects.get(pk=self.pk)
            if orig.done_date != self.done_date:
                if self.ETA is None:
                    self.ETA = []
                # Append the new done_date as a string
                self.ETA.append(self.done_date.strftime("%Y-%m-%d"))
        super(Task, self).save(*args, **kwargs)
    def __str__(self):
        return self.taskName

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    proficiency = models.CharField(max_length=50,null=True,blank=True,
                                   choices=[('Basic', 'Basic'),('Good', 'Good'), ('Excellent', 'Excellent')],default=('Basic'))
    tech_stack = models.CharField(max_length=50,null=True,blank=True)
    role = models.CharField(max_length=50,null=True,blank=True,
                              choices=[('UI/UX Designer','UI/UX Designer'),('Backend Developer ','Backend Developer'),('Full Stack Developer ','Full Stack Developer'),('Cloud Developer ','Cloud Developer')])
    designation = models.CharField(max_length=50,
                              choices=[('User', 'User'),('Manager', 'Manager'), ('Team Lead', 'Team Lead')],default=('User'))
    wallet_money = models.IntegerField(null=True,blank=True,default=0)

class Message(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField(max_length=5000)
    date_time = models.DateTimeField()










