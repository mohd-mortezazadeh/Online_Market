from django.urls import path , include
from .views import *
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('open' , TicketsOpenViewSet)
router.register('close' , TicketsCloseViewSet)
router.register('questions' , TicketsQuestionViewSet)
router.register('answers' , TicketsAnswerViewSet)

urlpatterns = [
    path('' , include(router.urls)),
    path('all/open/' , TicketsWithOutPagination.as_view()),
    path('all/questions/' , QuestionsWithOutPagination.as_view()),
    path('change/status/' , ChangeTicketStatus.as_view())
]
