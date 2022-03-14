FROM 'ubuntu:latest'
COPY . . 
RUN apt-get update
RUN apt-get install -y python3.8
RUN apt-get install -y python3-pip
RUN pip3 install -U pytest
RUN pip3 install pytest-html
RUN apt-get update
RUN apt-get install -y wget unzip
# Installs the latest internal release, it is 0.11.5-rc.2 on 02/15/2022
RUN wget https://jitx-staging.s3.amazonaws.com/public/ubuntu-bionic/jitx.zip
RUN unzip -p jitx.zip jitpcb.release/scripts/install.sh > install.sh
RUN bash install.sh jitx.zip
ENV PATH "$PATH:/root/.jitx/current/"

