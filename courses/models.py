from django.db import models
from django.db.models import Avg
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from courses.fields import OrderField
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils import timezone
from autoslug import AutoSlugField

import numpy as np

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='courses_created', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # slug = models.SlugField(max_length=200, unique=True)
    slug = AutoSlugField(populate_from='title', unique_with='created__month')
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='courses_joined', blank=True)

    class Meta:
        ordering = ('-created',)

    # def save(self, *args, **kwargs):
        # if not self.slug:
            # self.slug = slugify(self.title)
        # super(Course, self).save(*args, **kwargs)

    def average_rating(self):
        # all_ratings = map(lambda x: x.rating, self.reviews.all())
        # return np.mean(all_ratings)
        return self.reviews.aggregate(Avg('rating'))['rating__avg']

    def __str__(self):
        return self.title

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


class ItemBase(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='%(class)s_related', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def render(self):
        return render_to_string('courses/content/{}.html'.format(self._meta.model_name), {'item': self})

    def __str__(self):
        return self.title

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()


class Content(models.Model):
    module = models.ForeignKey(Module, related_name='contents', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, limit_choices_to={'model__in':('text', 'video', 'image', 'file')}, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5')
    )
    course = models.ForeignKey(Course, related_name='reviews', on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    user_name = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviewers', on_delete=models.CASCADE)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)


# https://github.com/pinax/pinax-badges
class BadgeAward(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="badges_earned", on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(default=timezone.now)
    slug = models.CharField(max_length=255)
    level = models.IntegerField()

    def __str__(self):
        return "{} : {} points - level {}".format(self.user.username, self.user.profile.award_points, self.level)
