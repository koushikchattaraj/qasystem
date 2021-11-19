from django.db import models
from django.contrib.auth.models import User
import os

class File(models.Model):

    name = models.CharField(max_length=100, null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    link = models.CharField(max_length=50, null=True, blank=True)
    extension = models.CharField(max_length=10, null=True, blank=True)
    document = models.FileField(upload_to="files", null=True, blank=True)
    doc_name = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey('Folder', on_delete=models.CASCADE, related_name="files", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_deleted = models.BooleanField(default=False, null=True, blank=True)
    is_starred = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
      return self.name


class Folder(models.Model):
  name = models.CharField(max_length=100)
  folders = models.ManyToManyField('self', related_name="parent", symmetrical=False, blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  parents = models.OneToOneField('self', related_name="folder", blank=True, null=True, on_delete=models.CASCADE)
  is_deleted = models.BooleanField(default=False)
  is_starred = models.BooleanField(default=False, null=True, blank=True)
  created_at = models.DateField(auto_now_add=True)


  # def all_parents(self):
  #   return self.parents

  def __str__(self):
    return self.name




