FROM eu.gcr.io/chariots-poc/ml_back/common:latest

ADD ./ /usr/src/app/ml_back
WORKDIR /usr/src/app/

RUN pip install -r ml_back/requirements.txt
RUN pip install -e git://github.com/aredier/chariots.git@e7f6ebc34455c574574d39f6350b83fe4767780f#egg=chariots

