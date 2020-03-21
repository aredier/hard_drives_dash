FROM eu.gcr.io/chariots-poc/ml_back/common:latest

COPY ./requirements.txt /opt/requirements.txt

WORKDIR /opt/

RUN pip install -r requirements.txt
RUN pip install -e git://github.com/aredier/chariots.git@aa875ad1a0afef5519d7e5c58a72ebbffb410045#egg=chariots


WORKDIR /usr/src/app/
ADD ./ /usr/src/app/ml_back
