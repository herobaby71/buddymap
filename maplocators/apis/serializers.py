from rest_framework import serializers
from django.contrib.auth import get_user_model
from maplocators.models import Locator
import json

class LocatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locator
        fields = ('longitude', 'latitude')
