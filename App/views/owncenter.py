from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.urls import reverse

from App.models import User


def update_username(req):
    if req.method == 'GET':
        return render(req, 'home/update_username.html')
    if req.method == 'POST':
        username = req.POST.get('username')
        if len(username) > 12:
            info = '用户名必须在12个字以内！'
            return render(req, 'home/update_username.html', {'info': info})
        if User.objects.filter(username=username):
            info = '用户名已存在！'
            return render(req, 'home/update_username.html', {'info': info})
        u = req.user
        u.username = username
        u.save()
        info = '用户名修改成功！'
        return render(req, 'home/update_username.html', {'info': info})


def update_password(req):
    if req.method == 'GET':
        return render(req, 'home/update_password.html')
    if req.method == 'POST':
        password = req.POST.get('password')
        new_password = req.POST.get('new_password')
        confirm = req.POST.get('confirm')
        if len(new_password) > 12:
            info = '新密码必须在12个字符以内！'
            return render(req, 'home/update_password.html', {'info': info})
        if new_password != confirm:
            info = '新密码两次输入不一致！'
            return render(req, 'home/update_password.html', {'info': info})
        u = authenticate(username=req.user.username, password=password)
        if u:
            u.set_password(raw_password=new_password)
            u.save()
            # logout(req.user)
            return redirect(reverse('App:index'))
        else:
            info = '旧密码错误！'
            return render(req, 'home/update_password.html', {'info': info})


def my_favourite(req):
    if req.method == 'GET':
        data = req.user.posts_set.all()
        return render(req, 'home/my_favourite.html', {'data': data})
    if req.method == 'POST':
        word = req.POST.get('titleword')
        data = req.user.posts_set.filter(title__contains=word)
        return render(req, 'home/my_favourite.html', {'data': data, 'word': word})
