from rest_framework import serializers


class ErrorMessageResponseSerializer(serializers.Serializer):
    error_code = serializers.IntegerField()
    error_message = serializers.CharField()

class ErrorMessageResponse(object):
    def __init__(self, error):
        self.error_code = error[0]
        self.error_message = error[1]
