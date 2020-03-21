FROM eu.gcr.io/chariots-poc/ml_back/common:latest

COPY ./requirements.txt /opt/requirements.txt

WORKDIR /opt/

RUN pip install -r ml_back/requirements.txt
RUN pip install -e git://github.com/aredier/chariots.git@e7f6ebc34455c574574d39f6350b83fe4767780f#egg=chariots
