import logging
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from models import Us, World, Politics, Business

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler("news_remover.log"),
                logging.StreamHandler()
            ]
        )
        
        models = [Us, World, Politics, Business]
        one_week_ago = timezone.now() - timedelta(days=7)

        for model in models:
            try:
                old_articles = model.objects.filter(published_date__lt=one_week_ago)
                deleted_count, _ = old_articles.delete()
                logging.info(f"Deleted {deleted_count} old articles from {model.__name__}.")
            except Exception as e:
                logging.error(f"Failed to delete old articles from {model.__name__}: {e}", exc_info=True)
