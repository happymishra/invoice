FROM python:3.7.5-slim

RUN useradd -m -s /bin/bash -d /home/jenkins jenkins
WORKDIR /home/jenkins/invoice
COPY ./requirements.txt /home/jenkins/invoice

RUN python -m pip install -r /home/jenkins/invoice/requirements.txt

COPY . /home/jenkins/invoice

RUN chown -R jenkins:jenkins /home/jenkins/invoice/ \
    && chmod -R 775 /home/jenkins/invoice/ \
    && mkdir -p /var/log/invoice \
    && chown  -R jenkins:jenkins /var/log/invoice \
    && mkdir -p /home/jenkins/invoice/staticfiles/ \
    && chown -R jenkins:jenkins /home/jenkins/invoice/staticfiles/ \
    && mkdir -p /home/jenkins/invoice/media/ \
    && chown -R jenkins:jenkins /home/jenkins/invoice/media/
