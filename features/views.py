from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import FeatureFlag
from .serializers import FeatureFlagSerializer

class FeatureFlagViewSet(viewsets.ModelViewSet):
    queryset = FeatureFlag.objects.all()
    serializer_class = FeatureFlagSerializer

    # GET /api/features/
    def list(self, request):
        features = FeatureFlag.objects.all()
        serializer = self.get_serializer(features, many=True)
        return Response(serializer.data)

    # PATCH /api/features/{id}/
    def partial_update(self, request, pk=None):
        try:
            feature = FeatureFlag.objects.get(pk=pk)
        except FeatureFlag.DoesNotExist:
            return Response(
                {"error": "Feature flag no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(feature, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
