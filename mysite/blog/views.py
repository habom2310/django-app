from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse
from .models import Content
from . import md_converter

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_blog_list'

    def get_queryset(self):
        """Return all blog"""
        return Content.objects.all()
        
def detail(request, pk):
    blog = get_object_or_404(Content, pk=pk)
    blog.body = md_converter.md_convert(blog.body)
    print(blog.body)
    return render(request, 'blog/detail.html', {'blog': blog})

class DetailView(generic.DetailView):
    model = Content
    template_name = 'blog/detail.html'

    def get_queryset(self):
        return Content.objects.all()