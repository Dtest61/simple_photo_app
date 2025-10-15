from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Photo
from .serializers import PhotoSerializer
from .permissions import IsOwner

import os
import zipfile
from io import BytesIO

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Photo


def index_view(request):
    return render(request, 'index.html')


class PhotoListCreateView(generics.ListCreateAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated]

    # 一覧は「自分の写真のみ」
    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user).order_by('-uploaded_at')

    # 作成時に user を自動付与
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PhotoZipDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        photos = Photo.objects.filter(user=request.user).order_by('-uploaded_at')

        buf = BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
            for p in photos:
                file_field = p.image
                if not file_field:
                    continue
                try:
                    # ZIP内のファイル名（ID＋元ファイル名で重複回避）
                    arcname = f"{p.id}_{os.path.basename(file_field.name)}"
                    # 物理パスから直接Zipに詰めるのが一番確実
                    zf.write(file_field.path, arcname=arcname)
                except Exception:
                    # 物理ファイルが見つからないなどの例外はスキップ
                    continue

        buf.seek(0)
        resp = HttpResponse(buf.getvalue(), content_type='application/zip')
        resp['Content-Disposition'] = 'attachment; filename="my_photos.zip"'
        return resp


class PhotoDestroyView(generics.DestroyAPIView):
    serializer_class = PhotoSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    # 削除対象も「自分の写真のみ」に限定
    def get_queryset(self):
        return Photo.objects.filter(user=self.request.user)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def photos_exist_view(request):
    hashes = request.data.get('checksums', [])
    exists = set(Photo.objects.filter(
        user=request.user, checksum__in=hashes
    ).values_list('checksum', flat=True))
    return Response({'exists': list(exists)})    