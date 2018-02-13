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


class RepositoryTests(TestCase):

    """Preparing data"""
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="user", password="user", email="user@gmail.com")
        self.contributor = User.objects.create(username="contributor", password="contributor", email="contributor@gmail.com")
        self.repository = Repository.objects.create(author=self.user, repo_name="repo",
                                                    owner_name=self.user.username, type='L')

    """Creating new repository test"""
    def test_create_repository(self):
        self.assertTrue(isinstance(self.repository, Repository))
        self.assertEqual(self.repository.repo_name, "repo")
        self.assertEqual(self.repository.owner_name, "user")
        self.assertEqual(self.repository.type, "L")
        self.assertNotEqual(self.repository.url, 'https://github.com/igen-ftn/igenhub.git')

    """Repository form tests"""
    def test_repostories_form(self):
        data_local = {'repo_name': "Some repo name Some repo name Some repo name Some repo name Some repo name"}
        form = LocalRepositoryForm(data=data_local)
        self.assertFalse(form.is_valid())

        data_git = {'repo_url': 'https://github.com/igen-ftn/igenhub.git'}
        form = GitRepositoryForm(data=data_git)
        self.assertTrue(form.is_valid())

    """Adding new contributor"""
    def test_add_controbutors(self):
        self.repository.contributors.add(self.contributor)
        self.repository.save()
        self.assertEqual(len(self.repository.contributors.all()), 1)

    """Adding repository test"""
    def test_adding_repository(self):
        # Log in
        self.client.force_login(self.user)

        # Go to Repositories page
        url = '/' + self.user.username + '/repositories/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # There should be one repository (because of the setup method)
        self.assertQuerysetEqual(response.context['repositories'], ['<Repository: Repository object>'])

        # Go to new repository page and create one
        url = '/' + self.user.username + '/add_repository/'
        response = self.client.post(url, {'repo_type': "local", 'repo_name': "Test Repository", 'contributors': []})
        self.assertEqual(response.status_code, 302) # 302 because in the new repository method has redirect method

        # Go back to the Repositories page
        url = '/' + self.user.username + '/repositories/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Repository list should not be empty and should have size 2
        self.assertEqual(len(response.context['repositories'].all()), 2)

        # Log out
        self.client.logout()
