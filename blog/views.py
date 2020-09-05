from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .forms import EmailPostShare, CommentForm, SearchForm, Feedback
from .models import Post, Comment
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery

# Create your views here.
def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    tags = Tag.objects.all()
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])    
    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts, 'tag': tag, 'tags': tags})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                   status='published',
                                   publish__year=year,
                                   publish__month=month,
                                   publish__day=day)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:2]
     

    return render(request, 'blog/post/detail.html', {'post': post,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'similar_posts': similar_posts}) 

def post_share(request, post_slug):
    post= get_object_or_404(Post, slug=post_slug, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostShare(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends your to reading {}'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
    else:
        form = EmailPostShare()

    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent })

def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(search=SearchVector('tags', 'title', 'body'),).filter(search=query)

    return render(request, 'blog/post/search.html', {'form': form, 'query': query, 'results': results})

def feed_back(request):
    sent = False
    if request.method == 'POST':
        form = Feedback(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            subject = '{} ({}) Feedback'.format(cd['name'], cd['email'])
            message = cd['message']
            sender = cd['email']
            send_mail(subject, message, sender, ['admin@myblog.com'])
            sent = True
    else:
        form = Feedback()
    return render(request, 'blog/contact.html', {'form': form, 'sent': sent})