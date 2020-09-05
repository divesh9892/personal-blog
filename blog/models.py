from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from taggit.managers import TaggableManager
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=25)
    profileImg = models.ImageField(upload_to='userprofile/', blank=True, null=True)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    # except ObjectDoesNotExist:
    #     Profile.objects.create(user=instance)


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    # authorId = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=400, null=False, blank=False, unique=True)
    metaTitle = models.CharField(max_length=400, null=False, blank=False)
    slug = models.SlugField(max_length=100, null=False, blank=False)
    summary = models.TextField(null=False, blank=False)
    published = models.BooleanField(default=True, blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    publishedAt = models.DateTimeField(auto_now=True)
    content = RichTextUploadingField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    tags = TaggableManager()
    comments = GenericRelation(Comment)
    # content = models.TextField(null=False, blank=False)
    # hitcounts = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Hitcounts(models.Model):
    id = models.AutoField(primary_key=True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    hitcounts = models.PositiveIntegerField(default=0)

    def increase(self, *args, **kwargs):
        self.hitcounts += 1
        super(Hitcounts, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.hitcounts)


class UserIP(models.Model):
    id = models.AutoField(primary_key=True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    ip = models.CharField(max_length=40)

    def __str__(self):
        return str(self.ip)


class Category(models.Model):

    class catChoices(models.TextChoices):
        PERSONAL = 'PER', "Personal"
        WEBDEVELOPMENT = 'WEB', "Web-Development"
        DATASTRUCTURESANDALGORITHMS = 'DSA', "Data Structures & Algorithms"

    id = models.AutoField(primary_key=True)
    postId = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=3,
        choices=catChoices.choices,
        default=catChoices.WEBDEVELOPMENT
    )
    slug = models.SlugField(max_length=100)

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.category)
    #     super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.category)
#
#
# class PostComment(models.Model):
#     id = models.AutoField(primary_key=True)
#     postId = models.ForeignKey(Post, on_delete=models.CASCADE)
#     title = models.CharField(max_length=400)
#     published = models.BooleanField(default=True)
#     createdAt = models.DateTimeField(auto_now_add=True)
#     publishedAt = models.DateTimeField(auto_now=True)
#     content = models.TextField()
#
#
# class Tag(models.Model):
#     id = models.AutoField(primary_key=True)
#     title = models.CharField(max_length=400)
#     metaTitle = models.CharField(max_length=400)
#     slug = models.SlugField(max_length=100)
#     content = models.CharField(max_length=200)
#
#
# class PostTag(models.Model):
#     postId = models.ForeignKey(Post, on_delete=models.CASCADE)
#     tagId = models.ForeignKey(Tag, on_delete=models.CASCADE)
#
#

#
#
# class PostCategory(models.Model):
#     postId = models.ForeignKey(Post, on_delete=models.CASCADE)
#     categoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
