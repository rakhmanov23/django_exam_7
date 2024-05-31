import uuid
from uuid import UUID

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.db.models import Model, CharField, SlugField, ForeignKey, CASCADE, ImageField, IntegerField, DateTimeField, \
    TextField, UUIDField, FileField, ManyToManyField, OneToOneField, TextChoices
from django.forms import EmailField
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class User(AbstractUser):
    class Types(TextChoices):
        EMPLOYER = 'employer', 'Employer'
        USER = 'user', 'User'

    types = CharField(max_length=255, choices=Types.choices, default=Types.USER)


class Vacancy(Model):
    title = CharField(max_length=255)
    description = CKEditor5Field()
    salary = IntegerField()
    qualification = CharField(max_length=255)
    time = CharField(max_length=255)
    address = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    employer = ForeignKey('apps.User', limit_choices_to={"types": User.Types.EMPLOYER}, on_delete=CASCADE)