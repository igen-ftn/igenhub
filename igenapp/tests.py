from django.test import TestCase, RequestFactory
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
        self.issue = Issue.objects.create(title="Some Issue", text="This is first issue", ordinal=100,
                                          date=timezone.now(), status='O', user=self.user)
        self.repository = Repository.objects.create(author=self.issue.user, repo_name="repo",
                                                    owner_name=self.issue.user.username, type='L')

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


class RepositoryTests(TestCase):

    """Preparing data"""
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="user", password="user", email="user@gmail.com")
        self.contributor = User.objects.create(username="contributor", password="contributor", email="contributor@gmail.com")
        self.repository = Repository.objects.create(author=self.user, repo_name="repo",
                                                    owner_name=self.user.username, type='L')

    """Creating new issue test"""
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