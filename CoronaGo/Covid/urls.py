from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
	path("", views.Landing,name="Landing"),
	path('AboutProject',views.AboutProject,name="AboutProject"),
    path('ContactUs',views.ContactUs,name="ContactUs"),
    path('Visualize',views.Visualize,name="Visualize"),
    path('data', views.get_data,name="get_data"),
    path('IndiaMap/', views.IndiaMap,name="IndiaMap"),
    path('data1/', views.data1,name="data1"),
    path('data2/', views.data2,name="data2"),
    path('FAQ/', views.FAQ,name="FAQ"),
    
]