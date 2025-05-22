import json
from django.core.management.base import BaseCommand

from quiz.models import QuestionCategory, Question, Answer

class Command(BaseCommand):
    help = 'Loads quiz data from JSON file'

    def handle(self, *args, **options):
        with open('quiz_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            category_name = item['category']
            question_text = item['question']
            answers_data = item['answers']
            difficulty = item['difficulty']

            category, _ = QuestionCategory.objects.get_or_create(name=category_name)

            question = Question.objects.create(category=category, text=question_text, difficulty=difficulty)

            for answer_data in answers_data:
                Answer.objects.create(question=question, **answer_data)

        self.stdout.write(self.style.SUCCESS('Successfully loaded quiz data'))