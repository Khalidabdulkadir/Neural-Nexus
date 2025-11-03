from rest_framework import viewsets
from .models import Patient
from .serializers import PatientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows patients to be viewed or edited.
    Provides `list`, `create`, `retrieve`, `update`, and `destroy` actions.
    """
    queryset = Patient.objects.all().order_by('-created_at')
    serializer_class = PatientSerializer

