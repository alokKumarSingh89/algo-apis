FROM python:3.11-slim

COPY . /app/

WORKDIR /app/

#Default installs
RUN apt-get update && \
    apt-get install -y \
    build-essential\
    python3-dev \
    python3-setuptools \
    gcc \
    make

#Create virtual environment
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/python -m pip install pip --upgrade && \
    /opt/venv/bin/python -m pip install -r /app/src/requirements.txt


#Purge unused
RUN apt-get remove -y --purge make gcc build-essential \
    && apt-get autoremove -y \
    && rm -rvf /var/lib/apt/lists/*

#make executable to entrypoint
RUN chmod +x ./src/entrypoint.sh

#RUn
CMD ["./src/entrypoint.sh"]