#!/bin/bash
cd /Users/yback/projects/django/news_crawler/backend
source /Users/yback/projects/django/news_crawler/myvenv/bin/activate

LOG_DIR="/Users/yback/projects/django/news_crawler/backend/cron_logs"
NEWS_CRAWLER_LOG_FILE="$LOG_DIR/news_crawler_$(date +\%Y-\%m-\%d).log"

python manage.py news_crawler >> $NEWS_CRAWLER_LOG_FILE 2>&1
