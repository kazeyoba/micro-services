FROM python:3.9.20-alpine3.19

ENV TZ=Europe/Paris

RUN apk update && apk add --no-cache \
        tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && apk add --no-cache bash \
    && adduser -D -u 1000 appuser \
    && mkdir -p /data \
    && chown -R appuser:appuser /data

WORKDIR /app

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser ./app /app

USER appuser

EXPOSE 5000

CMD ["python3", "app.py"]