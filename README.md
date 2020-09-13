About
==============================

To run
--
```
docker-compose -f local.yml up
```

It will setup DB at first start.
And it will start up two services:
- api (will be available on http://0.0.0.0:81/doc)
- scrapper


To apply db migrations
---
In container `scrapnow_dev_scrapnow_main_1` run
```
scrapnow_alembic scrapnow.db.alembic -c "/opt/conf/alembic.ini" upgrade head
```

Api
--
There are two main methods
- **/article/find_new** - it will try to retrieve new articles from 
url `https://www.reuters.com/news/archive/rates-rss` 
with the specified handler (there is only one for now `reuters_article`)
```
curl -X POST "http://0.0.0.0:81/scrapper/add_task" \
-H "accept: application/json" \
-H "Content-Type: application/json" \
-d "{ \"url\": \"https://www.reuters.com/news/archive/rates-rss\", \"handler\": \"reuters_article\"}"
```
- **/article/retrieve** - it return articles from db for the specified date in iso format.
```
curl -X GET "http://0.0.0.0:81/article/retrieve?date=2020-09-11T00%3A00%3A00.000Z" \
-H "accept: application/json"
```