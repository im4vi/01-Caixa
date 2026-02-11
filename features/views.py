# features/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from .models import FeatureFlag
from .serializers import FeatureFlagSerializer
import logging

logger = logging.getLogger(__name__)

@authentication_classes([])
@permission_classes([AllowAny])
class FeatureFlagViewSet(viewsets.ModelViewSet):
    queryset = FeatureFlag.objects.all()
    serializer_class = FeatureFlagSerializer

    def list(self, request):
        """GET /api/features/ - Listar todos"""
        logger.info("Listando features")
        features = FeatureFlag.objects.all()
        serializer = self.get_serializer(features, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """GET /api/features/{id}/ - Obtener uno"""
        try:
            feature = FeatureFlag.objects.get(pk=pk)
            logger.info(f"Feature {pk} obtenido")
            serializer = self.get_serializer(feature)
            return Response(serializer.data)
        except FeatureFlag.DoesNotExist:
            logger.error(f"Feature {pk} no encontrado")
            return Response(
                {"error": "Feature flag no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

    def partial_update(self, request, pk=None):
        """PATCH /api/features/{id}/ - Actualizar enabled"""
        try:
            feature = FeatureFlag.objects.get(pk=pk)
        except FeatureFlag.DoesNotExist:
            logger.error(f"Feature {pk} no encontrado en PATCH")
            return Response(
                {"error": "Feature flag no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(feature, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"Feature {pk} actualizado a enabled={serializer.data['enabled']}")
            return Response(serializer.data)

        logger.warning(f"Datos inválidos en PATCH feature {pk}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
