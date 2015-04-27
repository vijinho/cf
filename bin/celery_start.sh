#cd processor
celery -A processor.tasks worker --loglevel=info
