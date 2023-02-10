ARG BASE_IMAGE=ubuntu
FROM ${BASE_IMAGE}

RUN echo "Running AutoBlender container"
RUN apt update && apt dist-upgrade -y && apt-get install python3 python3-pip git libxrender1 libxxf86vm-dev libxfixes-dev libxi-dev libxkbcommon-dev libegl-dev openexr -y && apt-get clean -y

ADD . /autoblender/

RUN useradd -m autoblender && cp /root/.bashrc /autoblender/ && chown -R --from=root autoblender /autoblender
ENV HOME /autoblender
USER autoblender


WORKDIR /autoblender/
RUN pip3 install -r requirements.txt

CMD ["/bin/bash"]