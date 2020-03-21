FROM eu.gcr.io/chariots-poc/ml_back/common:latest

COPY ./requirements.txt /opt/requirements.txt

WORKDIR /opt/

RUN pip install -r requirements.txt
RUN pip install -e git://github.com/aredier/chariots.git@e7f6ebc34455c574574d39f6350b83fe4767780f#egg=chariots


WORKDIR /usr/src/app/
ADD ./ /usr/src/app/ml_back
