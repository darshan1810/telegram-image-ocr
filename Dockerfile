FROM ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive 
RUN apt-get update \
    && apt install -y tesseract-ocr python3 python3-pip \
    && apt-get clean \
    && apt-get autoremove

ADD . /home/App
WORKDIR /home/App
COPY requirements.txt ./
COPY . .

RUN pip3 install -r requirements.txt

VOLUME ["/img"]
CMD ["python3", "monitor_telegram.py"]
