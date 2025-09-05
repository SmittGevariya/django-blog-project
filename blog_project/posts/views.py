from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.


def post_list(request):
    posts = Post.objects.all()
    return render(request,'posts/post_list.html',{'posts':posts})

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request,'posts/post_detail.html',{'post':post})

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form=form.save()
            return redirect('post_detail',pk=form.pk)
    else:
        form = PostForm()
    return render(request,'posts/post_edit.html',{'form':form})

@login_required
def post_edit(request,pk):
    post = get_object_or_404(Post,pk=pk)

    if request.method=='POST':
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request,'posts/post_edit.html',{'form':form})

@login_required
def post_delete(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request,'posts/post_confirm_delete.html',{'post':post})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request,'registration/signup.html',{'form':form}) 