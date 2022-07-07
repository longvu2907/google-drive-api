from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from image.models import Image
from image.serializers import ImageSerializer

from google_drive.gdrive import upload_files, get_files_list

def update_database(folder):
    Image.objects.all().delete()

    images = get_files_list(folder)

    create_serializer = ImageSerializer(data=images, many=True)
    if create_serializer.is_valid(raise_exception=True):
        create_serializer.save()

class ImageListView(ListCreateAPIView):
    serializer_class = ImageSerializer
    
    queryset = Image.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filter_fields = ['id', 'category', 'name']
    ordering_fields = ['created_at', 'category']

    def get(self, request, *args, **kwargs):
        folder = None
        try:
            folder = kwargs['folder']
        except:
            pass
        if folder: 
            self.queryset = self.queryset.filter(category=folder)

        return self.list(request)

    def post(self, request, *args, **kwargs):
        folder = None
        try:
            folder = kwargs['folder']
        except:
            pass
        
        if folder is None:
            folder = 'album'

        file_data = request.data['image'].read()
        name = request.data['image'].name
        category = 'album'
        try:
            id, category_id, created_at = upload_files(name, file_data, folder)
            image_url = f"https://drive.google.com/uc?id={id}"
        except Exception as ex:
            print(ex)
            return Response({'errors': 'Upload failed.'}, status=400)
        
        image = {
            'id': id,
            'name': name,
            'image_url': image_url,
            'category': category,
            'category_id': category_id,
            'created_at': created_at
        }

        create_serializer = ImageSerializer(data=image)

        if create_serializer.is_valid():
            todo_item_object = create_serializer.save()
            read_serializer = ImageSerializer(todo_item_object)

            return Response(read_serializer.data, status=201)   

        return Response(create_serializer.errors, status=400)
