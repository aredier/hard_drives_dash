FROM eu.gcr.io/chariots-poc/ml_back/common-chariots:latest


WORKDIR /usr/src/app/ml_back
RUN pip install ./

WORKDIR /usr/src/app
ADD ./ ./scripts

RUN pip install -r scripts/requirements.txt
RUN pip install -e ml_back/
