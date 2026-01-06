from rest_framework import serializers
from .models import Photo, Album


class PhotoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Photo
        fields = ("id", "url", "created_at", "is_deleted", "album")
        extra_kwargs = {
            "album": {"write_only": True},
            "id": {"required": False},
            "created_at": {"required": False},
            "is_deleted": {"required": False},
        }
        

class AlbumSerializer(serializers.ModelSerializer):
    photos = PhotoSerializer(many=True, required=False, source='live_photos')
    
    class Meta:
        model = Album
        fields = "__all__"
        
        extra_kwargs = {
            "id": {"read_only": True, "required": False},
            "created_at": {"read_only": True, "required": False},
            "updated_at": {"read_only": True, "required": False}
        }


