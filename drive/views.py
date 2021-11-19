from os import name, rename
from django.http import response
from django.shortcuts import redirect, render
from django.views.generic.base import View
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.decorators import api_view,permission_classes
from .serilizers import FolderSerilizers, FileSerilizers, FileGetSerilizers, FolderMainSerilizers   
from rest_framework import fields, status
from rest_framework.response import Response
from .models import Folder, File
from datetime import date



class NewDriveView(View):
    template_name = 'newdrive.html'

    def get(self, request):
	    return render(request, self.template_name)

class ApiFolder(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        context = {}
        user = Folder.objects.filter(user= request.user.id ,is_deleted=False)
        folder_serilizer = FolderSerilizers(user, many=True)
        context['data'] = folder_serilizer.data
        context['message'] = "Your Folder are"
        context['status'] = status.HTTP_200_OK
        return Response(context, status=status.HTTP_200_OK)



    def post(self, request):
        context = {}
        if request.user.is_authenticated:
            request.data.update({"user":request.user.id})
            if 'folders' in request.data:
                filter_mainfolder = Folder.objects.filter(name=request.data['name'], user=request.user.id, folders=request.data['folders'])
                if filter_mainfolder:
                    context['status'] = status.HTTP_400_BAD_REQUEST
                    context['message'] = "Folder Already Exists!!!!"
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
                else:

                    if 'folders' in request.data:
                        folderserilizer = FolderSerilizers(data=request.data)

                        if folderserilizer.is_valid():
                            folderserilizer.save()
                            foldermainseerilize = FolderMainSerilizers(Folder.objects.get(id=folderserilizer.data['id']),many=False)

                            context['status'] = status.HTTP_200_OK
                            context['data'] = foldermainseerilize.data
                            context['message'] = "Folder is scucessfully created"
                            return Response(context, status=status.HTTP_200_OK)
                        else:
                            context['status'] = status.HTTP_400_BAD_REQUEST
                            context['data'] = FolderSerilizers.errors
                            context['message'] = "Folder is not created"
                            return Response(context, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        folderserilizer = FolderMainSerilizers(data=request.data)
                        if folderserilizer.is_valid():
                            folderserilizer.save()
                            context['status'] = status.HTTP_200_OK
                            context['data'] = folderserilizer.data
                            context['message'] = "Folder is scucessfully created"
                            return Response(context, status=status.HTTP_200_OK)
                        else:
                            context['status'] = status.HTTP_400_BAD_REQUEST
                            context['data'] = FolderSerilizers.errors
                            context['message'] = "Folder is not created"
                            return Response(context, status=status.HTTP_400_BAD_REQUEST)


            else:
                filter_folder = Folder.objects.filter(name=request.data['name'], user=request.user.id)
            if filter_folder:
                context['status'] = status.HTTP_400_BAD_REQUEST
                context['message'] = "Folder Already Exists!!!!"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            else:

                if 'folders' in request.data:
                    folderserilizer = FolderSerilizers(data=request.data)

                    if folderserilizer.is_valid():
                        folderserilizer.save()
                        foldermainseerilize = FolderMainSerilizers(Folder.objects.get(id=folderserilizer.data['id']),many=False)

                        context['status'] = status.HTTP_200_OK
                        context['data'] = foldermainseerilize.data
                        context['message'] = "Folder is scucessfully created"
                        return Response(context, status=status.HTTP_200_OK)
                    else:
                        context['status'] = status.HTTP_400_BAD_REQUEST
                        context['data'] = FolderSerilizers.errors
                        context['message'] = "Folder is not created"
                        return Response(context, status=status.HTTP_400_BAD_REQUEST)
                else:
                    folderserilizer = FolderMainSerilizers(data=request.data)
                    if folderserilizer.is_valid():
                        folderserilizer.save()
                        context['status'] = status.HTTP_200_OK
                        context['data'] = folderserilizer.data
                        context['message'] = "Folder is scucessfully created"
                        return Response(context, status=status.HTTP_200_OK)
                    else:
                        context['status'] = status.HTTP_400_BAD_REQUEST
                        context['data'] = FolderSerilizers.errors
                        context['message'] = "Folder is not created"
                        return Response(context, status=status.HTTP_400_BAD_REQUEST)

            
    def delete(self, request):
        context = {}


        folder = Folder.objects.filter(id=request.data['id'],user=request.user.id).first()
        
        subfolder = Folder.objects.filter(folders=request.data['id'],user=request.user.id).first()
        if folder:
            folder.is_deleted=True
            subfolder.is_deleted=True
            folder.save()
            subfolder.save()

            context['status'] = status.HTTP_200_OK
            context['message'] = "Folder is scucessfully Deleted"
            return Response(context, status=status.HTTP_200_OK)
            
        else:
            context['status'] = status.HTTP_400_BAD_REQUEST
            context['message'] = "Thats not your folder"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        context = {}

        folder = Folder.objects.get(user=request.user.id, id=request.data['id'])
        folder_serilizer = FolderSerilizers(folder, data=request.data, partial=True)
        if folder_serilizer.is_valid():
            folder_serilizer.save()
            context['status'] = status.HTTP_200_OK
            context['message'] = "Folder is scucessfully Updated"
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['status'] = status.HTTP_400_BAD_REQUEST
            context['message'] = folder_serilizer.errors
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

class ApiMainFile(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)


    def get(self, request):
        context = {}
        user = File.objects.filter(user = request.user.id, parent=None)
        file_serilizer = FileGetSerilizers(user, many=True)
        context['data'] = file_serilizer.data
        context['message'] = "Your File are"
        context['status'] = status.HTTP_200_OK
        return Response(context, status=status.HTTP_200_OK)

    def post(self, request):
        context = {}
        if request.user.is_authenticated:

            name = request.data['document'].name
            extension = request.data['document'].name.split(".")[-1]
            size = request.data['document'].size

            request.data.update({"user":request.user.id, "name":name, "extension":extension, "size":size})
            fileserilizer = FileSerilizers(data=request.data)
            filter_file = File.objects.filter(name=request.data['document'], user=request.user.id)
            if filter_file:
                context['status'] = status.HTTP_400_BAD_REQUEST
                context['message'] = "File Already Exists!!!!"
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
            else:
                if fileserilizer.is_valid():
                    fileserilizer.save()
                    context['status'] = status.HTTP_200_OK
                    context['data'] = fileserilizer.data
                    context['message'] = "File is scucessfully created"
                    return Response(context, status=status.HTTP_200_OK)
                else:
                    context['status'] = status.HTTP_400_BAD_REQUEST
                    context['data'] = FolderSerilizers.errors
                    context['message'] = "File is not created"
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        context = {}
        file = File.objects.get(user=request.user.id, id=request.data['id'])
        file_serilizer = FileSerilizers(file, data=request.data, partial=True)
        if file_serilizer.is_valid():
            file_serilizer.save()
            context['status'] = status.HTTP_200_OK
            context['data'] = file_serilizer.data
            return Response(context, status=status.HTTP_200_OK)
        else:
            context['status'] = status.HTTP_400_BAD_REQUEST
            context['message'] = file_serilizer.errors
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

class FolderByIdApi(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    def get(self, request, pk):
        context = {}
        filter_folder = Folder.objects.get(pk=pk)
        filter_folder = Folder.objects.filter(folders=pk, user=request.user.id, is_deleted=False)
        folder_serilizer = FolderSerilizers(filter_folder, many=True)
        context['data'] = folder_serilizer.data
        context['message'] = "Your Folder are"
        context['status'] = status.HTTP_200_OK
        return Response(context, status=status.HTTP_200_OK)


class SubFolder(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def delete(self, request):
        context = {}

        folder = Folder.objects.filter(id=request.data['id'],user=request.user.id).first()

        subfolder = Folder.objects.filter(folders=request.data['id'],user=request.user.id).first()
        if subfolder:
            subfolder.is_deleted=True
            subfolder.save()

            context['status'] = status.HTTP_200_OK
            context['message'] = "Folder is scucessfully Deleted"
            return Response(context, status=status.HTTP_200_OK)
            
        else:
            context['status'] = status.HTTP_400_BAD_REQUEST
            context['message'] = "Thats not your folder"
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

def all_parents(folder):
    list = [folder]
    parent = folder.folders
    while parent.count() != 0:
        temp = parent.all()[0]
        list.insert(0, temp)
        parent = temp.folders
    return list

class FolderByIdView(View):
    template_name = 'drive.html'

    def get(self, request ,pk):
        folder = Folder.objects.get(id=pk)
        parent = [i for i in all_parents(folder)]
        mydict = {"list" : parent}
        parent_folder = folder.folders.all()

        return render(request, self.template_name, mydict)


class ApiMainFolder(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        context = {}
        user = Folder.objects.filter(user= request.user.id, folders=None, is_deleted=False)
        folder_serilizer = FolderSerilizers(user, many=True)
        context['data'] = folder_serilizer.data
        context['message'] = "Your Folder are"
        context['status'] = status.HTTP_200_OK
        return Response(context, status=status.HTTP_200_OK)


class ApiSubFile(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)


    def get(self, request, pk):
        context = {}
        user = File.objects.filter(parent=pk, user = request.user.id)
        file_serilizer = FileGetSerilizers(user, many=True)
        context['data'] = file_serilizer.data
        context['message'] = "Your File are"
        context['status'] = status.HTTP_200_OK
        return Response(context, status=status.HTTP_200_OK)

class ApiTrashMainFolder(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        context = {}
        user = Folder.objects.filter(user= request.user.id, folders=None, is_deleted=True)
        folder_serilizer = FolderSerilizers(user, many=True)
        context['data'] = folder_serilizer.data
        context['message'] = "Your Folder are"
        context['status'] = status.HTTP_200_OK
        return Response(context, status=status.HTTP_200_OK)

class TrashFolderByIdApi(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    def get(self, request, pk):
        context = {}
        filter_folder = Folder.objects.get(pk=pk)
        filter_folder = Folder.objects.filter(folders=pk, user=request.user.id, is_deleted=True)
        folder_serilizer = FolderSerilizers(filter_folder, many=True)
        context['data'] = folder_serilizer.data
        context['message'] = "Your Folder are"
        context['status'] = status.HTTP_200_OK
        return Response(context, status=status.HTTP_200_OK)

class FullFolderUpload(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        context = {}
        files = request.FILES.getlist("document")

        for x in files:
            
            if request.user.is_authenticated:

                name = x.name
                extension = name.split(".")[-1]
                size = x.size

                newdata = ({"user":request.user.id, "name":name, "size":size, 'document':x, 'parent':request.data['parent'],'extension':extension})
                fileserilizer = FileSerilizers(data=newdata)
                if fileserilizer.is_valid():
                    fileserilizer.save()
                    context['status'] = status.HTTP_200_OK
                    context['data'] = fileserilizer.data
                    context['message'] = "File is scucessfully created"
        return Response(context, status=status.HTTP_200_OK)

class StarFolder(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        context = {}
        user = Folder.objects.filter(user=request.user.id ,is_deleted=False, is_starred=True)
        folder_serilizer = FolderSerilizers(user, many=True)
        context['data'] = folder_serilizer.data
        context['message'] = "Your Folder are"
        context['status'] = status.HTTP_200_OK
        return Response(context, status=status.HTTP_200_OK)


    
class StarFile(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        context = {}
        user = File.objects.filter(user=request.user.id ,is_deleted=False, is_starred=True)

        file_serilizer = FileSerilizers(user, many=True)
        context['data'] = file_serilizer.data
        context['message'] = "Your File are"
        context['status'] = status.HTTP_200_OK
        return Response(context, status=status.HTTP_200_OK)


class ApiRecentMainFolder(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        context = {}
        user = Folder.objects.filter(user=request.user.id ,is_deleted=False, created_at=date.today())
        folder_serilizer = FolderSerilizers(user, many=True)
        context['data'] = folder_serilizer.data
        context['message'] = "Your Folder are"
        context['status'] = status.HTTP_200_OK
        return Response(context, status=status.HTTP_200_OK)

class ApiRecentMainFile(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        context = {}
        user = File.objects.filter(user=request.user.id ,is_deleted=False, created_at=date.today())
        file_serilizer = FileSerilizers(user, many=True)
        context['data'] = file_serilizer.data
        context['message'] = "Your File are"
        context['status'] = status.HTTP_200_OK
        return Response(context, status=status.HTTP_200_OK)