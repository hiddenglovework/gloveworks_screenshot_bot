# FROM seleniarm/standalone-chromium:114.0

# # Install additional packages if needed
# RUN set -eux \
#   && sudo apt-get update \
#   && sudo apt-get install -y \
#     python3-pip \
#     python3-discord \
#     python3-selenium \ 
#   && sudo apt-get clean

# RUN set -eux \
#   && pip3 install --break-system-packages \
#     apscheduler==3.10.1 \
#     discord_ext_bot==1.0.1 \
#     webdriver_manager==3.8.6

# COPY discord_screenshot_bot.py /usr/local/sbin/gw-discord-ss-bot 


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

# CMD ["sleep","3600"]