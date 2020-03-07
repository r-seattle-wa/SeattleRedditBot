FROM python:alpine3.6
ENV TZ=America/Los_Angeles

WORKDIR /opt/reddit/
COPY . .
RUN apk add -U build-base && \ 
    pip install --no-cache-dir -r requirements.txt && \
    apk del build-base

CMD [ "python", "./daily_post.py" ]
