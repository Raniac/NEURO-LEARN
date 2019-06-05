from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'add_book$', views.add_book, ),
    url(r'show_books$', views.show_books, ),
    url(r'login$', views.overview_submissions, ),
    url(r'overview_submissions$', views.overview_submissions, ),
    url(r'new_task$', views.new_task, ),
    url(r'show_submissions$', views.show_submissions, ),
    url(r'upload_data$', views.upload_data, ),
    url(r'show_data$', views.show_data, ),
    url(r'show_results$', views.show_results, ),
    url(r'show_roc$', views.show_roc, ),
    url(r'show_opt$', views.show_opt, ),
    url(r'download_templates$', views.download_templates, ),
    ]
