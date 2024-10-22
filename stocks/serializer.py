from rest_framework import serializers

class BacktestSerializer(serializers.Serializer):
    initial_investment = serializers.FloatField()
    short_moving_average = serializers.IntegerField()
    long_moving_average = serializers.IntegerField()
