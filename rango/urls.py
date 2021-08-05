from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/', views.add_page, name='add_page'),
    path('restricted/', views.restricted, name='restricted'),
    path('like_category/', views.LikeCategoryView.as_view(), name='like_category'),

    path('profile/<username>/', views.show_profile, name='profile'),
    path('profile/<username>/update_profile/', views.update_profile, name='update_profile'),

    path('<slug:page_name_slug>/', views.show_page, name='show_page'),
    path('<slug:page_name_slug>/order-by-likes', views.show_page_order_by_likes, name='show_page_order_by_likes'),
    path('<slug:page_name_slug>/add-comment', views.add_comment, name='add_comment'),

    

]