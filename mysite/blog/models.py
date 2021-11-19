from django.db import models
from django.template.defaultfilters import truncatechars

class Author(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)
    github_link = models.CharField(max_length=200, blank=True, default="")
    website = models.CharField(max_length=200, blank=True, default="")
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username

class CV(models.Model):
    class Exp_type(models.TextChoices):
        EDU = "EDU", "Education"
        WORK = "WORK", "Work Experience"

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    exp_type = models.CharField(max_length=10, choices=Exp_type.choices, default=Exp_type.WORK)
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    responsibility = models.TextField(default="", blank=True)
    projects = models.TextField(default="", blank=True)
    technologies = models.TextField(default="", blank=True)
    reference = models.TextField(default="", blank=True)

    date_start = models.DateTimeField()
    date_end = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.exp_type}-{self.position}"

class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Content(models.Model):
    title = models.CharField(max_length=100)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    github_link = models.CharField(max_length=200, default="")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def body_display(self):
        return truncatechars(self.body, 200)

    def __str__(self):
        return self.title



