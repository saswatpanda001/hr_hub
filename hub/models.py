from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Skills(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class Qualifications(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name



class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('HR', 'HR'),
        ('Recruiter', 'Recruiter'),
        ('Candidate', 'Candidate'),
        ('Employee', 'Employee'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Candidate')
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/',default="default_profile.png", blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    linkedin_url = models.URLField(max_length=255, blank=True, null=True)
    github_url = models.URLField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    skills = models.ManyToManyField(Skills, blank=True,related_name="user_skills")
    qualifications = models.ManyToManyField(Qualifications,blank=True,related_name="user_qualifications")

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Job(models.Model):
    status_choices = (('Open', 'Open'), ('Closed', 'Closed'))
    type = (("internal","internal"),("external","external"),("combined","combined"))
    
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    posted_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    status = models.CharField(max_length=20, choices=status_choices, default='Open', blank=True, null=True)
    qualifications = models.ManyToManyField(Qualifications, blank=True,related_name="job_qualifications")
    skills = models.ManyToManyField(Skills,blank=True,related_name="job_skills")
    type = models.CharField(max_length=100,blank=True,null=True,choices=type)
    vaccency = models.IntegerField(blank=True,null=True)
    

    def __str__(self):
        return self.title

from django.db import models
from django.utils import timezone

class Application(models.Model):
    choices = [('Pending', 'Pending'), ('Shortlisted', 'Shortlisted'), ('Rejected', 'Rejected'), ('Hired', 'Hired'), ('Interview Scheduled', 'Interview Scheduled')]
    
    applicant = models.ForeignKey(UserProfile, on_delete=models.CASCADE, blank=True, null=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)
    applied_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    status = models.CharField(max_length=20, choices=choices, default='Pending', blank=True, null=True)


    interview_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    interview_location = models.CharField(max_length=255, blank=True, null=True)
    interview_notes = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    
    
    
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    work_history = models.TextField(blank=True, null=True)
    qualifications = models.ManyToManyField(Qualifications, blank=True, related_name="applicant_qualifications")
    skills = models.ManyToManyField(Skills, blank=True, related_name="applicant_skills")
    age = models.IntegerField(blank=True, null=True)
    expected_salary = models.IntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    linkedin_url = models.URLField(max_length=255, blank=True, null=True)
    github_url = models.URLField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.city)

class Interview(models.Model):
    choices = [('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]

    application = models.OneToOneField(Application, on_delete=models.CASCADE)
    interview_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    interview_location = models.CharField(max_length=255, blank=True, null=True)
    interview_notes = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=choices, default='Scheduled')

    def __str__(self):
        return f"Interview for {self.application.applicant.user.username} - {self.application.job.title}"


class Offer(models.Model):
    choices = [('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')]
    application = models.OneToOneField(Application, on_delete=models.CASCADE, blank=True, null=True)
    salary_offered = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    joining_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    status = models.CharField(max_length=20, choices=choices, default='Pending')

    def __str__(self):
        return f"Offer for {self.application.applicant.user.username} - {self.application.job.title}"




class Notifications(models.Model):
    title = models.CharField(max_length=100,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    sender = models.ForeignKey(UserProfile,on_delete=models.CASCADE, blank=True,null=True)
    time = models.DateTimeField(default=timezone.now, blank=True, null=True)


    def __str__(self):
        return self.title
