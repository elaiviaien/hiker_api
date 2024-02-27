from rest_framework import serializers



class SendMail(serializers.Serializer):
    """serializer for city's profile"""
    subject = serializers.CharField()
    email = serializers.CharField()
    message = serializers.CharField()
    name = serializers.CharField()



