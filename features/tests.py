# Create your tests here.
# features/tests.py

from rest_framework.test import APITestCase
from .models import FeatureFlag
from django.test import TestCase

class FeatureFlagAPITests(APITestCase):

    def test_list_features(self):
        """Probar que la API devuelve la lista de features"""
        # Crear un feature de prueba
        FeatureFlag.objects.create(name="Prueba del test", enabled=True)

        # Hacer petición GET
        response = self.client.get('/api/features/')

        # Verificar que funciona
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Prueba del test')
