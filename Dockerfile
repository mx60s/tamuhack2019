FROM python:3
COPY main.py /tmp
COPY requirements.txt /tmp
WORKDIR /tmp

COPY pa_stable_v19_20140130.tgz /tmp
RUN tar -xvf /tmp/pa_stable_v19_20140130.tgz
WORKDIR /tamuhack2019/tmp/portaudio

RUN cd /tamuhack2019/tmp/portaudio \
    && ./configure \
    && make

RUN pip install -r requirements.txt

CMD [ "python", "main.py"]