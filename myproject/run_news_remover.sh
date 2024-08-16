#!/bin/bash
cd /Users/yback/projects/django/news_crawler/myproject
source /Users/yback/projects/django/news_crawler/myvenv/bin/activate

LOG_DIR="/Users/yback/projects/django/news_crawler/myproject/cron_logs"
NEWS_REMOVER_LOG_FILE="$LOG_DIR/news_remover_$(date +\%Y-\%m-\%d).log"

python manage.py news_remover >> $NEWS_REMOVER_LOG_FILE 2>&1
