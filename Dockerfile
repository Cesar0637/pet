FROM debian:bullseye-slim

RUN apt-get update
RUN apt-get install apache2 python3 python3-pip libmariadb-dev \
    libapache2-mod-wsgi-py3 python3-dev openssh-client nano -y

# Configure timezone
ENV TZ=America/Mexico_City
RUN ln -snf  /etc/l/usr/share/zoneinfo/$TZocaltime && echo $TZ > /etc/timezone

# Application environment
WORKDIR /app

COPY ./petTrackMx/requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

EXPOSE 80

CMD ["apachectl", "-D", "FOREGROUND"]
