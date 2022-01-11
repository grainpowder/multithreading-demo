FROM amazonlinux:2

# -y : automatically choose "yes" for future questions
# This is mandatory since build process is cancelled if certain question is not answered
RUN yum update -y \
    && yum groupinstall -y "Development Tools" \
    && yum install -y python3 python3-pip

ENV APP_PATH /opt/app
ENV PYTHONPATH $APP_PATH/src
COPY src $PYTHONPATH

WORKDIR $APP_PATH
COPY requirements.txt $APP_PATH/requirements.txt
RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt

CMD /bin/bash