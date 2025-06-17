from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/<int:id>/', views.project_detail, name='project_detail'),
    path('load-more-projects/', views.load_more_projects, name='load_more_projects'),
    path('my-portfolio-admin/', views.mainAdmin, name='mainAdmin'),
    path('respond/<int:pk>/', views.mark_responded, name='mark_responded'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='mainAdmin/login.html'), name='login'),
    path('change-password/', views.change_password, name='change_password'),
    path('settings/', views.settings, name='settings'),
    path('delete-profession/<int:id>/', views.delete_profession, name='delete_profession'),
    path('delete-skill/<int:id>/', views.delete_skill, name='delete_skill'),
    path('delete-education-info/<int:id>/', views.delete_edu, name='delete_edu'),
    path('delete-experience-info/<int:id>/', views.delete_exp, name='delete_exp'),
    path('delete-service-info/<int:id>/', views.delete_service, name='delete_service'),
    path('delete-social-media-info/<int:id>/', views.delete_social_media, name='delete_social_media'),
    path('delete-project/<int:id>/', views.delete_proj, name='delete_proj'),
    path('update-project/<int:id>/', views.update_proj, name='update_proj'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)