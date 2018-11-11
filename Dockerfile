# Docker image for Tweet-Toot project.
FROM ubuntu
MAINTAINER ayushsharma.22+tweettoot@gmail.com

ARG mastodon_token

RUN cd /root;\
	apt-get -y update;\
	apt-get -y upgrade;\
	apt-get -y install python3 python3-pip git wget cron rsyslog;\
	git clone https://github.com/ayush-sharma/tweet-toot.git;\
	cd tweet-toot;\
	pip3 install -r requirements.txt;\
	apt-get -y purge python3-pip git;\
	apt-get -y install python3-idna;\
	apt-get -y autoremove;\
	apt-get -y autoclean;\
	# Configure Tweet-Toot
	sed -i 's/"toots.app_secure_token": ""/"toots.app_secure_token": "'$mastodon_token'"/g' config.json;\

RUN crontab -l > /tmp/crontab;\
	echo '* * * * * cd /root/tweet-toot; python3 /root/tweet-toot/run.py >> /tmp/tweet-toot.log 2>&1' >> /tmp/crontab;\
	crontab /tmp/crontab

RUN touch /tmp/tweet-toot.log

CMD cron && tail -f /tmp/tweet-toot.log