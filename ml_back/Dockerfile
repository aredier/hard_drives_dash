FROM eu.gcr.io/chariots-poc/ml_back/common:latest

ADD ./ /usr/src/app/ml_back
WORKDIR /usr/src/app/

RUN pip install -r ml_back/requirements.txt
RUN pip install -e git://github.com/aredier/chariots.git@13290fe50ced2ead85cc7ab5f9346957352bb139#egg=chariots

