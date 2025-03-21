from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from hub.models import Job, Notification, Application

User = get_user_model()

class HubViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.employee_user = User.objects.create_user(username='employee', password='password123', role='Employee')
        self.hr_user = User.objects.create_user(username='hr', password='password123', role='HR')
        self.candidate_user = User.objects.create_user(username='candidate', password='password123', role='Candidate')
        self.job = Job.objects.create(title='Software Engineer', description='Test Job', created_by=self.hr_user)
        
    def test_landing_page(self):
        response = self.client.get(reverse('hub:landing'))
        self.assertEqual(response.status_code, 200)

    def test_employee_login_view(self):
        response = self.client.post(reverse('hub:employee_login'), {'username': 'employee', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)

    def test_hr_login_view(self):
        response = self.client.post(reverse('hub:hrmanager_login'), {'username': 'hr', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)

    def test_candidate_login_view(self):
        response = self.client.post(reverse('hub:candidate_login'), {'username': 'candidate', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)

    def test_role_redirect(self):
        self.client.login(username='employee', password='password123')
        response = self.client.get(reverse('hub:role_redirect'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_redirect(self):
        self.client.login(username='hr', password='password123')
        response = self.client.get(reverse('hub:dashboard_redirect'))
        self.assertEqual(response.status_code, 302)

    def test_employee_dashboard(self):
        self.client.login(username='employee', password='password123')
        response = self.client.get(reverse('hub:employee_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_job_detail_view(self):
        self.client.login(username='hr', password='password123')
        response = self.client.get(reverse('hub:job-detail', kwargs={'pk': self.job.pk}))
        self.assertEqual(response.status_code, 200)

    def test_create_job_view(self):
        self.client.login(username='hr', password='password123')
        response = self.client.post(reverse('hub:job-create'), {'title': 'New Job', 'description': 'Job Description'})
        self.assertEqual(response.status_code, 200)

    def test_apply_for_job(self):
        self.client.login(username='candidate', password='password123')
        response = self.client.post(reverse('hub:apply', kwargs={'id': self.job.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Application.objects.filter(job=self.job, candidate=self.candidate_user).exists())



from django.test import TestCase
from django.contrib.auth.models import User
from hub.models import Skills, Qualifications, UserProfile, Job, Application, Interview, Offer, Notifications

class SkillsModelTest(TestCase):
    def test_create_skill(self):
        skill = Skills.objects.create(name="Python")
        self.assertEqual(str(skill), "Python")

class QualificationsModelTest(TestCase):
    def test_create_qualification(self):
        qualification = Qualifications.objects.create(name="B.Tech")
        self.assertEqual(str(qualification), "B.Tech")

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_create_user_profile(self):
        profile = UserProfile.objects.create(user=self.user, role="Candidate", phone="1234567890")
        self.assertEqual(str(profile), "testuser - Candidate")

class JobModelTest(TestCase):
    def test_create_job(self):
        job = Job.objects.create(title="Software Engineer", status="Open", salary=60000)
        self.assertEqual(str(job), "Software Engineer")

class ApplicationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="applicantuser", password="12345")
        self.profile = UserProfile.objects.create(user=self.user, role="Candidate")
        self.job = Job.objects.create(title="Developer", status="Open")

    def test_create_application(self):
        application = Application.objects.create(applicant=self.profile, job=self.job, status="Pending")
        self.assertEqual(application.status, "Pending")

class InterviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="interviewuser", password="12345")
        self.profile = UserProfile.objects.create(user=self.user, role="Candidate")
        self.job = Job.objects.create(title="QA Engineer", status="Open")
        self.application = Application.objects.create(applicant=self.profile, job=self.job)

    def test_create_interview(self):
        interview = Interview.objects.create(application=self.application, status="Scheduled")
        self.assertEqual(str(interview), f"Interview for {self.user.username} - {self.job.title}")

class OfferModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="offeruser", password="12345")
        self.profile = UserProfile.objects.create(user=self.user, role="Candidate")
        self.job = Job.objects.create(title="Backend Developer", status="Open")
        self.application = Application.objects.create(applicant=self.profile, job=self.job)

    def test_create_offer(self):
        offer = Offer.objects.create(application=self.application, salary_offered=70000, status="Pending")
        self.assertEqual(str(offer), f"Offer for {self.user.username} - {self.job.title}")

class NotificationsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="notifuser", password="12345")
        self.sender_profile = UserProfile.objects.create(user=self.user, role="HR")

    def test_create_notification(self):
        notification = Notifications.objects.create(title="Meeting Reminder", description="HR Meeting at 2 PM", sender=self.sender_profile)
        self.assertEqual(str(notification), "Meeting Reminder")






from django.test import TestCase, Client
from django.contrib.auth.models import User
from hub.models import UserProfile, Job, Notifications, Application, Skills, Qualifications
from django.urls import reverse


class HubViewsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user_hr = User.objects.create_user(username='hruser', password='password', last_name='HR')
        self.user_candidate = User.objects.create_user(username='candidateuser', password='password', last_name='Candidate')
        self.user_employee = User.objects.create_user(username='employeeuser', password='password', last_name='Employee')
        
        self.hr_profile = UserProfile.objects.create(user=self.user_hr, role='HR')
        self.candidate_profile = UserProfile.objects.create(user=self.user_candidate, role='Candidate')
        self.employee_profile = UserProfile.objects.create(user=self.user_employee, role='Employee')
        
        self.job = Job.objects.create(title='Software Engineer', description='Job Description', salary=60000)
        self.application = Application.objects.create(job=self.job, applicant=self.candidate_profile, status='Pending')
        self.notification = Notifications.objects.create(title='Test Notification', description='Notification Body', sender=self.hr_profile)

    # Authentication Tests
    def test_login_redirect(self):
        response = self.client.get(reverse('hub:applications', args=[self.job.id]))
        self.assertEqual(response.status_code, 302)
        
    def test_role_based_redirect_hr(self):
        self.client.login(username='hruser', password='password')
        response = self.client.get(reverse('hub:role_based_redirect'))
        self.assertRedirects(response, reverse('hub:hr_dashboard'))

    def test_role_based_redirect_candidate(self):
        self.client.login(username='candidateuser', password='password')
        response = self.client.get(reverse('hub:role_based_redirect'))
        self.assertRedirects(response, reverse('hub:candidate_dashboard'))

    def test_role_based_redirect_employee(self):
        self.client.login(username='employeeuser', password='password')
        response = self.client.get(reverse('hub:role_based_redirect'))
        self.assertRedirects(response, reverse('hub:employee_dashboard'))

    # Application Tests
    def test_view_applications(self):
        self.client.login(username='hruser', password='password')
        response = self.client.get(reverse('hub:applications', args=[self.job.id]))
        self.assertEqual(response.status_code, 200)

    def test_application_details(self):
        self.client.login(username='hruser', password='password')
        response = self.client.get(reverse('hub:application_details', args=[self.application.id]))
        self.assertEqual(response.status_code, 200)

    def test_my_applications(self):
        self.client.login(username='candidateuser', password='password')
        response = self.client.get(reverse('hub:my_applications'))
        self.assertEqual(response.status_code, 200)

    # Job Tests
    def test_create_job(self):
        self.client.login(username='hruser', password='password')
        response = self.client.get(reverse('hub:job_create'))
        self.assertEqual(response.status_code, 200)

    def test_edit_job(self):
        self.client.login(username='hruser', password='password')
        response = self.client.get(reverse('hub:job_edit', args=[self.job.id]))
        self.assertEqual(response.status_code, 200)

    def test_delete_notification(self):
        self.client.login(username='hruser', password='password')
        response = self.client.post(reverse('hub:delete_notification', args=[self.notification.id]))
        self.assertRedirects(response, reverse('hub:notifications'))

    # Notification Tests
    def test_create_notification(self):
        self.client.login(username='hruser', password='password')
        response = self.client.post(reverse('hub:create_notification'), {'title': 'New Notification', 'description': 'This is a test'})
        self.assertRedirects(response, reverse('hub:notifications'))

    def test_notification_view(self):
        self.client.login(username='hruser', password='password')
        response = self.client.get(reverse('hub:notifications'))
        self.assertEqual(response.status_code, 200)

    # Profile Tests
    def test_profile_view(self):
        self.client.login(username='candidateuser', password='password')
        response = self.client.get(reverse('hub:profile'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile(self):
        self.client.login(username='candidateuser', password='password')
        response = self.client.get(reverse('hub:edit_profile'))
        self.assertEqual(response.status_code, 200)

    # Application Status Tests
    def test_shortlist_application(self):
        self.client.login(username='hruser', password='password')
        response = self.client.post(reverse('hub:shortlist_application', args=[self.job.id, self.application.id]))
        self.application.refresh_from_db()
        self.assertEqual(self.application.status, 'Shortlisted')

    def test_reject_application(self):
        self.client.login(username='hruser', password='password')
        response = self.client.post(reverse('hub:reject_application', args=[self.job.id, self.application.id]))
        self.application.refresh_from_db()
        self.assertEqual(self.application.status, 'Rejected')


