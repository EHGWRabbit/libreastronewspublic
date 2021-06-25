from rest_framework import serializers 
from main.models import Bb 
from main.models import Comment

#создаем сериализатор для списка новостей
class BbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb 
        fields = ('id', 'title', 'content', 'source', 'created_at')


#сериализатор выдающий сведения об новости
class BbDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb 
        fields = ('id', 'title', 'content', 'source', 'created_at', 'contacts', 'image')


#сериализатор для выводы списка комментариев
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment 
        fields = ('bb', 'author', 'content', 'created_at')