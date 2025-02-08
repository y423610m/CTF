FROM ubuntu:24.04

USER root

RUN echo "# --- my scripts ---" >> ~/.bashrc && echo "cd ~/" >> ~/.bashrc

RUN apt update && apt install -y software-properties-common less wget zip vim && \
    add-apt-repository -y ppa:ubuntu-toolchain-r/test

RUN apt install -y build-essential

# CTF 
RUN apt install -y gdb checksec binutils

# pwntool
RUN apt install -y python3-pip && python3 -m pip install --upgrade pwntools ipython --break-system-packages 

# netcat Need to specify "netcat-traditional 1.10-48" or "netcat-openbsd 1.226-1ubuntu2"
RUN apt install -y netcat-openbsd

CMD ["bash"]
