# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import smart_unicode
from django.db import models

from django.core.urlresolvers import reverse
from collections import OrderedDict
# Create your models here.

class Author(models.Model):
	name = models.CharField(max_length=30)
	email = models.EmailField(blank=True)
	website = models.URLField(blank=True)
	def __str__(self):
		return self.name.encode('utf8')

class TagManager(models.Manager):
	def get_queryset(self):
		tags = Tag.objects.all()
		objects_list = []
		for item in tags:
			articles = item.article_set.published() #等价item.article_set.all().filter(publish=True)
			objects_list.append((item.slug, len(articles)))
		return objects_list

class Tag(models.Model):
	slug = models.SlugField(max_length=200, unique=True)
	creat_time = models.DateTimeField(auto_now_add=True)
	objects = models.Manager()
	tag_list = TagManager()
	def __str__(self):
		return self.slug.encode('utf8')
		
class ClassificationManager(models.Manager):
	def get_queryset(self):
		classifications = Classification.objects.all()
		objects_list = []
		for item in classifications:
			articles = item.articles.published()
			objects_list.append((item.name, len(articles)))
		return objects_list

class Classification(models.Model):
	name = models.CharField(max_length=25)
	objects = models.Manager()
	clssification_list = ClassificationManager()
	def __str__(self):
		return u'%s' %(self.name)


class ArticleManager(models.Manager):
	def published(self):
		return self.get_queryset().filter(publish=True).order_by('-modified');
	def get_queryset(self):
		return super(ArticleManager, self).get_queryset() #.filter(publish=True)
	def get_recently_article_list(self):
		return self.published().order_by("-created")[:5]
	def get_archive_month_list(self):
		time_list = self.published().datetimes('modified', 'month', order='DESC')
		archive_list = []
		for time in time_list:
			articles = self.published().filter(modified__year=time.year).filter(modified__month=time.month)
			archive_list.append((time,len(articles)))
		# return sorted(archive_list, reverse=True)
		return archive_list
	def get_archive_year_list(self):
		time_list = self.published().datetimes('modified', 'year', order='DESC')
		dicts = OrderedDict()
		for time in time_list:
			articles = self.published().filter(modified__year=time.year)
			dicts.setdefault(time,articles)
		return dicts

class Article(models.Model):
	title = models.CharField(max_length=200)
	author = models.ManyToManyField(Author)
	from django_markdown.models import MarkdownField
	body = MarkdownField()#models.TextField()
	slug = models.SlugField(max_length=200, unique=True)
	n_comments = models.IntegerField(default=0)
	n_pingbacks = models.IntegerField(default=0)

	publish = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField()#(auto_now=True)
	tags = models.ManyToManyField(Tag)
	classification = models.ForeignKey(Classification, related_name='articles')#不写related_name则是 article_set
	# objects = models.Manager()
	objects = ArticleManager();

	def get_previous_article(self):
		article_list = Article.objects.published()
		current_article = article_list.get(id=self.id)
		index = 0
		for article in article_list:			
			if current_article == article:				
				if index > 0:
					return article_list[index-1]
				break;
			index=index+1
		return

	def get_next_article(self):
		article_list = Article.objects.published()
		current_article = article_list.get(id=self.id)
		index = 0
		for article in article_list:			
			if current_article == article:
				if index+1 < len(article_list):
					return article_list[index+1]
				break
			index=index+1
		return

	def get_absolute_url(self):
		return reverse("article_detail", kwargs={"slug": self.slug})

	def __str__(self):
		return self.title.encode('utf8')

	# def __unicode__(self): 
	# 	return smart_unicode(self.title)

	class Meta:
		verbose_name = "Blog Entry"
		verbose_name_plural = "Blog Entries"
		ordering = ["-modified"]




