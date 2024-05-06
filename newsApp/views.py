from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
import json
from newsApp import models, forms


def context_data():
    """
    Function to generate common context data for views.
    """
    context = {
        'site_name': 'NewsUp',
        'page': 'home',
        'page_title': 'News Portal',
        'categories': models.Category.objects.filter(status=1).all(),
    }
    return context


def home(request):
    """
    View for the home page.
    """
    context = context_data()
    posts = models.Post.objects.filter(status=1).order_by('-date_created').all()
    context['page'] = 'home'
    context['page_title'] = 'Home'
    context['latest_top'] = posts[:2]
    context['latest_bottom'] = posts[2:12]
    print(posts)
    return render(request, 'home.html', context)


def login_user(request):
    """
    View for user login.
    """
    logout(request)
    resp = {"status": 'failed', 'msg': ''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status'] = 'success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type='application/json')


def logoutuser(request):
    """
    View for user logout.
    """
    logout(request)
    return redirect('/')


@login_required
def update_profile(request):
    """
    View for updating user profile.
    """
    context = context_data()
    context['page_title'] = 'Update Profile'
    user = User.objects.get(id=request.user.id)
    if not request.method == 'POST':
        form = forms.UpdateProfile(instance=user)
        context['form'] = form
        print(form)
    else:
        form = forms.UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile-page")
        else:
            context['form'] = form
    return render(request, 'update_profile.html', context)



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
import json
from newsApp import models, forms


def context_data():
    """
    Function to generate common context data for views.
    """
    context = {
        'site_name': 'NewsUp',
        'page': 'home',
        'page_title': 'News Portal',
        'categories': models.Category.objects.filter(status=1).all(),
    }
    return context


@login_required
def update_password(request):
    """
    View for updating user password.
    """
    context = context_data()
    context['page_title'] = "Update Password"
    if request.method == 'POST':
        form = forms.UpdatePasswords(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account Password has been updated successfully")
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context['form'] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context['form'] = form
    return render(request, 'update_password.html', context)


@login_required
def profile(request):
    """
    View for user profile page.
    """
    context = context_data()
    context['page'] = 'profile'
    context['page_title'] = "Profile"
    return render(request, 'profile.html', context)


@login_required
def manage_post(request, pk=None):
    """
    View for managing posts (new post or edit post).
    """
    context = context_data()
    if pk is not None:
        context['page'] = 'edit_post'
        context['page_title'] = 'Edit Post'
        context['post'] = models.Post.objects.get(id=pk)
    else:
        context['page'] = 'new_post'
        context['page_title'] = 'New Post'
        context['post'] = {}

    return render(request, 'manage_post.html', context)


@login_required
def save_post(request):
    """
    View for saving a new post or updating an existing one.
    """
    resp = {'status': 'failed', 'msg': '', 'id': None}
    if request.method == 'POST':
        if request.POST['id'] == '':
            form = forms.savePost(request.POST, request.FILES)
        else:
            post = models.Post.objects.get(id=request.POST['id'])
            form = forms.savePost(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            if request.POST['id'] == '':
                post_id = models.Post.objects.all().last().id
            else:
                post_id = request.POST['id']
            resp['id'] = post_id
            resp['status'] = 'success'
            messages.success(request, "Post has been saved successfully.")
        else:
            for field in form:
                for error in field.errors:
                    if resp['msg'] != '':
                        resp['msg'] += '<br />'
                    resp['msg'] += f"[{field.label}] {error}"

    else:
        resp['msg'] = "Request has no data sent."
    return HttpResponse(json.dumps(resp), content_type="application/json")


def view_post(request, pk=None):
    """
    View for displaying a single post.
    """
    context = context_data()
    post = models.Post.objects.get(id=pk)
    context['page'] = 'post'
    context['page_title'] = post.title
    context['post'] = post
    context['latest'] = models.Post.objects.exclude(id=pk).filter(status=1).order_by('-date_created').all()[:10]
    context['comments'] = models.Comment.objects.filter(post=post).all()
    context['actions'] = False
    if request.user.is_superuser or request.user.id == post.user.id:
        context['actions'] = True
    return render(request, 'single_post.html', context)


def save_comment(request):
    """
    View for saving a new comment or updating an existing one.
    """
    resp = {'status': 'failed', 'msg': '', 'id': None}
    if request.method == 'POST':
        if request.POST['id'] == '':
            form = forms.saveComment(request.POST)
        else:
            comment = models.Comment.objects.get(id=request.POST['id'])
            form = forms.saveComment(request.POST, instance=comment)
    
        if form.is_valid():
            form.save()
            if request.POST['id'] == '':
                comment_id = models.Comment.objects.all().last().id
            else:
                comment_id = request.POST['id']
            resp['id'] = comment_id
            resp['status'] = 'success'
            messages.success(request, "Comment has been saved successfully.")
        else:
            for field in form:
                for error in field.errors:
                    if resp['msg'] != '':
                        resp['msg'] += '<br />'
                    resp['msg'] += f"[{field.label}] {error}"

    else:
        resp['msg'] = "Request has no data sent."
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def list_posts(request):
    """
    View for listing all posts.
    """
    context = context_data()
    context['page'] = 'all_post'
    context['page_title'] = 'All Posts'
    if request.user.is_superuser:
        context['posts'] = models.Post.objects.order_by('-date_created').all()
    else:
        context['posts'] = models.Post.objects.filter(user=request.user).all()

    context['latest'] = models.Post.objects.filter(status=1).order_by('-date_created').all()[:10]
    
    return render(request, 'posts.html', context)


def category_posts(request, pk=None):
    """
    View for listing posts by category.
    """
    context = context_data()
    if pk is None:
        messages.error(request, "File not Found")
        return redirect('home-page')
    try:
        category = models.Category.objects.get(id=pk)
    except models.Category.DoesNotExist:
        messages.error(request, "File not Found")
        return redirect('home-page')

    context['category'] = category
    context['page'] = 'category_post'
    context['page_title'] = f'{category.name} Posts'
    context['posts'] = models.Post.objects.filter(status=1, category=category).all()
        
    context['latest'] = models.Post.objects.filter(status=1).order_by('-date_created').all()[:10]
    
    return render(request, 'category.html', context)


@login_required
def delete_post(request, pk=None):
    """
    View for deleting a post.
    """
    resp = {'status': 'failed', 'msg': ''}
    if pk is None:
        resp['msg'] = 'Post ID is Invalid'
        return HttpResponse(json.dumps(resp), content_type="application/json")
    try:
        post = models.Post.objects.get(id=pk)
        post.delete()
        messages.success(request, "Post has been deleted successfully.")
        resp['status'] = 'success'
    except models.Post.DoesNotExist:
        resp['msg'] = 'Post ID is Invalid'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def delete_comment(request, pk=None):
    """
    View for deleting a comment.
    """
    resp = {'status': 'failed', 'msg': ''}
    if pk is None:
        resp['msg'] = 'Comment ID is Invalid'
        return HttpResponse(json.dumps(resp), content_type="application/json")
    try:
        comment = models.Comment.objects.get(id=pk)
        comment.delete()
        messages.success(request, "Comment has been deleted successfully.")
        resp['status'] = 'success'
    except models.Comment.DoesNotExist:
        resp['msg'] = 'Comment ID is Invalid'
    
    return HttpResponse(json.dumps(resp), content_type="application/json")
