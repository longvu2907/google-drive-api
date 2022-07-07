from image.models import Image
from image.serializers import ImageSerializer

from google_drive.gdrive import get_files_list

def update_database():
    images = get_files_list()

    for image in images:
        instance = Image.objects.filter(id=image['id']).first()

        if instance and image['trashed']:
            instance.delete()
            continue

        if instance is None:
            if not image['trashed']:
                create_serializer = ImageSerializer(data=image)
            else:
                continue
        else:
            create_serializer = ImageSerializer(instance, data=image)

        if create_serializer.is_valid(raise_exception=True):
            create_serializer.save()
