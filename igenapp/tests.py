from django.test import TestCase, RequestFactory, Client
from .models import *
from .forms import *
from .views import *
from django.utils import timezone
from django.contrib.auth.models import User


class IssueTests(TestCase):

    """Preparing data"""
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="user", password="user", email="user@gmail.com")
        self.repository = Repository.objects.create(author=self.user, repo_name="repo",
                                                    owner_name=self.user.username, type='L')
        self.issue = Issue.objects.create(title="Some Issue", text="This is first issue", ordinal=100,
                                          date=timezone.now(), status='O', user=self.user, repository=self.repository)

    """Creating new issue test"""
    def test_create_issue(self):
        self.assertTrue(isinstance(self.issue, Issue))
        self.assertEqual(self.issue.text, "This is first issue")
        self.assertEqual(self.issue.title, "Some Issue")
        self.assertNotEqual(self.issue.ordinal, 99)
        self.assertEqual(self.issue.user.username, "user")
        self.assertIsNone(self.issue.milestone)

    """View test"""
    def test_issue_view(self):
        request = self.factory.get('/' + self.user.username + '/' + self.repository.repo_name + '/issues')
        request.user = self.user
        response = issues(request, self.user.username, 'repo')
        self.assertEqual(response.status_code, 200)

    """Issue form test"""
    def test_issue_form(self):
        data = {'title': "Issue", 'text': "This is form body", 'milestone': "null"}
        form = IssueForm(data=data)
        self.assertTrue(form.is_valid())

        data = {'title': "", 'text': "This is form body", 'milestone': "null"}
        form = IssueForm(data=data)
        self.assertFalse(form.is_valid())

    """User activity test"""
    def test_activity(self):
        # Log in
        self.client.force_login(self.user)

        # Go to Repositories page
        url = '/' + self.user.username + '/repositories/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # There should be no activity
        self.assertQuerysetEqual(response.context['activity'], [])

        # Create issue
        url = '/' + self.user.username + '/' + self.repository.repo_name + '/add_issue/0/'
        response = self.client.post(url, {'title': "Issue", 'text': "This is form body", 'milestone': "null"})
        self.assertEqual(response.status_code, 200)

        # Go back to the repository page
        url = '/' + self.user.username + '/repositories/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Activity set should not be empty
        self.assertQuerysetEqual(response.context['activity'], ['<Activity: Activity object>'])

        # Log out
        self.client.logout()
