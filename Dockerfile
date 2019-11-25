FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /ybsapi2
WORKDIR /ybsapi2
COPY setup.py /ybsapi2/
RUN python setup.py install
COPY . /ybsapi2/
