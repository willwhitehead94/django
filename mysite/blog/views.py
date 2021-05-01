from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView  # Used for class-based views (Django specific)
from .forms import EmailPostForm, CommentForm, SearchForm
from django.core.mail import send_mail  # Used to sent data to somebody via the view (Page 44).
from taggit.models import Tag  # The taggable manager to allow us to list the tags next to each post (Page 61).
from django.db.models import Count  # Used to start to recommend similar articles. The Count module contains the aggregations, such as Avg, Max, Min etc. (Page 64)
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank  # Used to search across fields.


# Create your views here.
def post_list(request, tag_slug=None):
    # posts = Post.published.all()
    object_list = Post.published.all()
    
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        print(f'Demo - TAG SLUG:{tag_slug}!')
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3)  # Cap the number of posts per page at 3.
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts,
                                                    'tag': tag})

    # return render(request, 'blog/post/list.html', {'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)

    # Comment additions
    comments = post.comments.filter(active=True)
    new_comment = None
    comment_form = CommentForm()

    if request.method == 'POST':
        # New comment has been posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False) # Object created but not formally saved.
            new_comment.post = post #  Link the comment to this Post object.
            new_comment.save()
        else:
            comment_form = CommentForm()

    # Similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                    'comments': comments,
                                                    'new_comment': new_comment,
                                                    'comment_form': comment_form,
                                                    'similar_posts': similar_posts
                                                    })

# Class-based views, as opposed to functional views as above.
class PostListView(ListView):
    queryset = Post.published.all()
    # model = Post #  Use this if you want Django to generate it's own object.all() view.
    context_object_name = 'posts' # This would default to object_list if we didn't define a context here.
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_share(request, post_id):
    # Retrieve a post by its ID.
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cleaned_data['name']} recommends you read {post.title}!"
            message = f"Read {post.title} by clicking here, or visiting {post_url}.\n\n{cleaned_data['name']} said {cleaned_data['comment']}!"
            send_mail(subject,message,'will@littleoxfordstreet.com', [cleaned_data['to']])
            
            sent = True
        else:
            print(f'Form contained validation issues: {form.errors}')
    else:
        form = EmailPostForm()
        
    return render(request, 'blog/post/share.html', {'post':post, 'form': form, 'sent':sent})


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query)
            results = Post.published.annotate(
                search = search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(search=search_query).order_by('-rank')
    return render(request,
                'blog/post/search.html',
                {'form':form, 'query':query, 'results':results}
                )