FROM python:3.8


RUN apt update
WORKDIR /var/project

COPY ./requirements.txt ./
COPY ./dev-requirements.txt ./

RUN pip3 install -r ./requirements.txt
RUN pip3 install -r ./dev-requirements.txt

COPY ./ ./

RUN cat VERSION | xargs pysemver bump patch | tee VERSION
RUN python3 setup.py sdist bdist_wheel

