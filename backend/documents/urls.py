from django.urls import path
from .views import DocumentUploadView, AskQuestionView, ReadStoreView

urlpatterns = [
    path("upload/", DocumentUploadView.as_view()),
    path("ask/", AskQuestionView.as_view()),
    path("store/", ReadStoreView.as_view()),
]
