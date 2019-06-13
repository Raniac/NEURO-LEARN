from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'add_book$', views.add_book, ),
    url(r'show_books$', views.show_books, ),
    url(r'register$', views.user_register, ),
    url(r'login$', views.user_login, ),
    url(r'overview_submissions$', views.overview_submissions, ),
    url(r'new_task$', views.new_task, ),
    url(r'show_submissions$', views.show_submissions, ),
    url(r'upload_data$', views.upload_data, ),
    url(r'show_data$', views.show_data, ),
    url(r'show_results$', views.show_results, ),
    url(r'show_img$', views.show_img, ),
    url(r'download_templates$', views.download_templates, ),
    ]
