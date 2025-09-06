from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostForm
from .models import Post
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.


def post_list(request):
    query = request.GET.get('q')
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-id')
    else:
        posts = Post.objects.all().order_by('-id')

    paginator = Paginator(posts,4)
    page_number= request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'posts/post_list.html',{'page_obj':page_obj})

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request,'posts/post_detail.html',{'post':post})

@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit = False)
            post.author = request.user
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm()
    return render(request,'posts/post_edit.html',{'form':form})

@login_required
def post_edit(request,pk):
    post = get_object_or_404(Post,pk=pk)

    if post.author != request.user:
        return redirect('post_list')
    if request.method=='POST':
        form = PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request,'posts/post_edit.html',{'form':form})

@login_required
def post_delete(request,pk):
    post = get_object_or_404(Post,pk=pk)

    if post.author != request.user:
        return redirect('post_list')

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
