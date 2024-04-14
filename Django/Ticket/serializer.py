from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *

class TicketSerializer(ModelSerializer):
    questions_count = serializers.SerializerMethodField()
    answers_count = serializers.SerializerMethodField()

    def get_questions_count(self, ticket):
        count = TicketQuestion.objects.filter(ticket=ticket).count()
        return count

    def get_answers_count(self, ticket):
        count = TicketAnswer.objects.filter(ticket=ticket).count()
        return count

    class Meta:
        model = Ticket
        fields = '__all__'




class TicketQuestionSerializer(ModelSerializer):
    class Meta:
        model = TicketQuestion
        fields = '__all__'



class TicketAnswerSerializer(ModelSerializer):
    class Meta:
        model = TicketAnswer
        fields = '__all__'