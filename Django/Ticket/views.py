from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from Permission.admin import IsAdminMixin
from config.pagination import CustomPagination
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.utils.translation import gettext_lazy as _
from .serializer import *
from .models import *

## Tickets ##

class TicketsOpenViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Ticket.objects.filter(status=True)
    serializer_class = TicketSerializer
    pagination_class = CustomPagination
    search_fields = ['title', 'user__username']


class TicketsCloseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Ticket.objects.filter(status=False)
    serializer_class = TicketSerializer
    pagination_class = CustomPagination
    search_fields = ['title', 'user__username']

###############################################

## Ticket Questions ##

class TicketsQuestionViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = TicketQuestion.objects.all()
    serializer_class = TicketQuestionSerializer
    pagination_class = CustomPagination
    search_fields = ['text', 'ticket__title']

## Ticket Answers ##
class TicketsAnswerViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = TicketAnswer.objects.all()
    serializer_class = TicketAnswerSerializer
    pagination_class = CustomPagination
    search_fields = ['text', 'ticket__title' , 'question__text']

###########################################################

class TicketsWithOutPagination(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    queryset = Ticket.objects.filter(status=True)
    serializer_class = TicketSerializer


class QuestionsWithOutPagination(ListAPIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]
    serializer_class = TicketQuestionSerializer

    def get_queryset(self):
        ticket_id = self.request.GET['ticket']
        return TicketQuestion.objects.filter(ticket_id=ticket_id)


class ChangeTicketStatus(APIView):
    permission_classes = [IsAuthenticated, IsAdminMixin]

    def post(self , request):
        if self.request.POST.get('type') == 'open':
            pk = self.request.POST.get('id')
            product = Ticket.objects.get(pk=pk)
            product.status = True
            product.save()

            return Response({'detail': _('ticket status has been set TRUE')}, 200)
        else:
            pk = self.request.POST.get('id')
            product = Ticket.objects.get(pk=pk)
            product.status = False
            product.save()

            return Response({'detail': _('ticket status has been set FALSE')}, 200)

