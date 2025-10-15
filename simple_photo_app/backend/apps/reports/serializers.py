from rest_framework import serializers
from .models import Photo
import hashlib

class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ['id', 'image', 'uploaded_at', 'checksum', 'file_size']
        read_only_fields = ('uploaded_at', 'checksum', 'file_size')

    def create(self, validated_data):
        request = self.context['request']
        f = validated_data['image']
        size = getattr(f, 'size', None)

        # 画像のSHA256を計算
        sha = hashlib.sha256()
        for chunk in f.chunks():
            sha.update(chunk)
        f.seek(0)  # 保存前にポインタ戻す
        checksum = sha.hexdigest()

        # 既存があればそれを返す（重複保存しない）
        exists = Photo.objects.filter(user=request.user, checksum=checksum).first()
        if exists:
            return exists

        return Photo.objects.create(
            user=request.user,
            image=f,
            checksum=checksum,
            file_size=size
        )