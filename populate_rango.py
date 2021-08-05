import os, random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()
from rango.models import Category, Page, User, UserProfile, Comment

# For an explanation of what is going on here, please refer to the TwD book.

def populate():
    python_pages = [
        {'title': 'Official Python Tutorial',
         'url':'http://docs.python.org/3/tutorial/',
         'views': 114,},
        {'title':'How to Think like a Computer Scientist',
         'url':'http://www.greenteapress.com/thinkpython/',
         'views': 53},
        {'title':'Learn Python in 10 Minutes',
         'url':'http://www.korokithakis.net/tutorials/python/',
         'views': 20} ]
    
    django_pages = [
        {'title':'Official Django Tutorial',
         'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/',
         'views': 32},
        {'title':'Django Rocks',
         'url':'http://www.djangorocks.com/',
         'views': 12},
        {'title':'How to Tango with Django',
         'url':'http://www.tangowithdjango.com/',
         'views': 1} ]

    java_pages = [
        {'title':'Java Tutorial for Beginners',
         'url':'https://www.guru99.com/java-tutorial.html',
         'views': 100},
        {'title':'Java API Specification',
         'url':'https://docs.oracle.com/javase/7/docs/api/',
         'views': 10},]

    c_pages = [
        {'title':'C Tutorial',
         'url':'https://www.tutorialspoint.com/cprogramming/index.htm',
         'views': 100},]
    
    database_pages = [
        {'title':'What Is a Database',
         'url':'https://www.oracle.com/database/what-is-database/',
         'views': 100},
        {'title':'Database Design',
         'url':'https://www3.ntu.edu.sg/home/ehchua/programming/sql/Relational_Database_Design.html',
         'views': 10},]

    other_pages = [
        {'title':'Bottle',
         'url':'http://bottlepy.org/docs/dev/',
         'views': 54},
        {'title':'Flask',
         'url':'http://flask.pocoo.org',
         'views': 64} ]
    
    cats = {'Python': {'pages': python_pages, 'views': 128, 'likes': 64},
            'Django': {'pages': django_pages, 'views': 64, 'likes': 32},
            'Java': {'pages': java_pages, 'views': 54, 'likes': 3},
            'C Programming': {'pages': c_pages, 'views': 24, 'likes': 44},
            'Database': {'pages': database_pages, 'views': 14, 'likes': 22},
            'Other Frameworks': {'pages': other_pages, 'views': 32, 'likes': 16} }
    
    for cat, cat_data in cats.items():
        c = add_cat(cat, views=cat_data['views'], likes=cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'], views=p['views'])
    
    #populate users with profiles
    i=0
    name='user'
    while i<10:
        u = add_user(name+str(i), 1)
        for page in Page.objects.all():#add comments to each page
            add_comment(u, page, 'I am '+name+str(i)+', I think '+ page.title+' is great!', random.randint(0,1000), random.randint(0,1000))
        i=i+1


def add_comment(author, page, content, likes, dislikes):
    comment = Comment.objects.get_or_create(author=author, page=page)[0]
    comment.content=content
    comment.likes=likes
    comment.dislikes=dislikes
    comment.save()

def add_user(name, password):
    u = User.objects.get_or_create(username=name, password=password)[0]
    u.save()
    profile = UserProfile.objects.get_or_create(user=u)[0]
    profile.save()
    return u

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name, views=0, likes=0):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c

# Start execution here!
if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()