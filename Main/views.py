from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


@require_GET
def HomePage(request):
    category = request.GET.get("category")
    if category:
        posts = Post.objects.filter(category=category)
    else:
        posts = Post.objects.all()
    
    page = request.GET.get("page")
    paginator = Paginator(posts, 14) # view 16 post by page
    current_page = paginator.get_page(page)

    # send Showcase and Popular posts
    popular_posts = Post.objects.order_by("-upload_date")[:6]
    showcase_posts = Post.objects.order_by("likes")[:3]

    content = {"posts": current_page, "popular_posts": popular_posts, "showcase_posts": showcase_posts}
    return render(request, "Main/home.html", content)



class PostDetailPage(View):

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        # send Popular posts
        popular_posts = Post.objects.order_by("-upload_date")[:6]
        return render(request, "Main/post_detail.html", {"post": post, "popular_posts": popular_posts})

    def post(self, request, slug):
        content = request.POST.get("content")
        post = get_object_or_404(Post, slug=slug)
        if request.user.is_authenticated:
            Comment.objects.create(post=post, content=content, owner=request.user)
        else:
            Comment.objects.create(post=post, content=content, anonymous_name=request.POST.get("anonymous_name"))
        return HttpResponse("Comment Created", status=200)


@method_decorator(login_required(login_url="/login/"), name="dispatch")
class PostUploadPage(View):

    def get(self, request):
        upload_form = PostUploadForm()
        return render(request, "Main/post_upload.html", {"form": upload_form})

    def post(self, request):
        post_form = PostUploadForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.owner = request.user
            post.save()
            return redirect(PostDetailPage, slug=post.slug)

        else:
            errors = post_form.errors
            upload_form = PostUploadForm()
            return render(request, "Main/post_upload.html", {"form": upload_form, "errors": errors})


@require_GET
def SearchPost(request):
    query = request.GET.get("query")
    posts = Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    popular_posts = Post.objects.all().order_by("-title")[:6]
    return render(request, "Main/search.html", {"posts": posts, "popular_posts": popular_posts})