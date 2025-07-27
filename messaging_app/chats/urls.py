from django.urls import include, path
from chats.views import ConversationViewSet, MessageViewSet
from rest_framework import routers
from rest_framework_nested.routers import NestedDefaultRouter


# main_router = routers.DefaultRouter()
# main_router.register(
#    r"conversations", ConversationViewSet, basename="conversations"
# )

# conversations_router = NestedDefaultRouter(
#    main_router, r"conversations", lookup="conversation"
# )

app_router = routers.DefaultRouter()
app_router.register(
    r"conversations", ConversationViewSet, basename="conversations"
)

"""crate conversations router first based on default router"""
conversations_router = NestedDefaultRouter(
    app_router, r"conversations", lookup="conversation"
)

"""nest messages routing inside conversations"""
conversations_router.register(
    r"messages", MessageViewSet, basename="conversation-messages"
)


urlpatterns = [
    # path("", include((main_router.urls, "chats"), namespace="chats")),
    path("", include(app_router.urls)),
    path("", include(conversations_router.urls)),
]
