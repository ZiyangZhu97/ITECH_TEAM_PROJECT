from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField

class Category(models.Model):
    NAME_MAX_LENGTH = 128

    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Page(models.Model):
    TITLE_MAX_LENGTH = 128
    URL_MAX_LENGTH = 200

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=TITLE_MAX_LENGTH, unique=True)
    url = models.URLField()
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Page, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class Comment(models.Model):
    COMMENT_MAX_LENGTH = 4000

    author = models.ForeignKey(User, on_delete=CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    content = models.TextField(max_length=COMMENT_MAX_LENGTH)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    writtenTime = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.author.username+" "+self.writtenTime.__str__()