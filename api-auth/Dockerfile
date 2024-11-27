FROM python:3.9.20-alpine3.19

ENV TZ=Europe/Paris

RUN apk update && apk add --no-cache \
        tzdata \
    && ln -sf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && apk add --no-cache bash \
    && adduser -D -u 1000 appuser

WORKDIR /app
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY --chown=appuser:appuser ./app /app

EXPOSE 80

USER appuser

CMD ["uvicorn", "main:app", "--port", "5000", "--host", "0.0.0.0"]