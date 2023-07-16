FROM seleniarm/standalone-chromium:114.0

# Install additional packages if needed
RUN set -eux \
  && sudo apt-get update \
  && sudo apt-get install -y \
    python3-pip \
    python3-discord \
    python3-selenium \ 
  && sudo apt-get clean

RUN set -eux \
  && pip3 install --break-system-packages \
    apscheduler==3.10.1 \
    discord_ext_bot==1.0.1 \
    webdriver_manager==3.8.6

COPY discord_screenshot_bot.py /usr/local/sbin/gw-discord-ss-bot 
