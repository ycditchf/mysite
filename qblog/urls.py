from django.conf.urls import *
from . import views, feed

urlpatterns = [
    url(r'^$', views.BlogIndex.as_view(), name="index"),
    url(r'^feed/$', feed.LatestPosts(), name="feed"),
    url(r'^article/(?P<slug>\S+)$', views.BlogDetail.as_view(), name="article_detail"),
    url(r'^about/$', views.About, name="about"),
    url(r'^articleClassification/(?P<name>\w+)/$', views.classification, name="articleClassification"),
    url(r'^articleTag/(?P<name>\w+)/$', views.tag, name="articleTag"),
	url(r'^archive/(?P<year>\d{4})/(?P<month>\d{1,2})/$', views.archive_month, name="archive_month"),
	url(r'^archive/$', views.archive, name="archive"),
	url(r'^search/$', views.search, name="search"),
  
]