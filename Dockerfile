FROM alpine:latest

RUN apk add --no-cache python3 chromium chromium-chromedriver

RUN apk add --no-cache py3-pip

ENV CHROME_BIN=/usr/bin/chromium-browser \
    CHROME_DRIVER=/usr/bin/chromedriver

ENV PATH="/usr/bin/chromedriver:${PATH}"
ENV PATH="/usr/bin/chromium:${PATH}" 

WORKDIR /usr/local/gw-discord-ss-bot

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY discord_screenshot_bot.py /usr/local/sbin/gw-discord-ss-bot

CMD ["python3", "/usr/local/sbin/gw-discord-ss-bot"]
