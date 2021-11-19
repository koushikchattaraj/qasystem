from django.urls import path
from . import views


app_name= 'drive'

urlpatterns = [
    path('newdrive/', views.NewDriveView.as_view(), name="newdrive"),
    path('api/folder/', views.ApiFolder.as_view(), name="ApiFolder"),
    path('api/mainfolder/', views.ApiMainFolder.as_view(), name="ApiFolder"),
    path('api/starfolder/', views.StarFolder.as_view(), name="ApiFolder"),
    path('api/starfile/', views.StarFile.as_view(), name="ApiFile"),
    path('api/file/', views.ApiMainFile.as_view(), name="ApiFile"),
    path('api/folderfile/', views.FullFolderUpload.as_view(), name="ApiFolderFile"),
    path('api/subfile/<int:pk>', views.ApiSubFile.as_view(), name="ApisubFile"),
    path('newdrive/<int:pk>', views.FolderByIdView.as_view(), name="folderdrive"),
    path('api/folder/<int:pk>', views.FolderByIdApi.as_view(), name="folderapidrive"),
    path('api/trashfolder/<int:pk>', views.TrashFolderByIdApi.as_view(), name="trashfolderapidrive"),
    path('api/trashmainfolder/', views.ApiTrashMainFolder.as_view(), name="ApiTrashFolder"),
    path('api/recentfolder/', views.ApiRecentMainFolder.as_view(), name="ApiRecentFolder"),
    path('api/recentfile/', views.ApiRecentMainFile.as_view(), name="ApiRecentFile"),

]   