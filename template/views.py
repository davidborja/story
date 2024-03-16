from rest_framework import viewsets
from template.models import Template
from template.template_serializers import TemplateSerializer


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer
