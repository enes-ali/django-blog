from django.db import models
from Account.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.contrib.auth import get_user_model


post_categories = [
    ("tech", "Tech"),
    ("food", "Food"),
    ("health", "Health"),
    ("life", "Life"),
]

def cover_photo_upload_path(instance, filename):
    return f"posts/{instance.owner.username}/{instance.title}/{filename}"

class Post(models.Model):

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="posts")
    title = models.CharField("Title", max_length=155, unique=True)
    content = RichTextField()
    summary = models.CharField("Summary", max_length=200, default="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Mi proin sed libero enim sed faucibus turpis in")
    cover_photo = models.ImageField("Cover Photo", upload_to=cover_photo_upload_path)
    upload_date = models.DateField("Upload Date", auto_now_add=True)
    last_edit = models.DateField("Last Edit", auto_now=True)
    slug = models.SlugField("Slug for url", max_length=155, unique=True, blank=True)
    likes = models.ManyToManyField(get_user_model(), related_name="liked_posts", blank=True)
    category = models.CharField("Category", choices=post_categories, max_length=155)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["upload_date"]

class Comment(models.Model):

    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="comments", blank=True, null=True)
    anonymous_name = models.CharField("Name for anonymous users", max_length=155, blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    date = models.DateTimeField(auto_now_add=True)
    replyed_comment = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, related_name="replys", null=True)
    content = models.TextField("Content Of Comment", max_length=1000)

    class Meta:
        ordering  = ["date"]

    def __str__(self):
        if self.owner:
            return self.owner.username + "  " + self.post.title
        return self.anonymous_name + "  " + self.post.title

    def save(self, *args, **kwargs):
        if self.owner is None and self.anonymous_name is None:
            raise ValueError("You have to give owner or anonymous_name")
        
        super().save(*args, **kwargs)