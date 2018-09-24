# Docker image for Tweet-Toot project.
FROM ubuntu
MAINTAINER ayushsharma.22+tweettoot@gmail.com

ARG mastodon_token
ARG papertrail_token

RUN cd /root;\
	apt-get -y update;\
	apt-get -y upgrade;\
	apt-get -y install python3 python3-pip git wget cron;\
	git clone https://github.com/ayush-sharma/tweet-toot.git;\
	cd tweet-toot;\
	pip3 install -r requirements.txt;\
	apt-get -y purge python3-pip git;\
	apt-get -y install python3-idna;\
	apt-get -y autoremove;\
	apt-get -y autoclean;\
	# Configure Tweet-Toot
	sed -i 's/"toots.app_secure_token": ""/"toots.app_secure_token": "'$mastodon_token'"/g' config.json

# Install Papertrail agent
RUN wget -qO - --header="X-Papertrail-Token: "$papertrail_token https://papertrailapp.com/destinations/10693082/setup.sh | bash;\
	wget - https://github.com/papertrail/remote_syslog2/releases/download/v0.20/remote-syslog2_0.20_amd64.deb;\
	dpkg -i remote-syslog2_0.20_amd64.deb;\
		remote_syslog \
		  -p 22420 \
		  -d logs7.papertrailapp.com \
		  --pid-file=/var/run/remote_syslog.pid \
		  /tmp/tweet-toot.log;\
	apt-get -y purge wget

RUN crontab -l > /tmp/crontab;\
	echo '* * * * * cd /root/tweet-toot; python3 /root/tweet-toot/run.py >> /tmp/tweet-toot.log' >> /tmp/crontab;\
	crontab /tmp/crontab