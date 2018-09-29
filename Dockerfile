
# This is an auto generated Dockerfile for ros:ros-core
# generated from docker_images/create_ros_core_image.Dockerfile.em
FROM ubuntu:xenial

# install packages
RUN apt-get update && apt-get install -q -y \
    dirmngr \
    gnupg2 \
    lsb-release \
    && rm -rf /var/lib/apt/lists/*

# setup keys
RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 421C365BD9FF1F717815A3895523BAEEB01FA116

# setup sources.list
RUN echo "deb http://packages.ros.org/ros/ubuntu `lsb_release -sc` main" > /etc/apt/sources.list.d/ros-latest.list

# install bootstrap tools
RUN apt-get update && apt-get install --no-install-recommends -y \
    python-rosdep \
    python-rosinstall \
    python-vcstools \
    python-pip \
    && rm -rf /var/lib/apt/lists/*

# setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# bootstrap rosdep
RUN rosdep init \
    && rosdep update

# install ros packages
ENV ROS_DISTRO kinetic
RUN apt-get update && apt-get install -y \
    ros-kinetic-ros-core=1.3.2-0* \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --upgrade pip
RUN pip2 install psycopg2 


RUN apt-get update
RUN apt-get install -y postgresql postgresql-contrib
RUN apt-get -y install python3-pip
RUN apt install -y vim
RUN apt-get -y install libyaml-cpp-dev

RUN pip3 install pyyaml
RUN pip3 install psycopg2
RUN pip3 install pandas 
RUN pip3 install numpy
RUN pip3 install psycopg2 
RUN pip3 install psycopg2-binary
RUN pip3 install --upgrade pip
RUN pip2 install --upgrade pip

RUN mkdir -p /home/tmp1 && mkdir -p /home/tmp2

#COPY ./temp_folder /home
#COPY ./bag_to_csv_bash.py /
#COPY ./database_dump_csv_bash.py /
#COPY ./database_dump_bag_file_bash.py /
#COPY ./json_parser_bash.py / 
#COPY ./automate.sh /
#COPY ./testing_.bag /

#RUN iptables -t nat -L -n
# setup entrypoint
COPY ./ros_entrypoint.sh /

ENTRYPOINT ["/ros_entrypoint.sh"]



CMD ["bash"]
#install libraries 

