FROM python:3.5.1-onbuild

COPY ../../common_utils /op/common_utils
COPY ../../ml_back /opt/ml_back

WORKDIR /opt/

RUN pip install common_utils
RUN pip install ml_back


EXPOSE 5000
CMD ["ml_back", "server"]