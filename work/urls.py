from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('add',views.add,name='add'),
    path('check',views.check,name='check'),
    path('signin',views.signin,name='signin'),
    path('watch',views.watch,name='watch'),
    path('verify',views.verify,name='verify'),
    path('profile',views.profile,name='profile'),
    path('logout',views.logout,name='logout'),
    path('product',views.product,name='product'),
    path('editprofile',views.editprofile,name='editprofile'),
    path('saveprofile',views.saveprofile,name='saveprofile'),
    path('resend',views.resend,name='resend'),
    path('fgtpwd',views.fgtpwd,name='fgtpwd'),
    path('changepwd',views.changepwd,name='changepwd'),
    path('fgtpwdgo',views.fgtpwdgo,name='fgtpwdgo'),
    path('actionmovies', views.actionmovies, name = 'actionmovies'),
    path('romantic', views.romantic, name = 'romantic'),
    path('comedy', views.comedy, name = 'comedy'),
    path('drama', views.drama, name = 'drama'),
    path('watch_1', views.watch_1, name = 'watch_1'),
    path('searchmovies', views.searchmovies, name = 'searchmovies'),


]
