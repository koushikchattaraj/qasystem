from os import pardir, rename
from rest_framework import serializers
from .models import File, Folder
from django.shortcuts import get_object_or_404, render
from accounts.models import User

class FolderMainSerilizers(serializers.ModelSerializer):
    
    class Meta:
        model = Folder
        fields = ['id', 'name', 'user','folders', 'parents', 'is_deleted'] 
    
class FolderSerilizers(serializers.ModelSerializer):
    folders = serializers.CharField(required=True)
    class Meta:
        model = Folder
        fields = ['id', 'name', 'user','folders', 'parents','is_starred'] 
    
    def create(self, validated_data):
        name = validated_data.get('name')
        user = validated_data.get('user')
        folders = validated_data.get('folders')
        folderobj = get_object_or_404(Folder, pk=folders)
        userobj = get_object_or_404(User, pk = user)
        parents = validated_data.get('parents')
        folder = Folder(name=name, user=userobj, parents = parents)
        folder.save()
        folder.folders.add(folderobj)
        return folder


class FileSerilizers(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'document', 'user', 'parent', 'name', 'size', 'extension','is_starred']
    

class FileGetSerilizers(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'extension', 'document', 'user', 'parent'] 

class RenameFileSerilizers(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'document', 'user', 'parent',]
    
    def create(self, validated_data):
        file = File(name=validated_data['name'])
        file.save(client='client')
        return file