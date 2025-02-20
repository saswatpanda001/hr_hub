from django.urls import path,include
from hub import views
app_name = "hub"

urlpatterns = [
    path("",views.home,name="landing"),
    path('login/employee/', views.EmployeeLoginView.as_view(), name='employee_login'),
    path('login/hrmanager/', views.HrManagerLoginView.as_view(), name='hrmanager_login'),
    path('login/candidate/', views.CandidateLoginView.as_view(), name='candidate_login'),
    path('role_login/', views.role_based_redirect, name='role_redirect'),
    
    path('login_dashbaord/', views.login_dashboard, name='login_dashboard'),
    path('dashboard', views.redirect_dashboard,name="dashboard_redirect"),
    path('dashboard/employee', views.employee_dashboard, name='employee_dashboard'),
    path('dashbaord/candidate', views.candidate_dashboard, name='candidate_dashboard'),
    path('dashbaord/hr', views.hr_dashboard, name='hr_dashboard'),
    
    path('profile',views.profile,name="profile"),
    path('profile/edit', views.edit_profile, name='edit_profile'),
    path('jobs/', views.jobs_available, name='jobs'),
    path("create_job/", views.JobCreateView.as_view(), name="job-create"),
    path("edit_job/<int:pk>/", views.JobUpdateView.as_view(), name="job-edit"),
    path("job/<int:pk>/", views.JobDetailView.as_view(), name="job-detail"),

    path("notifications", views.notifications_view, name="notifications"),
    path("notifications/create", views.create_notification, name="create_notifications"),
    path('notifications/delete/<int:pk>/', views.delete_notification, name='delete_notification'),
    path("apply/<int:id>/", views.apply_for_job, name="apply"),

     
    path("applications/job/<int:id>", views.applications, name="applications"),
    path("applications/<int:id>", views.application_details, name="application_details"),
    path("applications/user", views.my_applications, name="my_applications"),
    path("shortlisted/", views.shortlisted, name="shortlisted"),

    path('applications/<int:job_id>/<int:app_id>/reject/', views.reject_application, name='reject_application'),
    path('applications/<int:job_id>/<int:app_id>/shortlist/', views.shortlist_application, name='shortlist_application'),
]

