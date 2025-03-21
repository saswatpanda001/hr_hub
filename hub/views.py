from django.shortcuts import render
from django.shortcuts import render, redirect
from allauth.account.views import LoginView
from django.views.generic import UpdateView,CreateView, DetailView,ListView
from django.contrib.auth.decorators import login_required
from hub.models import UserProfile, Job, Notifications, Qualifications, Skills, Application, Interview
from hub.forms import UserProfileForm, InterviewForm
from django.views.generic import CreateView
from django.urls import reverse_lazy
from hub.models import Job, Notifications
from hub.forms import JobForm, NotificationForm
from django.utils import timezone
import random
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Application
from django.contrib import messages

@login_required
def applications(request, id):
    profile = UserProfile.objects.filter(user=request.user)[0]
    applications = Application.objects.filter(job=id)
    data = {"applications":applications}

    return render(request, "applications.html",data)

    

@login_required
def application_details(request,id):
    if request.user.last_name == "HR":
        applications = Application.objects.filter(id=id)[0]
        data = {"application":applications}
        print(data["application"])
        return render(request, "application_details.html",data)
    else:
        return render(request, "error.html")
    
    

@login_required
def my_applications(request):
    profile = UserProfile.objects.filter(user=request.user)[0]
    my_applications = Application.objects.filter(applicant=profile)
    data = {"applications":my_applications}
    return render(request, "my_applications.html",data)

    
@login_required
def shortlisted(request):
    applications = Application.objects.filter(status="Shortlisted")
    choices = Application.choices  # Correcting the choices reference
    return render(request, "my_applications.html", {"applications": applications, "choices": choices})

@login_required
def rejected_applicants(request):
    applications = Application.objects.filter(status="Rejected")
    return render(request, "rejected_applicants.html", {"applications": applications})


@login_required
def update_status(request, application_id):
    if request.method == "POST":
        new_status = request.POST.get("status")
        application = get_object_or_404(Application, id=application_id)
        application.status = new_status
        application.save()

        if new_status == "Hired":
            return redirect("hub:hired_applicants")
        elif new_status == "Rejected":
            return redirect("hub:rejected_applicants")
        elif new_status == "Interview Scheduled":
            return redirect("hub:interview_scheduled_applicants")
        else:
            return redirect("hub:shortlisted")

def hired_applicants(request):
    applications = Application.objects.filter(status="Hired")
    return render(request, 'hired_applicants.html', {'applications': applications})

@login_required
def interview_scheduled_applicants(request):
    applications = Application.objects.filter(status="Interview Scheduled")
    return render(request, "interview_scheduled_applicants.html", {"applications": applications})


def update_interview(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if request.method == 'POST':
        interview_date = request.POST.get('interview_date')
        interview_location = request.POST.get('interview_location')
        interview_notes = request.POST.get('interview_notes')
        feedback = request.POST.get('feedback')

        # Update application with form data
        application.interview_date = interview_date
        application.interview_location = interview_location
        application.interview_notes = interview_notes
        application.feedback = feedback
        application.save()

        return redirect('hub:application_details', application.id)
    
    return render(request, 'hub/application_details.html', {'application': application})






@login_required
def schedule_interview(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()
            application.status = 'Interview Scheduled'
            application.save()
            return redirect('shortlisted')
    else:
        form = InterviewForm()

    return render(request, 'schedule_interview.html', {'form': form, 'application': application})



@login_required
def apply_for_job(request,id):
    
    job = Job.objects.filter(id=id)
    print(job)
    if request.user.last_name not in  ["Employee", "Candidate"]:
        return render(request,"error.html")

    elif len(job)==0:
        return render(request,"error.html")
    
    else:
        job_data = job[0]
        applicant_data = UserProfile.objects.filter(user=request.user)[0]

        if request.method == "POST":
            work_history = request.POST.get("work_history")
            expected_salary = request.POST.get("expected_salary")
            address = request.POST.get("address")
            city = request.POST.get("city")
            state = request.POST.get("state")
            country = request.POST.get("country")
            phone = request.POST.get("phone")
            email = request.POST.get("email")
            age = request.POST.get("age")
            linkedin_url = request.POST.get("linkedin_url")
            github_url = request.POST.get("github_url")
            bio = request.POST.get("bio")
            resume = request.FILES.get("resume")
            skills = request.POST.getlist("skills")  # Get multiple selected skills
            qualifications = request.POST.getlist("qualifications")  # Get multiple selected qualifications

            

            # Create application
            application = Application.objects.create(
                applicant=applicant_data,  # Assuming UserProfile exists
                job=job_data,
                work_history=work_history,
                expected_salary=expected_salary,
                address=address,
                city=city,
                state=state,
                country=country,
                phone=phone,
                email=email,
                age=age,
                linkedin_url=linkedin_url,
                github_url=github_url,
                bio=bio,
                resume=resume
            )

            # Add ManyToMany relationships (Skills & Qualifications)
            application.skills.set(skills)  # Assign selected skills
            application.qualifications.set(qualifications)  # Assign selected qualifications

            return redirect("hub:jobs")  # Redirect after successful submission

        # Fetch required data for the form
        jobs = Job.objects.all()
        skills = Skills.objects.all()
        qualifications = Qualifications.objects.all()
        
        context = {
            "jobs": jobs,
            "skills": skills,
            "qualifications": qualifications
        }
        
        return render(request, "apply.html", context)




@login_required
def create_notification(request):


    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")

       
        notification = Notifications.objects.create(
            title=title,
            description=description,
            sender=request.user.userprofile  
        )
        notification.save()

        return redirect("hub:notifications") 

    return render(request, "create_notifications.html")


def notifications_view(request):
    user_profile = UserProfile.objects.get(user=request.user)
    notf_personal = Notifications.objects.filter(sender=user_profile).order_by("-time")
    notf_all = Notifications.objects.all().order_by("-time")
    data = {"notf_all":notf_all,"notf_personal":notf_personal}

    return render(request, "notifications.html",data)

     



class JobDetailView(DetailView):
    model = Job
    template_name = "job_details.html"
    context_object_name = "job"



class JobCreateView(CreateView):
    model = Job
    form_class = JobForm
    template_name = "create_job.html"
    success_url = reverse_lazy("hub:jobs")  # Redirect to the job list page

    def form_valid(self, form):
        return super().form_valid(form)



class JobUpdateView(UpdateView):
    model = Job
    form_class = JobForm
    template_name = "edit_job.html"
    
    def get_success_url(self):
        return reverse_lazy("hub:jobs-detail", kwargs={"pk": self.object.pk})

def home(request):
    return render(request, "landing.html")

def login_dashboard(request):
    return render(request, "login_dash.html")

class EmployeeLoginView(LoginView):
    template_name = "account/internal_emp_login.html"

class HrManagerLoginView(LoginView):
    template_name = "account/hr_login.html"

class CandidateLoginView(LoginView):
    template_name = "account/external_emp_login.html"


@login_required
def role_based_redirect(request):
    user = request.user
    print("login user: ",user)
    profile_data = UserProfile.objects.filter(user=user)
    if len(profile_data)==0:
        print("no profile")
        return redirect("hub:login_dashboard")
    else:
        profile_data = profile_data[0]
        print(profile_data.role)
        if profile_data.role=="Employee":
            return redirect('hub:employee_dashboard')
        elif profile_data.role=="HR":
            return redirect('hub:hr_dashboard')
        elif profile_data.role=="Candidate":
            print("loggedin")
            return redirect('hub:candidate_dashboard')
        else:
            return redirect('hub:login_dashboard')


@login_required
def redirect_dashboard(request):
    role = request.user.last_name
    if role=="Candidate":
        return redirect('hub:candidate_dashboard')
    if role=="HR":
        return redirect('hub:hr_dashboard')
    if role=="Employee":
        return redirect('hub:employee_dashboard')
    


@login_required        
def profile(request):
    profile = UserProfile.objects.filter(user=request.user)
    if len(profile)==0:
        return render(request,"error.html")
    else:
        profile = profile[0]
        data = {"profile":profile}
        return render(request,"profile.html",data)

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('hub:profile')  # Redirect to profile page

    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'profile_edit.html', {'form': form})





@login_required
def jobs_available(request):


    jobs = Job.objects.all()
    data = {"jobs":jobs}
    return render(request, "jobs.html",data)


def delete_notification(request, pk):
    notification = Notifications.objects.get(id=pk)
    
    if request.method == "POST":
        notification.delete()
        messages.success(request, "Notification deleted successfully!")
    
    return redirect('hub:notifications')



def employee_dashboard(request):
    return render(request, "dashboard/emp_dashboard.html")


def hr_dashboard(request):
    return render(request, "dashboard/hr_dashboard.html")


def candidate_dashboard(request):
    return render(request, "dashboard/candidate_dashboard.html")





def reject_application(request,job_id,app_id):
    application = get_object_or_404(Application, id=app_id)
    application.status = "Rejected"
    application.save()
    messages.success(request, "Application has been rejected.")
    return redirect('hub:applications', job_id)

def shortlist_application(request,job_id,app_id):
    application = get_object_or_404(Application, id=app_id)
    application.status = "Shortlisted"
    application.save()
    messages.success(request, "Application has been shortlisted.")
    return redirect('hub:applications', job_id)


