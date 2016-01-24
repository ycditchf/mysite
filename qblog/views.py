# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views import generic
from django.template import loader
from django.http import HttpResponse
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from . import models
from django.http import Http404

# Create your views here.


class BlogIndex(generic.ListView):
	queryset = models.Article.objects.published()
	template_name = "blog/home.html"
	paginate_by = 5
	def get_context_data(self, **kwargs):
		context = super(BlogIndex, self).get_context_data(**kwargs)
		context['classification_list'] = models.Classification.clssification_list.all()
		context['tag_list'] = models.Tag.tag_list.all()
		context['recently_articles'] = models.Article.objects.get_recently_article_list()
		context['archives_month'] = models.Article.objects.get_archive_month_list()
		context['is_listview'] = True
		return context

class BlogDetail(generic.DetailView):
	model = models.Article
	template_name = "blog/post.html"
	
	def get_context_data(self, **kwargs):
		context = super(BlogDetail, self).get_context_data(**kwargs)
		context['classification_list'] = models.Classification.clssification_list.all()
		context['tag_list'] = models.Tag.tag_list.all()
		context['recently_articles'] = models.Article.objects.get_recently_article_list()
		context['archives_month'] = models.Article.objects.get_archive_month_list()
		return context

def classification(request,name):

	try:
		cate = models.Classification.objects.get(name=name)
	except models.Classification.DoesNotExist:		
		raise Http404
	object_list = models.Article.objects.published().filter(classification=cate)
	paginator = Paginator(object_list, 5)
	page_num = request.GET.get('page')
	try:
		object_list = paginator.page(page_num)
	except PageNotAnInteger:
		object_list = paginator.page(1)
	except EmptyPage:
		object_list = paginator.page(paginator.num_pages)
	is_category = True
	classification_list = models.Classification.clssification_list.all()
	tag_list = models.Tag.tag_list.all()
	recently_articles = models.Article.objects.get_recently_article_list()
	archives_month = models.Article.objects.get_archive_month_list()
	# context = {"object_list": object_list, "classification_list": classification_list, "is_category": is_category}
	return render(request, 'blog/home.html', locals())

def tag(request,name):
	try:
		tag = models.Tag.objects.get(slug=name)
	except models.Tag.DoesNotExist:		
		raise Http404
	object_list = models.Article.objects.published().filter(tags=tag)
	paginator = Paginator(object_list, 5)
	page_num = request.GET.get('page')
	try:
		object_list = paginator.page(page_num)
	except PageNotAnInteger:
		object_list = paginator.page(1)
	except EmptyPage:
		object_list = paginator.page(paginator.num_pages)
	is_tag = True
	classification_list = models.Classification.clssification_list.all()
	tag_list = models.Tag.tag_list.all()
	recently_articles = models.Article.objects.get_recently_article_list()
	archives_month = models.Article.objects.get_archive_month_list()
	# context = {"object_list": object_list, "classification_list": classification_list, "is_category": is_category}
	return render(request, 'blog/home.html', locals())

def archive(request):
	is_archive = True
	object_list = models.Article.objects.get_archive_year_list()
	classification_list = models.Classification.clssification_list.all()
	tag_list = models.Tag.tag_list.all()
	recently_articles = models.Article.objects.get_recently_article_list()
	archives_month = models.Article.objects.get_archive_month_list()
	# context = {"object_list": object_list, "classification_list": classification_list, "is_category": is_category}
	return render(request, 'blog/archive.html', locals())	

def archive_month(request, year, month):
	is_archive_month = True
	object_list = models.Article.objects.published().filter(modified__year=year, modified__month=month)
	paginator = Paginator(object_list, 5)
	page_num = request.GET.get('page')
	try:
		object_list = paginator.page(page_num)
	except PageNotAnInteger:
		object_list = paginator.page(1)
	except EmptyPage:
		object_list = paginator.page(paginator.num_pages)
	classification_list = models.Classification.clssification_list.all()
	tag_list = models.Tag.tag_list.all()
	recently_articles = models.Article.objects.get_recently_article_list()
	archives_month = models.Article.objects.get_archive_month_list()
	# context = {"object_list": object_list, "classification_list": classification_list, "is_category": is_category}
	return render(request, 'blog/home.html', locals())

def search(request):
	is_search = True
	if 'search_text' in request.GET:
		keyword = request.GET["search_text"]
		if not keyword:
			return render(request, 'home.html')
		else:
			object_list = models.Article.objects.published().filter(title__icontains = keyword)
	paginator = Paginator(object_list, 5)
	page_num = request.GET.get('page')
	try:
		object_list = paginator.page(page_num)
	except PageNotAnInteger:
		object_list = paginator.page(1)
	except EmptyPage:
		object_list = paginator.page(paginator.num_pages)
	classification_list = models.Classification.clssification_list.all()
	tag_list = models.Tag.tag_list.all()
	recently_articles = models.Article.objects.get_recently_article_list()
	archives_month = models.Article.objects.get_archive_month_list()
	# context = {"object_list": object_list, "classification_list": classification_list, "is_category": is_category}
	return render(request, 'blog/home.html', locals())	

def About(request):
	# t = loader.get_template("about.html")
	classification_list = models.Classification.clssification_list.all()
	tag_list = models.Tag.tag_list.all()
	recently_articles = models.Article.objects.get_recently_article_list()
	archives_month = models.Article.objects.get_archive_month_list()
	context = {"content": u"iOS开发，喜欢专研技术咦。。"}
	# return HttpResponse(t.render(context))
	return render(request, "blog/about.html", locals())
		
