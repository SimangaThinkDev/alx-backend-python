from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Conversation, Message


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone_number", "id")


# class LoginSerializers(serializers.Serializer):
#    email = serializers.CharField(max_length=255)
#    password = serializers.CharField(
#        label=_("password"),
#        style={"input_type": "password"},
#        trim_whitespace=False,
#        max_length=128,
#        write_only=True,
#    )
#
#    def validate(self, data):
#        username = data.get("email")
#        password = data.get("password")
#
#        if username and password:
#            user = authenticate(
#                request=self.context.get("request"),
#                username=username,
#                password=password,
#            )
#            if not user:
#                msg = _("Unable to log in with provided credentials.")
#                raise serializers.ValidationError(msg, code="authorization")
#        else:
#            msg = _('Must include "username" and "password".')
#            raise serializers.ValidationError(msg, code="authorization")
#
#        data["user"] = user
#        return data


class ConversationSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    id = serializers.CharField(max_length=80)

    class Meta:
        model = Conversation

        fields = ["conversationid", "participants", "created_at", "messages"]

    def get_messages(self, obj):
        ret = Message.objects.filter(conversation=obj)
        if not len(ret):
            raise serializers.ValidationError("Empty conversation")
        return MessageSerializer(ret, many=True).data


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token["email"] = user.email
        return token
