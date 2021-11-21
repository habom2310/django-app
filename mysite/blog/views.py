from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from .models import Content
from . import md_converter
from django.urls import reverse
from django.utils import timezone
from .forms import BlogForm
import os 
import json
from . import utils

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_blog_list'

    def get_queryset(self):
        """Return all blog"""
        return Content.objects.all()
        
def detail(request, pk):
    blog = get_object_or_404(Content, pk=pk)
    md_text = utils.read_md_file(blog.body)
    html_text = md_converter.md_convert(md_text)
    blog.body = html_text
    # print(blog.body)
    return render(request, 'blog/detail.html', {'blog': blog})

def add(request):
    print("here")
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            has_file = False
            has_text = False
            print("valid")
            blog_post = form.save(commit=False)
            if request.FILES.get('file_upload', False):
                file = request.FILES['file_upload']
                if str(file)[-3:] != '.md':
                    print("[Error] File type not supported")
                    return render(request, 'blog/add.html', {'form': form, 'error_message': 'File type not supported'})
                has_file = True
            else:
                print('No file upload')

            if blog_post.body != '':
                has_text = True

            if has_file == True:
                blog_post.body = utils.handle_uploaded_file(file, blog_post.title)
            else:
                if has_text == True:
                    blog_post.body = utils.save_md_to_file(blog_post.body, blog_post.title)
                else:
                    return render(request, 'blog/add.html', {'form': form, 'error_message': 'Enter something in the body or upload a md file'})

            blog_post.updated_at = timezone.now()
            blog_post.save()
            return HttpResponseRedirect(reverse('blog:index'))
    else:
        form = BlogForm()
    return render(request, 'blog/add.html', {'form': form})

def string_escape(s, encoding='utf-8'):
    return (s.encode('latin1')         # To bytes, required by 'unicode-escape'
             .decode('unicode-escape') # Perform the actual octal-escaping decode
             .encode('latin1')         # 1:1 mapping back to bytes
             .decode(encoding))        # Decode original encoding

def ajax_preview(request):
    if request.is_ajax() or request.method == 'POST':
        print("ajax here")
        body = request.POST.get('mdtext', "")
        body = md_converter.md_convert(string_escape(body[1:-1]))
        print(body)

        return HttpResponse(json.dumps({'html_output': body}), content_type="application/json", status=200)
    else:
        return HttpResponse("")

def edit(request, pk):
    blog = get_object_or_404(Content, pk=pk)
    md_text = utils.read_md_file(blog.body)
    blog.body = md_text

    return render(request, 'blog/edit.html', {'blog': blog})

def edit_confirm(request, pk):
    blog = get_object_or_404(Content, pk=pk)
    if request.method == 'POST':
        title = request.POST.get("title", "")
        md_text = request.POST.get("markdown_text", "")

        valid = True
        if title != "":
            blog.title = title
        else:
            valid = False
        if md_text != "":
            file_path = blog.body
            utils.update_md_file(file_path, md_text)
        else:
            valid = False

        if valid:
            blog.updated_at = timezone.now()
            blog.save()
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            print("invalid")
            blog.body = md_text
            return render(request, 'blog/edit.html', {'blog': blog, 'error_message': 'Empty title or body'})
    else:
        md_text = utils.read_md_file(blog.body)
        html_text = md_converter.md_convert(md_text)
        blog.body = html_text
        return render(request, 'blog/edit.html', {'blog': blog})