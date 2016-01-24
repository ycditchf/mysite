# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from .models import Article

class LatestPosts(Feed):
	title = u"逆水博客"
	link = "/feed/"
	description = "Lastest Posts"

	def items(self):
		return Article.objects.published()[:5]
