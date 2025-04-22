from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from .import views

urlpatterns = [
    path('', views.index),
    path('register', views.register,name='register'),
    path('login_view', views.login_view,name='login_view'),
    path('logout_view', views.logout_view,name='logout_view'),
    path('index/', views.index,name='index'),
    path('addstudent', views.addstudent,name='addstudent'),
    path('showlist', views.showlist,name='showlist'),
    path('searchlist', views.searchlist,name='searchlist'),
    path('searchpay', views.searchpay,name='searchpay'),
    path('editstudent/<int:pk>', views.editstudent,name='editstudent'),
    path('deletestudent/<int:pk>', views.deletestudent,name='deletestudent'),
    path('addpayment', views.addpayment,name='addpayment'),
    path('paymentshowlist', views.paymentshowlist,name='paymentshowlist'),
    path('attendance_view', views.attendance_view,name='attendance_view'),
    path('show/<int:pk>', views.show, name='show'),
    path('note', views.note, name='note'),
    path('attendancelist', views.attendancelist, name='attendancelist'),
    path('notes/', views.note_view, name='note_view'),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)