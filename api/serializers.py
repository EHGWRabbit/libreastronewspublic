from rest_framework import serializers 
from main.models import Bb 

#создаем сериализатор для списка обьявлений
class BbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb 
        fields = ('id', 'title', 'content', 'source', 'created_at')
