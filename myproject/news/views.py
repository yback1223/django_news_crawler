# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Us, World, Politics, Business
from .news_serializers import UsSerializer, WorldSerializer, PoliticsSerializer, BusinessSerializer

class NewsListView(APIView):
    def get(self, request):
        us_news = Us.objects.all()
        world_news = World.objects.all()
        politics_news = Politics.objects.all()
        business_news = Business.objects.all()

        all_news = {
            'us': UsSerializer(us_news, many=True).data,
            'world': WorldSerializer(world_news, many=True).data,
            'politics': PoliticsSerializer(politics_news, many=True).data,
            'business': BusinessSerializer(business_news, many=True).data,
        }

        return Response(all_news)
