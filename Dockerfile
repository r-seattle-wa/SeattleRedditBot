FROM python:alpine3.6
ENV TZ=America/Los_Angeles

WORKDIR /opt/reddit/
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [ "python", "./daily_post.py" ]
