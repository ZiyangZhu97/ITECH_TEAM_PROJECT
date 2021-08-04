from django.shortcuts import render
from django.shortcuts import HttpResponse
from rango.models import Category, Page, User, UserProfile, Comment
from rango.forms import CategoryForm
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import PageForm, UserForm, UserProfileForm, CommentForm, UserAvatarForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    TOPX = 5;
    liked_category_list=Category.objects.order_by('-likes')[:TOPX]
    viewed_category_list=Category.objects.order_by('-views')[:TOPX]

    liked_page_list=Page.objects.order_by('-likes')[:TOPX]
    viewed_page_list=Page.objects.order_by('-views')[:TOPX]

    context_dict = {}
    context_dict['boldmessage'] = 'Welcome to Rango, we have collected various IT tutorials for you!'
    context_dict['liked_categories'] = liked_category_list
    context_dict['liked_pages'] = liked_page_list
    context_dict['viewed_categories'] = viewed_category_list
    context_dict['viewed_pages'] = viewed_page_list
    context_dict['TOPX'] = TOPX
    
    return render(request, 'rango/index.html', context=context_dict)
    
def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context=context_dict)

def show_category(request, category_name_slug):
    context_dict= {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category) 
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    
    return render(request, 'rango/category.html', context=context_dict)

def show_profile(request, username):
    context_dict= {}
    try:
        user = request.user
        user1 = User.objects.get(username=username)
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get_or_create(user=user)[0]
        else:
            user_profile = None
        user_profile1  = UserProfile.objects.get_or_create(user=user1)[0]
        context_dict['user'] = user
        context_dict['user1'] = user1
        context_dict['user_profile'] = user_profile
        context_dict['user_profile1'] = user_profile1
    except User.DoesNotExist:
        context_dict['user'] = None
        context_dict['user1'] = None
        context_dict['user_profile'] = None
        context_dict['user_profile1'] = None

    return render(request, 'rango/profile.html', context_dict)

def update_avatar(request,username):
    context_dict= {}

    if request.method == 'POST':
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get_or_create(user=user)[0]  
            form = UserAvatarForm()
        except TypeError:
            return redirect(reverse('rango:index'))
        
        form = UserAvatarForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)
    else:
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get_or_create(user=user)[0]  
            form = UserAvatarForm()
            context_dict['user'] = user
            context_dict['user_profile'] = user_profile
            context_dict['form'] = form
        except User.DoesNotExist:
            context_dict['user'] = None
            context_dict['user_profile'] = None
            context_dict['form'] = None

    return render(request, 'rango/update_avatar.html', context_dict)

    

def show_page(request, page_name_slug):
    context_dict= {}
    try:
        page = Page.objects.get(slug=page_name_slug) 
        context_dict['page'] = page
    except Page.DoesNotExist:
        context_dict['page'] = None
    
    return render(request, 'rango/page.html', context=context_dict)

def show_page_order_by_likes(request, page_name_slug):
    context_dict= {}
    try:
        page = Page.objects.get(slug=page_name_slug) 
        context_dict['page'] = page
    except Page.DoesNotExist:
        context_dict['page'] = None
    
    return render(request, 'rango/page_comment_ordered_by_likes.html', context=context_dict)


@login_required
def add_comment(request, page_name_slug):
    
    try:
        page = Page.objects.get(slug=page_name_slug)
    except:
        page = None

    if page is None:
        context_dict= {}
        page = Page.objects.get(slug=page_name_slug) 
        context_dict['page'] = page
        return redirect('/rango/page.html', context=context_dict)

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            if page:
                comment = form.save(commit=False)
                comment.page = page
                comment.author = request.user######
                comment.likes = 0
                comment.dislikes = 0
                comment.save()

                return redirect(reverse('rango:show_page', kwargs={'page_name_slug': page_name_slug}))
        else:
            print(form.errors) 
    
    context_dict = {'form': form, 'page': page}
    return render(request, 'rango/add_comment.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.likes = 0
                page.dislikes = 0
                page.save()

                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors) 
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    return render(request, 'rango/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).seconds > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits