ARG BASE_IMAGE=ubuntu
FROM ${BASE_IMAGE}

RUN echo "Running AutoBlender container"
RUN apt update && apt dist-upgrade -y && apt-get install python3 python3-pip git libxrender1 libxxf86vm-dev libxfixes-dev libxi-dev libxkbcommon-dev libegl-dev openexr -y && apt-get clean -y
ADD . /autoblender/
WORKDIR /autoblender/
RUN pip3 install -r requirements.txt

USER autoblender

CMD ["/bin/bash"]