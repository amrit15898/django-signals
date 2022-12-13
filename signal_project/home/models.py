from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete, post_delete
from django.dispatch import receiver
from django.template.defaultfilters import slugify
# Create your models here.
from datetime import datetime
import json

class Task(models.Model):
    name = models.CharField(max_length=100) 
    description = models.TextField()
    slug = models.SlugField(max_length=200, null=True, blank=True)

    is_deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

class TaskDate(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    date = models.CharField(max_length=100)

class History(models.Model):
    history = models.TextField(default={})

# def task_handler(sender, instance , **kwargs):
#     print("signal called")
#     print(instance)

# pre_save.connect(task_handler , sender=Task)
@receiver(pre_save, sender = Task)
def task_hanlder(sender , instance, **kwargs):
    print("task handler")
    print(instance.name)
    print(instance.description)
    instance.slug = slugify(instance.name)


@receiver(post_save, sender=Task)
def task_hanlder_post(sender, instance, **kwargs):
    TaskDate.objects.create(task = instance, date = datetime.now())

@receiver(pre_delete, sender = Task)
def task_hanlder_pre_delete(sender, instance, **kwargs):
    data = {"task":instance.name, "desc": instance.description , "slug":instance.slug}
    History.objects.create(history = json.dumps(data))

