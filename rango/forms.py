from django import forms
from rango.models import Page, Category, UserProfile, Comment
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, max_length=Comment.COMMENT_MAX_LENGTH, help_text="Enter your comment here:")
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    dislikes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    class Meta:
        model = Comment 
        fields = ('content',)#display textarea in the UI

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=Category.NAME_MAX_LENGTH, help_text="Please enter the category name:")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category 
        fields = ('name',)#display name input bar in the UI

class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Page.TITLE_MAX_LENGTH, help_text="Please enter the title of the page:")
    url = forms.URLField(max_length=Page.URL_MAX_LENGTH, help_text="Please enter the URL of the page:")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    dislikes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Page
        fields = ('title', 'url')#display title and url input bar in the UI

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = f'http://{url}'
            cleaned_data['url'] = url
        
        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)

class UserAvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)