from django.contrib import admin
from django.urls import path
from newsApp import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static

context = views.context_data()

urlpatterns = [
    path('', views.home, name="home-page"),
    path('login',auth_views.LoginView.as_view(template_name="login.html",redirect_authenticated_user = True,extra_context = context),name='login-page'),
    path('logout',views.logoutuser,name='logout'),
    path('userlogin', views.login_user, name="login-user"),
    path('profile', views.profile, name="profile-page"),
    path('update_profile', views.update_profile, name="update-profile"),
    path('update_password', views.update_password, name="update-password"),
    path('new_post', views.manage_post, name="new-post"),
    path('edit_post/<int:pk>', views.manage_post, name="edit-post"),
    path('save_post', views.save_post, name="save-post"),
    path('post/<int:pk>', views.view_post, name="view-post"),
    path('save_comment', views.save_comment, name="save-comment"),
    path('posts', views.list_posts, name="all-posts"),
    path('category/<int:pk>', views.category_posts, name="category-post"),
    path('delete_post/<int:pk>', views.delete_post, name="delete-post"),
    path('delete_comment/<int:pk>', views.delete_comment, name="delete-comment"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
URL patterns for the newsApp Django application.

This module defines the URL patterns for the different views and functionalities of the newsApp.
Each URL pattern is associated with a specific view function or class-based view.

The urlpatterns list contains the following URL patterns:
- '' (empty string): Maps to the home view function, serving as the landing page of the application.
- 'login': Maps to the LoginView class from Django's authentication views, rendering the login.html template.
- 'logout': Maps to the logoutuser view function, handling user logout.
- 'userlogin': Maps to the login_user view function, handling user login.
- 'profile': Maps to the profile view function, rendering the user's profile page.
- 'update_profile': Maps to the update_profile view function, handling the updating of user profile information.
- 'update_password': Maps to the update_password view function, handling the updating of user password.
- 'new_post': Maps to the manage_post view function, rendering the form for creating a new post.
- 'edit_post/<int:pk>': Maps to the manage_post view function, rendering the form for editing an existing post.
- 'save_post': Maps to the save_post view function, handling the saving of a new or edited post.
- 'post/<int:pk>': Maps to the view_post view function, rendering the details of a specific post.
- 'save_comment': Maps to the save_comment view function, handling the saving of a new comment on a post.
- 'posts': Maps to the list_posts view function, rendering a list of all posts.
- 'category/<int:pk>': Maps to the category_posts view function, rendering a list of posts in a specific category.
- 'delete_post/<int:pk>': Maps to the delete_post view function, handling the deletion of a post.
- 'delete_comment/<int:pk>': Maps to the delete_comment view function, handling the deletion of a comment.

The static() function is used to serve media files in development mode.

"""
