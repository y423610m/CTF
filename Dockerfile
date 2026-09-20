FROM ubuntu:24.04

USER root

# basic tools
RUN apt update && apt install -y software-properties-common git less wget zip vim build-essential
RUN add-apt-repository -y ppa:ubuntu-toolchain-r/test

# CTF tools
RUN apt install -y gdb checksec binutils

# netcat Need to specify "netcat-traditional 1.10-48" or "netcat-openbsd 1.226-1ubuntu2"
RUN apt install -y netcat-openbsd


USER ubuntu

RUN git clone https://github.com/longld/peda.git ~/peda && echo "source ~/peda/peda.py" >> ~/.gdbinit && cp /usr/lib/python3/dist-packages/six.py ~/peda/lib/six.py

# pixi
RUN curl -fsSL https://pixi.sh/install.sh | bash
ENV PATH="/home/ubuntu/.pixi/bin:$PATH"
RUN echo 'eval "$(pixi shell-hook)"' >> ~/.bashrc

CMD ["bash"]

