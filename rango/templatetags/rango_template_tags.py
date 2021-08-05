from django import template
from rango.models import Category, Comment

register = template.Library()

@register.inclusion_tag('rango/categories.html')
def get_category_list(current_category=None):
    return {'categories': Category.objects.all(),
            'current_category': current_category}

@register.inclusion_tag('rango/comments.html')
def get_comment_list_by_time(current_page=None):#called in html to display all comments in a page. Comments are ordered by the time when they were added
    return {'comments': Comment.objects.filter(page=current_page).order_by('-writtenTime'),
            }

@register.inclusion_tag('rango/comments.html')
def get_comment_list_by_likes(current_page=None):#called in html to display all comments in a page. Comments are ordered by the number of likes they got
    return {'comments': Comment.objects.filter(page=current_page).order_by('-likes'),
            }

@register.inclusion_tag('rango/comments.html')
def get_comment_list_by_user(current_user=None):#called in html to display all comments in a user's profile. Comments are ordered by the time when they were added
    return {'comments': Comment.objects.filter(author=current_user).order_by('-writtenTime'),
            }