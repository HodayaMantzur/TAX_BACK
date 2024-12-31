from rest_framework.viewsets import ModelViewSet
from .models import Calculation
from .serializers import CalculationSerializer

class CalculationViewSet(ModelViewSet):
    queryset = Calculation.objects.all()
    serializer_class = CalculationSerializer
