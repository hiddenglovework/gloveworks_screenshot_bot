FROM seleniarm/standalone-chromium:114.0

#Install additional packages that does not come pre-installed with seleniarm/standalone-chromium
RUN set -eux \
  && sudo apt-get update \
  && sudo apt-get install -y \
    python3-pip=23.1.2+dfsg-2 \
    python3-discord=2.3.0+dfsg-1 \
    python3-selenium=4.10.0+dfsg-1 \ 
  && sudo apt-get clean

RUN set -eux \
  && pip3 install --break-system-packages \
    apscheduler==3.10.1 \
    discord_ext_bot==1.0.1 \
    webdriver_manager==3.8.6

COPY discord_screenshot_bot.py /usr/local/sbin/gw-discord-ss-bot 
