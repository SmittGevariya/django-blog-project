from django.shortcuts import get_object_or_404, render, redirect
from .forms import PostForm
from .models import Post
# Create your views here.

def post_list(request):
    posts = Post.objects.all()
    return render(request,'posts/post_list.html',{'posts':posts})

def post_detail(request,pk):
    post = get_object_or_404(Post,pk=pk)
    return render(request,'posts/post_detail.html',{'post':post})

def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form=form.save()
            return redirect('post_detail',pk=form.pk)
    else:
        form = PostForm()
    return render(request,'posts/post_edit.html',{'form':form})

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

def post_delete(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request,'posts/post_confirm_delete.html',{'post':post})