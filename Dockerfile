FROM ubuntu:22.04
RUN apt-get update
ENV DEBIAN_FRONTEND=noninteractive

ADD . /hide
WORKDIR /hide

RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa

# RUN apt install -y python3.11 python3.11-dev
RUN apt-get install -y python3-pip
# RUN unlink /usr/bin/python3
# RUN ln -s /usr/bin/python3.11 /usr/bin/python3
# RUN unlink /usr/bin/python3-config
# RUN ln -s /usr/bin/x86_64-linux-gnu-python3.11-config /usr/bin/python3-config

RUN pip3 install sanic==23.12.1
# RUN pip3 install aiohttp-swagger
# RUN pip3 install asyncpg
# RUN pip3 install SQLAlchemy
# RUN pip3 install python-dotenv
RUN pip3 freeze > /hide/requirements.txt

RUN apt install -y git
# RUN apt install -y nginx
# RUN apt-get install -y cron
# RUN apt-get upgrade -y cron
# RUN apt-get install -y ntp
# RUN apt-get install -y redis
# RUN apt install -y postgresql
# RUN apt install -y supervisor

# RUN cp --force ./supervisord.conf /etc/supervisor/
# RUN cp --force ./nginx.conf /etc/nginx/sites-enabled/
# RUN rm /etc/nginx/sites-enabled/default
# RUN mkdir /var/log/hide
# RUN chmod -R 777 /var/log/hide

EXPOSE 80
ENTRYPOINT ["/hide/entrypoint.sh"]
