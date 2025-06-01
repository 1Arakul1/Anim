# quiz\serializers.py
from rest_framework import serializers
from .models import QuestionCategory, Question, Answer

class QuestionCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionCategory
        fields = '__all__'
        read_only_fields = ('id',)  # ID только для чтения

class QuestionSerializer(serializers.ModelSerializer):
    category = QuestionCategorySerializer(read_only=True) # Сериализуем категорию
    class Meta:
        model = Question
        fields = '__all__'
        read_only_fields = ('id',)  # ID только для чтения

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
        read_only_fields = ('id',)  # ID только для чтения

class CheckAnswerSerializer(serializers.Serializer):
    question_id = serializers.IntegerField(help_text="ID вопроса")
    answer_id = serializers.IntegerField(help_text="ID ответа")