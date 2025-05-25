#sections\serializers.py
from rest_framework import serializers
from .models import Section, Content

class SectionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') # Отображаем имя владельца

    class Meta:
        model = Section
        fields = '__all__' # Или укажите нужные поля


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'