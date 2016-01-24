# -*- coding: utf-8 -*-
from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from . import models
# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
	list_display = ('name', 'email', 'website')
	search_fileds = ('name',)

class ArticleAdmin(MarkdownModelAdmin):
	list_display = ("title", "created", 'classification', 'publish')
	list_filter = ('modified',)
	# date_hierarch = 'modified'  #设置时间过滤器
	ordering = ('-modified',)
	filter_horizontal = ('tags',)  #水平显示的过滤器
	prepopulated_fields = {"slug": ("title",)}
	seach_fields = ['title']

admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Classification)
admin.site.register(models.Author, AuthorAdmin)

