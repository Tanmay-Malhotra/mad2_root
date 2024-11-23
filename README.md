SPOC V2

## starting Redis Server for daily and monthly reminder
redis-server

## to check if a redis server is active on port 6379
sudo ss -tulnp | grep 6379

## To test redis server
redis-cli ping

## Stoping Redis Server
sudo killall redis-server


## start celery worker for daily reminder
    celery -A app.celery_app worker --loglevel=INFO

## start celery beat
    celery -A app.celery_app beat --loglevel=INFO

