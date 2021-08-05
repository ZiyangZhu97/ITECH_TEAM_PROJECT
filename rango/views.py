from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpResponse
from rango.models import Category, Page, User, UserProfile, Comment
from rango.forms import CategoryForm
from django.shortcuts import redirect
from django.urls import reverse
from rango.forms import PageForm, UserForm, UserProfileForm, CommentForm, UserAvatarForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils.decorators import method_decorator
from django.views import View

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
        context_dict['category'] = category
    except Category.DoesNotExist:
        return redirect(reverse('rango:index'))

    if request.method == 'POST':
        keyword = request.POST.get('keyword',None)
        pages = Page.objects.filter(category=category).filter(title__contains=keyword)
        context_dict['pages'] = pages
        context_dict['keyword'] = keyword
    else:
        pages = Page.objects.filter(category=category) 
        context_dict['pages'] = pages
        is_new_visit=visitor_cookie_handler(request) #count up visits
        if is_new_visit:
            category.views=category.views+1
            category.save()
        
    return render(request, 'rango/category.html', context=context_dict)

def show_profile(request, username):
    context_dict= {}
    if request.method == 'POST':
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get_or_create(user=user)[0]  
        form = UserAvatarForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)
    else:
        try:
            # user is request user (can be authenticated or unauthenticated)
            # user1 is selected user
            user = request.user
            user1 = User.objects.get(username=username)
            if request.user.is_authenticated:
                user_profile = UserProfile.objects.get_or_create(user=user)[0]
            else:
                user_profile = None
            user_profile1  = UserProfile.objects.get_or_create(user=user1)[0]
            form = UserAvatarForm()
            context_dict['user'] = user
            context_dict['user1'] = user1
            context_dict['user_profile'] = user_profile
            context_dict['user_profile1'] = user_profile1
            context_dict['form'] = form
        except User.DoesNotExist:
            context_dict['user'] = None
            context_dict['user1'] = None
            context_dict['user_profile'] = None
            context_dict['user_profile1'] = None
            context_dict['form'] = None

    return render(request, 'rango/profile.html', context_dict)

def update_profile(request,username):
    context_dict= {}

    if request.method == 'POST':
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        username = request.POST.get('username',None)
        email = request.POST.get('email',None)

        if username != None:
            user.username = username
        if email != None:
            user.email = email
        user.save()

        user_profile.user = user
        user_profile.save()

        return redirect('rango:profile', user.username)
        
    else:
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get_or_create(user=user)[0]
            context_dict['user'] = user
            context_dict['user_profile'] = user_profile
        except User.DoesNotExist:
            context_dict['user'] = None
            context_dict['user_profile'] = None

    return render(request, 'rango/update_profile.html', context_dict)

def show_page(request, page_name_slug):
    context_dict= {}
    try:
        page = Page.objects.get(slug=page_name_slug) 
        context_dict['page'] = page
        is_new_visit=visitor_cookie_handler(request)    #count up visits, a visit to a page also contributes to the visits of category
        if is_new_visit:
            page.views=page.views+1
            page.save()
            category = page.category
            category.views=category.views+1
            category.save()

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
            return redirect(reverse('rango:index'))
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

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

class LikeCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        category_id = request.GET['category_id']

        try:
            category = Category.objects.get(id=int(category_id))
        except Category.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        category.likes = category.likes + 1
        category.save()

        return HttpResponse(category.likes)


class LikePageView(View):
    @method_decorator(login_required)
    def get(self, request):
        page_id = request.GET['page_id']

        try:
            page = Page.objects.get(id=int(page_id))
        except Page.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        
        page.likes = page.likes + 1
        page.save()

        return HttpResponse(page.likes)

# class DislikePageView(View):
#     @method_decorator(login_required)
#     def get(self, request):
#         page_id = request.GET['page_id']

#         try:
#             page = Page.objects.get(id=int(page_id))
#         except Page.DoesNotExist:
#             return HttpResponse(-1)
#         except ValueError:
#             return HttpResponse(-1)
        
#         page.dislikes = page.dislikes + 1
#         page.save()

#         return HttpResponse(page.dislikes)

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).seconds > 3:  #each user can contribute to a visit every 3s
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
        return True
    else:
        request.session['last_visit'] = last_visit_cookie
        request.session['visits'] = visits
        return False