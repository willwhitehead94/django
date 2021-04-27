from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView  # Used for class-based views (Django specific)


# Create your views here.
def post_list(request):
    # posts = Post.published.all()
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # Cap the number of posts per page at 3.
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})

    # return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request, 'blog/post/detail.html', {'post': post})

# Class-based views, as opposed to functional views as above.
class PostListView(ListView):
    queryset = Post.published.all()
    # model = Post #  Use this if you want Django to generate it's own object.all() view.
    context_object_name = 'posts' # This would default to object_list if we didn't define a context here.
    paginate_by = 3
    template_name = 'blog/post/list.html'

