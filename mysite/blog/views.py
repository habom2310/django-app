from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from .models import Content
from . import md_converter
from django.urls import reverse
from django.utils import timezone
from .forms import BlogForm
import os 

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    context_object_name = 'latest_blog_list'

    def get_queryset(self):
        """Return all blog"""
        return Content.objects.all()
        
def detail(request, pk):
    blog = get_object_or_404(Content, pk=pk)
    # blog.body = md_converter.md_convert(blog.body)
    # print(blog.body)
    return render(request, 'blog/detail.html', {'blog': blog})

class DetailView(generic.DetailView):
    model = Content
    template_name = 'blog/detail.html'

    def get_queryset(self):
        return Content.objects.all()

def handle_uploaded_file(f, file_name):
    dt = timezone.datetime.now()
    folder_name = "blog/static/blog/" + dt.strftime('%Y%m%d')
    if os.path.exists(folder_name) == False:
        os.mkdir(folder_name)

    with open(f'{folder_name}/{file_name}.md', 'wb+') as destination:
        body = f.read()
        destination.write(body)
        body = md_converter.md_convert(body.decode('utf-8'))
        print(body)

    print(f"[Info] File writen to '{folder_name}/{file_name}.md'")

    return body


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
                blog_post.body = handle_uploaded_file(file, blog_post.title)
            else:
                if has_text == True:
                    blog_post.body = md_converter.md_convert(blog_post.body)
                else:
                    return render(request, 'blog/add.html', {'form': form, 'error_message': 'Enter something in the body or upload a md file'})

            blog_post.updated_at = timezone.now()
            blog_post.save()
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            print("invalid")
    else:
        form = BlogForm()
    return render(request, 'blog/add.html', {'form': form})