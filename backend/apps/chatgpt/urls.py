from django.urls import path

from backend.apps.chatgpt.views import ChatBoxView, ChatMessageView

urlpatterns = [
    path('box/', ChatBoxView.as_view({"get": "list", 'post': 'create', 'delete': 'destroy'})),
    path('<str:pk>/box/', ChatBoxView.as_view({'delete': 'destroy'})),
    path('<str:pk>/message/', ChatMessageView.as_view({"get": "list", 'post': 'create'}))

]
