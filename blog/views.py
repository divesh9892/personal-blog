from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .forms import PostForm, CategoryForm, UserForm, ProfileForm, LoginForm, ContactForm
from .models import Post, UserIP, Hitcounts, Category
from django.contrib import messages
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from itertools import chain
from taggit.models import Tag
# Create your views here.


def superuser_only(function):
    """Limit view to superusers only."""
    def _inner(request, *args, **kwargs):
       if not request.user.is_superuser:
           raise PermissionDenied
       return function(request, *args, **kwargs)
    return _inner



def index(request):
    return redirect('/home')


def home(request):
    posts = Post.objects.all().order_by('-updatedAt')
    return render(request, 'blog/home.html', {'posts': posts})


@transaction.atomic
def signup(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            print(user)
            user.save()
            for field in profile_form.changed_data:
                print(field)
                setattr(user.profile, field, profile_form.cleaned_data.get(field))
            user.profile.save()
            messages.success(request, 'Your profile was successfully created!')
            return redirect('/login')
        else:
            messages.error(request, 'OOPS!! Looks like something went wrong.')
            # return redirect('/signup')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'blog/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def userLogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = UserForm()
        if request.method == 'POST':
            name = request.POST.get('username')
            print(name)
            pwd = request.POST.get('password1')
            print(pwd)
            user = authenticate(request, username=name, password=pwd)
            print(user)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Username or password is incorrect!!")
        context = {'form': form}
        return render(request, 'blog/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


@superuser_only
@transaction.atomic
def postCreate(request):
    posts = Post.objects.order_by('-published')
    # Show most common tags
    common_tags = Post.tags.most_common()[:4]
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES)
        cform = CategoryForm(request.POST)
        if form.is_valid() and cform.is_valid():
            post = form.save(commit=False)
            cpost = cform.save(commit=False)
            cpost.postId = post
            if cpost.category == 'DSA':
                cpost.slug = "data-structures-and-algorithms"
            elif cpost.category == 'PER':
                cpost.slug = "personal"
            else:
                cpost.slug = "web-development"
            post.save()
            cpost.save()
            hitcounts = Hitcounts.objects.create(postId=post, hitcounts=0)
            hitcounts.save()
            form.save_m2m()
            messages.success(request, "Post created successfully")
    else:
        form = PostForm()
        cform = CategoryForm()
    return render(request, 'blog/postcreate.html', {'form': form, 'cform': cform, 'posts': posts, 'common_tags': common_tags})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def postView(request, id, slug):

    post = Post.objects.get(id=id)
    hitcounts = Hitcounts.objects.get(postId=post)
    ip = get_client_ip(request)
    if UserIP.objects.filter(postId=post, ip=ip).exists():
        pass
    else:
        usip = UserIP.objects.create(postId=post, ip=ip)
        hitcounts.increase()
        usip.save()
        print('new ')
    return render(request, 'blog/postview.html', {'post': post, 'hitcounts': hitcounts})


@superuser_only
@transaction.atomic
def postEdit(request, id):
    if request.user.is_staff:
        obj = get_object_or_404(Post, id=id)
        obj1 = get_object_or_404(Category, postId=id)
        if request.method == 'POST':
            form = PostForm(request.POST or None, files=request.FILES, instance=obj)
            cform = CategoryForm(request.POST, instance=obj1)
            # context = {'form': form}
            if form.is_valid() and cform.is_valid():
                obj = form.save(commit=False)
                obj1 = cform.save(commit=False)
                if obj1.category == 'DSA':
                    obj1.slug = "data-structures-and-algorithms"
                elif obj1.category == 'PER':
                    obj1.slug = "personal"
                else:
                    obj1.slug = "web-development"
                obj.save()
                obj1.save()
                form.save_m2m()
                messages.success(request, "You successfully updated the post")
                context = {'form': form, 'cform': cform}
                return render(request, 'blog/postedit.html', context)
            else:
                messages.error(request, "The form was not updated successfully!!")
                context = {'form': form, 'cform': cform,
                           'error': 'The form was not updated successfully.'}
                return render(request, 'blog/postedit.html', context)
        else:
            form = PostForm(instance=obj)
            cform = CategoryForm(instance=obj1)
            return render(request, 'blog/postedit.html', {'form': form, 'cform': cform})
    else:
        messages.error(request, "You are not authorized!!")
        return render(request, 'blog/error.html')


@superuser_only
@transaction.atomic
def postDelete(request, id):
    if request.user.is_staff:
        post = Post.objects.get(id=id)
        post.delete()
        return redirect('/home')


def search(request):
    query = request.GET.get('q', '')
    if query:
        queryset = (Q(title__icontains=query)) | (Q(summary__icontains=query))
        results = Post.objects.filter(queryset).distinct()
        # queryset_chain = chain(result1, queryset3)
        # results = sorted(queryset_chain, key=lambda instance: instance.pk, reverse=True)
        # results = sorted(queryset_chain, key=lambda instance: instance.pk)
    else:
        results = []
    return render(request, 'blog/search.html', {'results': results, 'query': query})


def categoryFilter(request, slug):
    queryset = Q(slug__icontains=slug)
    results = Category.objects.filter(queryset).distinct()
    print(results)
    return render(request, 'blog/catfilter.html', {'results': results, 'slug': slug})


def tagFilter(request, slug):
    results = Post.objects.filter(tags__name__in=[slug]).distinct()
    return render(request, 'blog/tagfilter.html', {'results': results})


def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
                messages.success(request, 'Message successfully sent')
            except BadHeaderError:
                # print('Invalid header found.')
                messages.error(request, 'Oops! Something went wrong!')
                #return HttpResponse('Invalid header found.')
            # return redirect('home')
    return render(request, "blog/email.html", {'form': form})


def successView(request):
    return HttpResponse('Success! Thank you for your message.')

def aboutMe(request):
    return render(request, 'blog/about.html')