from django.conf.urls import url
from App.views import views, user, posts, owncenter

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index),
    url(r'^register/$', user.register, name='register'),
    url(r'^userActivate/(\w+)/$', user.userActivate, name='userActivate'),
    url(r'^login/$', user.Login, name='login'),
    url(r'^logout/$', user.Logout, name='logout'),
    url(r'^verifycode/$', user.verifycode, name='verifycode'),
    url(r'^send_posts/$', posts.send_posts, name='send_posts'),
    url(r'^update_posts/$', posts.update_posts, name='update_posts'),
    url(r'^posts_detail/$', posts.posts_detail, name='posts_detail'),
    url(r'^search_posts/$', posts.search_posts, name='search_posts'),
    url(r'^upload/$', user.upload, name='upload'),
    url(r'^posts_manager/$', posts.posts_manager, name='posts_manager'),
    url(r'^delete_posts/$', posts.delete_posts, name='delete_posts'),
    url(r'^update_username/$', owncenter.update_username, name='update_username'),
    url(r'^update_password/$', owncenter.update_password, name='update_password'),
    url(r'^do_favourite/$', posts.do_favourite, name='do_favourite'),
    url(r'^delete_favourite/$', posts.delete_favourite, name='delete_favourite'),
    url(r'^my_favourite/$', owncenter.my_favourite, name='my_favourite'),

]
