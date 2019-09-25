from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'v0/register$', views.user_register, ),
    url(r'v0/login$', views.user_login, ),
    url(r'v0/overview_submissions$', views.overview_submissions, ),
    url(r'v0/new_task$', views.new_task, ),
    url(r'v0/new_sa_task$', views.new_sa_task, ),
    url(r'v0/show_submissions$', views.show_submissions, ),
    url(r'v0/upload_data$', views.upload_data, ),
    url(r'v0/show_data$', views.show_data, ),
    url(r'v0/delete_data$', views.delete_data, ),
    url(r'v0/download_data$', views.download_data, ),
    url(r'v0/show_results$', views.show_results, ),
    url(r'v0/show_img$', views.show_img, ),
    url(r'v0/download_templates$', views.download_templates, ),
    url(r'v0/download_workflows$', views.download_workflows, ),
    url(r'v0/download_feature_weights$', views.download_feature_weights, ),
    url(r'v0/download_significance_values$', views.download_significance_values, ),
    url(r'v0/show_project_overview$', views.show_project_overview, ),
    url(r'v0/show_flowchart$', views.show_flowchart, )
    ]
