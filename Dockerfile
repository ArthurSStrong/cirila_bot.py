FROM python:3.8-alpine
#LABEL maintainer="AlexFlipnote <root@alexflipnote.dev>" will leave this for respect, but since this container does not work with original code; Alex is not mainting this

LABEL build_date="2021-10-13"
RUN apk update && apk upgrade
RUN apk add --no-cache git make build-base linux-headers
WORKDIR /discord_bot
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "index.py"]
