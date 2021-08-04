from django import template
from rango.models import Category, Comment

register = template.Library()

@register.inclusion_tag('rango/categories.html')
def get_category_list(current_category=None):
    return {'categories': Category.objects.all(),
            'current_category': current_category}

@register.inclusion_tag('rango/comments.html')
def get_comment_list_by_time(current_page=None):
    return {'comments': Comment.objects.filter(page=current_page).order_by('-writtenTime'),
            }

@register.inclusion_tag('rango/comments.html')
def get_comment_list_by_likes(current_page=None):
    return {'comments': Comment.objects.filter(page=current_page).order_by('-likes'),
            }