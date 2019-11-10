FROM centos:7 

RUN yum -y install wget

# Install Python 3 and libs
RUN yum update -y
RUN yum -y install yum-utils
RUN yum groupinstall "Development Tools" -y
RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm
RUN yum -y install python36u
RUN yum -y install python36u-pip
RUN yum -y install python36u-devel
RUN pip3.6 install --upgrade pip
RUN pip3.6 install numpy

# install chrome browser and chromium driver
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
RUN yum install -y ./google-chrome-stable_current_x86_64.rpm
RUN yum install -y chromium
RUN wget https://chromedriver.storage.googleapis.com/74.0.3729.6/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/lib64/chromium-browser/

# prerequisites for opencv
RUN yum install cmake3 gcc gtk2-devel numpy pkconfig -y
RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip
RUN yum install -y libjpeg-devel libpng-devel libtiff-devel
RUN yum install -y libavcodec-devel libavformat-devel libswscale-devel libv4l-devel
RUN yum install -y atlas-devel gcc-gfortran

# opencv
RUN wget -O opencv.zip https://github.com/opencv/opencv/archive/4.0.0.zip
RUN wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.0.0.zip
RUN unzip opencv.zip -d /opt
RUN unzip opencv_contrib.zip -d /opt
RUN mv /opt/opencv-4.0.0 /opt/opencv
RUN mv /opt/opencv_contrib-4.0.0 /opt/opencv_contrib
RUN mkdir -p /opt/opencv/build
WORKDIR /opt/opencv/build
COPY xcmake.sh .
RUN chmod 0755 xcmake.sh
RUN ./xcmake.sh
RUN make -j4
RUN make install
RUN ldconfig
