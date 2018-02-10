from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import requests
import simplejson as json
import re
from .models import *
from .forms import *

from django.template import RequestContext

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json
import datetime


def index(request):
    return render(request, 'igenapp/index.html')


def create_activity(request, owner_name, repo_name, text, link):
    #Activity.objects.all().delete()
    repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
    Activity.objects.create(user=request.user, text=text, date=timezone.now(), link=link, repository=repository)


def home(request, owner_name=''):
    if owner_name:
        return render(request, 'igenapp/home.html', {'owner_name': owner_name})
    else:
        return render(request, 'igenapp/home.html', {'owner_name': ''})

def graphs(request, owner_name, repo_name):
    datan = []
    repo = Repository.objects.get(repo_name=repo_name)
    issues = Issue.objects.filter(repository=repo.id)
    for i in range (6,-1,-1):
        obj = {}
        date = datetime.date.today() - datetime.timedelta(days=i)
        obj["name"] = str(date)
        issueCount = 0
        for issue in issues:
            if str(issue.date).split(" ")[0] == str(date):
                issueCount += 1
        obj["value"] = issueCount
        datan.append(obj)
    data = json.dumps(datan)
    if repo.type == 'G':
        result = requests.get('https://api.github.com/repos/%s/%s/commits' % (owner_name, repo_name))
        commits = json.loads(result.content)
        autori = dict()
        if result:
            for commit in commits:
                if commit['commit']['committer']['name'] in autori.keys():
                    autori[commit['commit']['committer']['name']] = autori[commit['commit']['committer']['name']] + 1
                else:
                    autori[commit['commit']['committer']['name']] = 0
            sredjenZaD3 = []
            for x in autori:
                obj = {}
                obj["name"] = x
                obj["value"] = autori[x]
                sredjenZaD3.append(obj)
            autori = json.dumps(sredjenZaD3)
            return render(request, 'igenapp/graphs/graphs.html',
                          {'data': data, 'commits': autori, 'owner_name': owner_name, 'repo_name': repo_name})
    return render(request, 'igenapp/graphs/graphs.html', {'data': data, 'owner_name': owner_name, 'repo_name': repo_name})

def wiki(request, owner_name, repo_name):
    wikipages_list = WikiPage.objects.all()
    return render(request, 'igenapp/wiki.html', {'wikipages': wikipages_list, 'owner_name': owner_name, 'repo_name': repo_name})
    #return render(request, 'igenapp/wiki.html')


def wiki_form(request, owner_name, repo_name):
    if request.method == "POST":
        form = WikiForm(request.POST)
        if form.is_valid():
            form.save()
            create_activity(request, owner_name, repo_name, ' created wiki page ', '/'+owner_name+'/'+repo_name+'/wiki')
            return redirect('wiki', owner_name, repo_name)
        else:
            context = dict()
            context['form'] = form
            context['message'] = "Error has occured:"
            context['owner_name'] = owner_name
            context['repo_name'] = repo_name
            return render(request, 'igenapp/wiki/form.html', context)
    else:
        form = WikiForm()
        return render(request, 'igenapp/wiki/form.html', {'form': form, 'owner_name': owner_name, 'repo_name': repo_name})


def wiki_page(request, owner_name, repo_name, wikipage_id):
    wikipage = get_object_or_404(WikiPage, pk=wikipage_id)
    comments = Comment.objects.filter(wiki=wikipage).order_by('date')
    images = UserImage.objects.all()
    return render(request, 'igenapp/wiki/page.html', {'wiki': wikipage, 'comments': comments, 'images':images,
                                                                 'owner_name': owner_name, 'repo_name': repo_name})


def remove_wikipage(request, owner_name, repo_name, wikipage_id):
    WikiPage.objects.filter(pk=wikipage_id).delete()
    create_activity(request, owner_name, repo_name, ' removed wiki page ', '/' + owner_name + '/' + repo_name + '/wiki')
    wikipage_list = WikiPage.objects.all()
    #return render(request, 'igenapp/wiki.html', {'wikipages': wikipages_list, 'owner_name': owner_name, 'repo_name': repo_name})
    return redirect('wiki', owner_name, repo_name)


def edit_wikipage(request, owner_name, repo_name, wikipage_id):
    if request.method == "POST":
        # .first() at the end turns the object into instance
        wikipage = WikiPage.objects.filter(pk=wikipage_id).first()
        form = WikiForm(request.POST, instance=wikipage)
        if form.is_valid():

            form.save()
            return redirect('wiki', owner_name, repo_name)
        else:
            context = dict()
            context['form'] = form
            context['message'] = "Error has occured:"
            context['owner_name'] = owner_name
            context['repo_name'] = repo_name
            return render(request, 'igenapp/wiki/form.html', context)
    else:
        wikipage = WikiPage.objects.filter(pk=wikipage_id).first()
        form = WikiForm(instance=wikipage)
        return render(request, 'igenapp/wiki/form.html', {'form': form, 'owner_name': owner_name, 'repo_name': repo_name})


def issues(request, owner_name, repo_name):
    repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
    issues_list = Issue.objects.filter(repository=repository).order_by('-date')
    user_list = User.objects.all() #DOBITI SAMO AUTORE
    images = UserImage.objects.all()
    milestone_list = Milestone.objects.filter(repository=repository)
    return render(request, 'igenapp/issues/issues.html', {'issues': issues_list, 'users': user_list, 'milestones': milestone_list, 'images':images,
                                                          'owner_name': owner_name, 'repo_name': repo_name })


def new_issue(request, owner_name, repo_name, issue_id):
    repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
    milestone_list = Milestone.objects.filter(repository=repository)
    label_list = Label.objects.filter(repository=repository)
    users = User.objects.all() #DOBITI SAMO AUTORE
    images = UserImage.objects.all()
    try:
        issue = Issue.objects.get(pk=issue_id)
        return render(request, 'igenapp/issues/new_issue.html', {'labels': label_list, 'milestones': milestone_list,
                                                                 'issue': issue, 'users': users, 'images':images,
                                                                 'owner_name': owner_name, 'repo_name': repo_name})
    except Issue.DoesNotExist:
        return render(request, 'igenapp/issues/new_issue.html', {'labels': label_list, 'milestones': milestone_list,
                                                                 'users': users, 'images':images,
                                                                 'owner_name': owner_name, 'repo_name': repo_name})


def add_issue(request, owner_name, repo_name, issue_id):
    if request.method == "POST":
        form = IssueForm(request.POST)
        if form.is_valid():
            if int(issue_id) != 0:
                issue_history(request, form, issue_id)

                Issue.objects.filter(pk=issue_id).update(title=form.cleaned_data['title'],
                                                         text=form.cleaned_data['text'], ordinal=1, status='O')
                issue = get_object_or_404(Issue, pk=issue_id)
                if form.cleaned_data['milestone'] == 'null':
                    issue.milestone = None
                    issue.save()
            else:
                repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
                issue = Issue(title=form.cleaned_data['title'], text=form.cleaned_data['text'], ordinal=1,
                              date=timezone.now(), status='O', user=request.user, repository=repository)
                issue.save()
                create_activity(request, owner_name, repo_name, ' created issue ' + issue.title,
                                '/' + owner_name + '/' + repo_name + '/issues')
            if form.cleaned_data['milestone'] != 'null':
                milestone = get_object_or_404(Milestone, pk=form.cleaned_data['milestone'])
                issue.milestone = milestone
                issue.save()

            issue_labels(request, issue)
            issue_assignees(request, issue)
    else:
        form = IssueForm()

    repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
    issues_list = Issue.objects.filter(repository=repository).order_by('-date')
    user_list = User.objects.all()  # DOBITI SAMO AUTORE
    milestone_list = Milestone.objects.filter(repository=repository)
    images = UserImage.objects.all()
    return render(request, 'igenapp/issues/issues.html', {'issues': issues_list, 'users': user_list, 'images':images,
                                                          'milestones': milestone_list, 'owner_name': owner_name,
                                                          'repo_name': repo_name})


def issue_labels(request, issue):
    label_list = request.POST.getlist('label')
    added_labels = [c for c in list(map(int, label_list)) if c not in
                    list(issue.label.all().values_list('id', flat=True))]
    if added_labels:
        for lab in added_labels:
            added_label = get_object_or_404(Label, pk=lab)
            create_history(request, ' added label ' + added_label.name, issue)
            issue.label.add(added_label)
    removed_labels = [c for c in list(issue.label.all().values_list('id', flat=True)) if c not in
                      list(map(int, label_list))]
    if removed_labels:
        for lab in removed_labels:
            removed_label = get_object_or_404(Label, pk=lab)
            create_history(request, ' removed label ' + removed_label.name, issue)
            issue.label.remove(removed_label)
    issue.save()


def issue_assignees(request, issue):
    assignee_list = request.POST.getlist('assignees')
    added_assignees = [c for c in list(map(int, assignee_list)) if c not in
                       list(issue.assignee.all().values_list('id', flat=True))]
    if added_assignees:
        for assignee in added_assignees:
            added_assignee = get_object_or_404(User, pk=assignee)
            create_history(request, ' assigned ' + added_assignee.username, issue)
            issue.assignee.add(added_assignee)
    removed_assignees = [c for c in list(issue.assignee.all().values_list('id', flat=True)) if c not in
                         list(map(int, assignee_list))]
    if removed_assignees:
        for assignee in removed_assignees:
            removed_assignee = get_object_or_404(User, pk=assignee)
            create_history(request, ' removed assignee ' + removed_assignee.username, issue)
            issue.assignee.remove(removed_assignee)
    issue.save()


def issue_history(request, form, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    if issue.title != form.cleaned_data['title']:
        create_history(request, ' changed title to ' + form.cleaned_data['title'], issue)
    if issue.text != form.cleaned_data['text']:
        create_history(request, ' changed description: ' + form.cleaned_data['text'], issue)
    if issue.milestone is not None:
        if str(issue.milestone.id) != form.cleaned_data['milestone']:
            if form.cleaned_data['milestone'] != 'null':
                milestone = get_object_or_404(Milestone, pk=form.cleaned_data['milestone'])
                create_history(request, ' changed milestone from ' + issue.milestone.title + ' to ' + milestone.title,
                               issue)
            else:
                create_history(request, ' removed milestone', issue)
    else:
        if form.cleaned_data['milestone'] != 'null':
            milestone = get_object_or_404(Milestone, pk=form.cleaned_data['milestone'])
            create_history(request, ' added milestone: ' + milestone.title, issue)


def create_history(request, text, issue):
    new_history = IssueHistory.objects.create(user=request.user, text=text, date=timezone.now())
    issue.history.add(new_history)
    issue.save()


def issue_details(request, owner_name, repo_name, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)
    comments = Comment.objects.filter(issue = issue).order_by('date')
    images = UserImage.objects.all()
    return render(request, 'igenapp/issues/issue_details.html', {'issue': issue, 'comments': comments, 'images':images,
                                                                 'owner_name': owner_name, 'repo_name': repo_name})


def close(request, owner_name, repo_name, issue_id):
    issue = get_object_or_404(Issue, pk=issue_id)

    if issue.status == 'O':
        issue.status = 'C'
        create_activity(request, owner_name, repo_name, ' closed issue ' + issue.title,
                        '/' + owner_name + '/' + repo_name + '/issues')
        create_history(request, ' closed issue ', issue)
    else:
        issue.status = 'O'
        create_activity(request, owner_name, repo_name, ' reopened issue ' + issue.title,
                        '/' + owner_name + '/' + repo_name + '/issues')
        create_history(request, ' reopened issue ', issue)
    issue.save()

    repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
    issues_list = Issue.objects.filter(repository=repository).order_by('-date')
    user_list = User.objects.all()  # DOBITI SAMO AUTORE
    milestone_list = Milestone.objects.filter(repository=repository)
    images = UserImage.objects.all()
    return render(request, 'igenapp/issues/issues.html', {'issues': issues_list, 'users': user_list, 'images':images,
                                                          'milestones': milestone_list, 'owner_name': owner_name,
                                                          'repo_name': repo_name})


def search(request, owner_name, repo_name):
    author = request.POST.get('author')
    milestone = request.POST.get('milestone')
    status = request.POST.get('status')

    repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
    issues_list = Issue.objects.filter(repository=repository).order_by('-date')
    if author != 'null':
        issues_list = issues_list.filter(user=author)
    if milestone != 'null':
        issues_list = issues_list.filter(milestone=milestone)
    if status != 'null':
        issues_list = issues_list.filter(status=status)

    user_list = User.objects.all()  # DOBITI SAMO AUTORE
    milestone_list = Milestone.objects.filter(repository=repository)
    images = UserImage.objects.all()
    return render(request, 'igenapp/issues/issues.html', {'issues': issues_list, 'users': user_list, 'images':images,
                                    'milestones': milestone_list, 'owner_name': owner_name, 'repo_name': repo_name})


def milestones(request, owner_name, repo_name):
    repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
    milestone_list = Milestone.objects.filter(repository=repository)
    return render(request, 'igenapp/milestones/milestones.html',
                  {'milestones': milestone_list, 'owner_name': owner_name, 'repo_name': repo_name})


def add_milestone(request, owner_name, repo_name):
    if request.method == "POST":
        form = MilestoneForm(request.POST)
        if form.is_valid():
            due_date = request.POST.get('due_date')
            repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
            if due_date == '':
                due_date = None
            Milestone.objects.create(title=form.cleaned_data['title'], description=form.cleaned_data['description'],
                                     creation_date=timezone.now(), due_date=due_date, status='O',
                                     repository=repository)
            create_activity(request, owner_name, repo_name, ' created milestone ' + form.cleaned_data['title'],
                            '/' + owner_name + '/' + repo_name + '/milestones')
    else:
        form = MilestoneForm()

    repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
    milestone_list = Milestone.objects.filter(repository=repository)
    return render(request, 'igenapp/milestones/milestones.html',
                  {'milestones': milestone_list, 'owner_name': owner_name, 'repo_name': repo_name})


def remove_milestone(request, owner_name, repo_name, milestone_id):
    m = Milestone.objects.filter(pk=milestone_id).delete()
    repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
    milestone_list = Milestone.objects.filter(repository=repository)
    create_activity(request, owner_name, repo_name, ' removed milestone ',
                    '/' + owner_name + '/' + repo_name + '/milestones')
    return render(request, 'igenapp/milestones/milestones.html',
                  {'milestones': milestone_list, 'owner_name': owner_name, 'repo_name': repo_name})


def labels(request, owner_name, repo_name):
    repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
    label_list = Label.objects.filter(repository=repository)
    return render(request, 'igenapp/labels/labels.html', {'labels': label_list, 'owner_name': owner_name, 'repo_name': repo_name})


def add_label(request, owner_name, repo_name):
    if request.method == "POST":
        form = LabelForm(request.POST)
        if form.is_valid():
            repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
            Label.objects.create(name=form.cleaned_data['name'], color=form.cleaned_data['color'], repository=repository)
            create_activity(request, owner_name, repo_name, ' created label ' + form.cleaned_data['name'],
                            '/' + owner_name + '/' + repo_name + '/labels')
    else:
        form = LabelForm()

    repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
    label_list = Label.objects.filter(repository=repository)
    return render(request, 'igenapp/labels/labels.html', {'labels': label_list, 'owner_name': owner_name, 'repo_name': repo_name})


def remove_label(request, owner_name, repo_name, label_id):
    Label.objects.filter(pk=label_id).delete()
    create_activity(request, owner_name, repo_name, ' removed label ', '/' + owner_name + '/' + repo_name + '/labels')
    repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
    label_list = Label.objects.filter(repository=repository)
    return render(request, 'igenapp/labels/labels.html', {'labels': label_list, 'owner_name': owner_name, 'repo_name': repo_name})


def commits(request, owner_name, repo_name):
    #if owner_name == request.user.username:
        #return render(request, 'igenapp/commits/commits.html',
                      #{'repo_info': {'owner_name': owner_name, 'repo_name': repo_name}})

    result = requests.get('https://api.github.com/repos/%s/%s/commits' % (owner_name, repo_name))
    commits = json.loads(result.content)

    try:
        if commits['message'] == 'Not Found':
            repo_info = RepositoryInfo(owner_name, repo_name, [], [])
    except:
        result = requests.get('https://api.github.com/repos/%s/%s/branches' % (owner_name, repo_name))
        branches = json.loads(result.content)

        repo_info = RepositoryInfo(owner_name, repo_name, branches, commits)

    return render(request, 'igenapp/commits/commits.html', {'repo_info': repo_info})


def commit(request, owner_name, repo_name, commit_id):
    result = requests.get('https://api.github.com/repos/%s/%s/commits/%s' % (owner_name, repo_name, commit_id))
    commit = json.loads(result.content)
    commit['commit']['author']['date'] = commit['commit']['author']['date'].replace('T', ' ')[:-1]
    commit['allAdditions'] = sum([file['additions'] for file in commit['files']])
    commit['allDeletions'] = sum([file['deletions'] for file in commit['files']])

    return render(request, 'igenapp/commits/commit.html', {'commit': commit, 'owner_name': owner_name, 'repo_name': repo_name})


def selected_branch(request, owner_name, repo_name):
    branch = request.GET.get('branch')
    result = requests.get('https://api.github.com/repos/%s/%s/commits?sha=%s' % (owner_name, repo_name, branch))
    branch_info = {'owner_name': owner_name, 'repo_name': repo_name, 'commits': json.loads(result.content)}

    return JsonResponse(branch_info, safe=False)


def repositories(request, owner_name):
    repositories = Repository.objects.filter(author=request.user).all()
    controbute_to = Repository.objects.filter(contributors=request.user).all()
    all_repos = repositories | controbute_to
    activity = Activity.objects.filter(repository__in=all_repos).order_by('-date')

    try:
        image = UserImage.objects.get(user=request.user)
    except ObjectDoesNotExist:
        image = None
    return render(request, 'igenapp/repository/repository.html',
                  {'repositories': repositories, 'controbute_to': controbute_to,
                   'image': image, 'activity': activity, 'owner_name': request.user.username})


def new_repository(request, owner_name):
    users = User.objects.all().exclude(username=owner_name)
    return render(request, 'igenapp/repository/new_repository.html', {'users': users, 'owner_name': owner_name})


def delete_repository(request, owner_name, repository_id):
    Repository.objects.filter(pk=repository_id).delete()

    return redirect('/' + owner_name + '/repositories')


def add_repository(request, owner_name):
    if request.method == "POST":
        error = True
        repo_type = request.POST.get('repo_type')
        if repo_type == "local":
            form = LocalRepositoryForm(request.POST)
            if form.is_valid():
                repo_name = re.sub('[\s+]', '_', form.cleaned_data['repo_name'].strip())
                old_repo = Repository.objects.filter(repo_name=repo_name, owner_name=request.user.username)
                if len(old_repo) == 0:
                    repository = Repository(author=request.user,
                                            repo_name=repo_name,
                                            owner_name=request.user.username, type='L')
                    repository.save()
                    contributors = request.POST.getlist('contributors')
                    repository.contributors.clear()
                    for contributor in contributors:
                        repository.contributors.add(contributor)
                    repository.save()
                    error = False
        elif repo_type == "git":
            form = GitRepositoryForm(request.POST)
            if form.is_valid():
                repo_url = form.cleaned_data['repo_url']
                if not repo_url.endswith(".git"):
                    return redirect('/' + owner_name + '/new_repository')
                owner_repo_name = repo_url[repo_url.rfind("/", 0, repo_url.rfind("/"))+1:repo_url.rfind("/")]
                repo_name = repo_url[repo_url.rfind("/")+1:-4]
                old_repo = Repository.objects.filter(repo_name=repo_name, owner_name=owner_repo_name)
                if len(old_repo) == 0:
                    repository = Repository(author=request.user, repo_name=repo_name,
                                            owner_name=owner_repo_name, type='G', url=repo_url)
                    repository.save()
                    contributors = request.POST.getlist('contributors')
                    repository.contributors.clear()
                    for contributor in contributors:
                        repository.contributors.add(contributor)
                    repository.save()
                    error = False
        if error:
            return redirect('/' + owner_name + '/new_repository')

        return redirect('/'+owner_name+'/repositories')
    else:
        return redirect('/' + owner_name + '/new_repository')


def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            avat = request.FILES.get('avatar', False)
            if avat != False:
                image = UserImage()
                image.avatar = request.FILES['avatar']
                image.user = User.objects.get(username=user.username)
                image.save()
            return redirect('login')
        else:
            context = dict()
            context['form'] = form
            context['message'] = "Error has occured"
            return render(request, 'igenapp/users/signup.html', context)
    else:
        form = UserForm()
        image = ImageForm()
        return render(request, 'igenapp/users/signup.html', {'form':form, 'image':image})


def editUser(request):
    #nacin dobavljanja korisnika iz sesije je request.user
    user = request.user
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            context = dict()
            try:
                image = UserImage.objects.get(user=user)
                avat = request.FILES.get('avatar', False)
                if avat != False:
                    image.user = User.objects.get(username=user.username)
                    image.avatar = request.FILES['avatar']
                    image.save()
            except ObjectDoesNotExist:
                avat = request.FILES.get('avatar', False)
                if avat != False:
                    image = UserImage()
                    image.user = User.objects.get(username=user.username)
                    image.avatar = request.FILES['avatar']
                    image.save()
                else:
                    image = None
            context['image'] = image
            context['form'] = UserEditForm(instance = user)
            context['owner_name'] = user.username
            context['new_image'] = ImageForm()
            context['message'] = 'Your profile has been successfully updated!'
            return render(request, 'igenapp/users/user_profile.html', context)
        else:
            context = dict()
            try:
                image = UserImage.objects.get(user=user)
            except ObjectDoesNotExist:
                image = None
            context['image'] = image
            context['form'] = form
            context['message'] = 'Error updating profile info. Please check input data!'
            context['owner_name'] = user.username
            context['new_image'] = ImageForm()
            return render(request, 'igenapp/users/user_profile.html', context)
    else:
        if request.user.is_authenticated:
            user = request.user
            context = dict()
            context['form'] = UserEditForm(instance=user)
            try:
                image = UserImage.objects.get(user=user)
            except ObjectDoesNotExist:
                image = None
            context['image'] = image
            context['new_image'] = ImageForm()
            context['owner_name'] = user.username
            return render(request, 'igenapp/users/user_profile.html', context)
        else:
            return redirect('login')

def remove_avatar(request):
    user = request.user
    try:
        image = UserImage.objects.get(user=user)
        image.delete()
    except ObjectDoesNotExist:
        image = None
    return redirect('editUser')

def logout_view(request):
    logout(request)
    return redirect('login')


def add_comment(request, owner_name, repo_name, parent, parent_id):
    if request.method == "POST":
        if parent == 'issue':
            comment = Comment()
            comment.content = request.POST['content']
            comment.user = request.user
            comment.date = timezone.now()
            comment.issue = Issue.objects.get(id=parent_id)
            comment.save()
            create_activity(request, owner_name, repo_name, ' left comment on issue ' + comment.issue.title,
                            '/' + owner_name + '/' + repo_name + '/issues/' + str(comment.issue.id))
            return redirect('issue_details', owner_name, repo_name, parent_id)
        elif parent == 'task':
            comment = Comment()
            comment.content = request.POST['content']
            comment.user = request.user
            comment.date = timezone.now()
            comment.task = Task.objects.get(id=parent_id)
            comment.save()
            create_activity(request, owner_name, repo_name, ' left comment on task ' + comment.task.title,
                            '/' + owner_name + '/' + repo_name + '/task-page/' + str(comment.task.id))
            return redirect('task-page', owner_name, repo_name, parent_id)
        else:
            comment = Comment()
            comment.content = request.POST['content']
            comment.user = request.user
            comment.date = timezone.now()
            comment.wiki = WikiPage.objects.get(id=parent_id)
            comment.save()
            create_activity(request, owner_name, repo_name, ' left comment on wiki ' + comment.wiki.title,
                            '/' + owner_name + '/' + repo_name + '/wiki-page/' + str(comment.wiki.id))
            return redirect('wiki-page', owner_name, repo_name, parent_id)


def edit_comment(request, owner_name, repo_name, parent, parent_id):
    if request.method == "POST":
        comment_id = request.POST['comment_id']
        comment = Comment.objects.get(id=comment_id)
        comment.content = request.POST['content']
        comment.save()
        if parent == 'issue':
            return redirect('issue_details', owner_name, repo_name, parent_id)
        elif parent == 'task':
            return redirect('task-page', owner_name, repo_name, parent_id)
        else:
            return redirect('wiki-page', owner_name, repo_name, parent_id)


def delete_comment(request, owner_name, repo_name, parent, parent_id, comment_id):
    if request.method == "POST":
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        if parent == 'issue':
            return redirect('issue_details', owner_name, repo_name, parent_id)
        elif parent == 'task':
            return redirect('task-page', owner_name, repo_name, parent_id)
        else:
            return redirect('wiki-page', owner_name, repo_name, parent_id)


def landing(request, owner_name, repo_name):
    return render(request, 'igenapp/landingpage.html', owner_name, repo_name)


def task(request, owner_name, repo_name):
    tasks_list = Task.objects.all()
    return render(request, 'igenapp/task/tasks.html', {'tasks': tasks_list, 'owner_name': owner_name, 'repo_name': repo_name})


def task_form(request, owner_name, repo_name):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            create_activity(request, owner_name, repo_name, ' created task page ', '/'+owner_name+'/'+repo_name+'/task')
            return redirect('task', owner_name, repo_name)
        else:
            context = dict()
            context['form'] = form
            context['message'] = "Error has occured:"
            context['owner_name'] = owner_name
            context['repo_name'] = repo_name
            return render(request, 'igenapp/task/form.html', context)
    else:
        form = TaskForm()
        return render(request, 'igenapp/task/form.html', {'form': form, 'owner_name': owner_name, 'repo_name': repo_name})


def task_page(request, owner_name, repo_name, task_id):
    taskpage = get_object_or_404(Task, pk=task_id)
    comments = Comment.objects.filter(task=taskpage).order_by('date')
    images = UserImage.objects.all()
    return render(request, 'igenapp/task/page.html', {'task': taskpage, 'comments': comments, 'images':images,
                                                                 'owner_name': owner_name, 'repo_name': repo_name})


def remove_task(request, owner_name, repo_name, task_id):
    Task.objects.filter(pk=task_id).delete()
    create_activity(request, owner_name, repo_name, ' removed task page ', '/' + owner_name + '/' + repo_name + '/wiki')
    task_list = Task.objects.all()
    return redirect('task', owner_name, repo_name)


def edit_task(request, owner_name, repo_name, task_id):
    if request.method == "POST":
        taskpage = Task.objects.filter(pk=task_id).first()
        form = TaskForm(request.POST, instance=taskpage)
        if form.is_valid():

            form.save()
            return redirect('task', owner_name, repo_name)
        else:
            context = dict()
            context['form'] = form
            context['message'] = "Error has occured:"
            context['owner_name'] = owner_name
            context['repo_name'] = repo_name
            return render(request, 'igenapp/task/form.html', context)
    else:
        taskpage = Task.objects.filter(pk=task_id).first()
        form = TaskForm(instance=taskpage)
        return render(request, 'igenapp/task/form.html', {'form': form, 'owner_name': owner_name, 'repo_name': repo_name})


def search_task(request, owner_name, repo_name):
    title = request.POST.get('title')

    #repository = get_object_or_404(Repository, owner_name=owner_name, repo_name=repo_name)
    #tasks_list = Task.objects.filter(repository=repository).order_by('-date')
    #if title != 'null':
    #    tasks_list = tasks_list.filter(title=title)
    tasks_list = Task.objects.filter(title__contains=title)
    return render(request, 'igenapp/task/tasks.html',
                  {'tasks': tasks_list, 'owner_name': owner_name, 'repo_name': repo_name})
