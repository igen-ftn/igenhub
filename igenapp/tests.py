from django.test import TestCase, RequestFactory, Client
from .models import *
from .forms import *
from .views import *
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

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

class CommentTests(TestCase):
    """Preparing data"""
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="commentUser", password="comment", email="comment@gmail.com")
        self.repository = Repository.objects.create(author=self.user, repo_name="repo1",
                                                    owner_name=self.user.username, type='L')
        self.issue = Issue.objects.create(title="Some Issue 1", text="This is the second issue", ordinal=101,
                                          date=timezone.now(), status='O', user=self.user, repository=self.repository)
        self.comment = Comment.objects.create(user=self.user, issue=self.issue, content="test test test",
                                              date=timezone.now())
    """Test if comment is created properly"""
    def test_create_comment(self):
        self.assertTrue(isinstance(self.comment, Comment))
        self.assertIsNotNone(self.comment.content)
        self.assertIsNotNone(self.comment.user)
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.content, "test test test")
        self.assertEqual(self.comment.issue, self.issue)
        self.assertIsNotNone(self.comment.date)
    """Test if correct view is called and if it returns status 200"""
    def test_comment_view(self):
        request = self.factory.get('/' + self.user.username + '/' + self.repository.repo_name + '/issues' + '/' + str(self.comment.issue.id))
        request.user = self.user
        response = issue_details(request, self.comment.issue.repository.owner_name, self.comment.issue.repository.repo_name, self.comment.issue.id)
        self.assertEqual(response.status_code, 200)

    def test_url(self):
        url = reverse('issue_details',
                      args=[self.comment.user.username, self.comment.issue.repository.repo_name, self.comment.issue.id])
        url_build = "/" + self.comment.user.username + "/" + self.comment.issue.repository.repo_name + "/issues/" + str(self.comment.issue.id) + "/"
        self.assertEqual(url, url_build)

    def test_edit_comment(self):
        edit_com = Comment.objects.get(id=self.comment.id)
        edit_com.content = "edited"
        edit_com.save()
        edited_comment = Comment.objects.get(id=self.comment.id)
        self.assertEqual(edited_comment.content, "edited")

    def test_delete_comment(self):
        del_com = Comment.objects.get(id=self.comment.id)
        checkid = self.comment.id
        del_com.delete()
        self.assertRaises(Comment.DoesNotExist, Comment.objects.get, id = checkid)
        self.assertFalse(Comment.objects.filter(id=checkid).exists())


class TasksTests(TestCase):

    """Preparing data"""
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="user2", password="user2", email="user2@gmail.com")
        self.repository = Repository.objects.create(author=self.user, repo_name="repo2",
                                                    owner_name=self.user.username, type='L')
        self.task = Task.objects.create(title="Task Ex", description="This is a example task", status='0%', user=self.user, repository=self.repository)


    """Creating new task test"""
    def test_create_task(self):
        self.assertTrue(isinstance(self.task, Task))
        self.assertEqual(self.task.description, "This is a example task")
        self.assertEqual(self.task.title, "Task Ex")
        self.assertEqual(self.task.status, "0%")
        self.assertEqual(self.task.user.username, "user2")

    """View test"""
    def test_tasks_view(self):
        request = self.factory.get('/' + self.user.username + '/' + self.repository.repo_name + '/tasks')
        request.user = self.user
        response = task(request, self.user.username, 'repo2')
        self.assertEqual(response.status_code, 200)

    """task form test"""
    def test_task_form(self):
        data = {'title': "Task one", 'description': "do this", 'status':'0%', 'user':self.user.id}
        form = TaskForm(data=data)
        self.assertTrue(form.is_valid())

        data = {'title': "", 'description': "Mr. Slave", 'status':'0%'}
        form = WikiForm(data=data)
        self.assertFalse(form.is_valid())

    """User adding task test"""
    def test_adding_task(self):
        # Log in
        self.client.force_login(self.user)

        # Go to Tasks page
        url = '/' + self.user.username + '/' + self.repository.repo_name + '/tasks/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # There should be one task
        self.assertQuerysetEqual(response.context['tasks'], ['<Task: Task object>'])

        # Create task
        url = '/' + self.user.username + '/' + self.repository.repo_name + '/task-form/'
        response = self.client.post(url, {'title': "Task", 'description': "Do this and that.", 'status': "0%", 'user':self.user.id})
        self.assertEqual(response.status_code, 302)

        # Go back to the tasks page
        url = '/' + self.user.username + '/' + self.repository.repo_name + '/tasks/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Repository list should not be empty and should have size 2
        self.assertEqual(len(response.context['tasks'].all()), 2)

        # Log out
        self.client.logout()


class WikiTests(TestCase):

    """Preparing data"""
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username="user3", password="user3", email="user3@gmail.com")
        self.repository = Repository.objects.create(author=self.user, repo_name="repo3",
                                                    owner_name=self.user.username, type='L')
        self.wiki = WikiPage.objects.create(title="Wiki Ex", content="This is a example wiki", repository=self.repository)


    """Creating new wikipage test"""
    def test_create_wiki(self):
        self.assertTrue(isinstance(self.wiki, WikiPage))
        self.assertEqual(self.wiki.content, "This is a example wiki")
        self.assertEqual(self.wiki.title, "Wiki Ex")
        self.assertEqual(self.wiki.repository.repo_name, "repo3")

    """View test"""
    def test_wiki_view(self):
        request = self.factory.get('/' + self.user.username + '/' + self.repository.repo_name + '/wiki')
        request.user = self.user
        response = wiki(request, self.user.username, 'repo3')
        self.assertEqual(response.status_code, 200)

    """Wiki form test"""
    def test_wiki_form(self):
        data = {'title': "Wikiliks", 'content': "Lemiviks"}
        form = WikiForm(data=data)
        self.assertTrue(form.is_valid())

        data = {'title': "", 'content': "Mr. Slave"}
        form = WikiForm(data=data)
        self.assertFalse(form.is_valid())

    """User adding wiki test"""
    def test_adding_wiki(self):
        # Log in
        self.client.force_login(self.user)

        # Go to wiki
        url = '/' + self.user.username + '/' + self.repository.repo_name + '/wiki/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # There should be one wiki
        self.assertQuerysetEqual(response.context['wikipages'], ['<WikiPage: WikiPage object>'])

        url = '/' + self.user.username + '/' + self.repository.repo_name + '/wiki-form/'
        response = self.client.post(url, {'title':"asdfff", 'content':"idnjdfnsdf jfsd sdfo"})
        self.assertEqual(response.status_code, 302)

        # Go back to the tasks page
        url = '/' + self.user.username + '/' + self.repository.repo_name + '/wiki/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        # Repository list should not be empty and should have size 2
        self.assertEqual(len(response.context['wikipages'].all()), 2)

        # Log out
        self.client.logout()
