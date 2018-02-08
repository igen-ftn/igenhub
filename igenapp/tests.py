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

class CommentTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="commentUser", password="comment", email="comment@gmail.com")
        self.repository = Repository.objects.create(author=self.user, repo_name="repo1",
                                                    owner_name=self.user.username, type='L')
        self.issue = Issue.objects.create(title="Some Issue 1", text="This is the second issue", ordinal=101,
                                          date=timezone.now(), status='O', user=self.user, repository=self.repository)
        self.comment = Comment.objects.create(user=self.user, issue=self.issue, content="test test test",
                                              date=timezone.now())
    def test_create_comment(self):
        self.assertTrue(isinstance(self.comment, Comment))
        self.assertIsNotNone(self.comment.content)
        self.assertIsNotNone(self.comment.user)
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.content, "test test test")
        self.assertEqual(self.comment.issue, self.issue)
        self.assertIsNotNone(self.comment.date)

    def test_comment_view(self):
        request = self.factory.get('/' + self.user.username + '/' + self.repository.repo_name + '/issues' + '/' + str(self.comment.issue.id))
        request.user = self.user
        response = issue_details(request, self.comment.issue.repository.owner_name, self.comment.issue.repository.repo_name, self.comment.issue.id)
        self.assertEqual(response.status_code, 200)