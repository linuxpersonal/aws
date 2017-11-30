## Run the command to build -- AWSCli + Boto3 Script Execution
## docker build --build-arg access_key=Insert access key --build-arg secret_access_key=insert secret access key --build-arg region=insert region -t awscli .

FROM ubuntu:latest
LABEL maintainer "Chris Do <chris.d@linuxpersonal.com>"

ARG region
ARG access_key
ARG secret_access_key

RUN apt-get update && apt-get install -y \
    awscli \
    python3-pip \
    && pip3 install boto3 \
    && mkdir /root/.aws/ \
    && echo "PATH=$PATH:/aws-scripts" > /etc/environment \
    && { \
                echo '[default]'; \
                echo 'output = json'; \
                echo "region = $region"; \
        echo "aws_access_key_id = $access_key"; \
                echo "aws_secret_access_key = $secret_access_key"; \
        } > /root/.aws/config \
    && { \
                echo '[default]'; \
        echo "aws_access_key_id = $access_key"; \
                echo "aws_secret_access_key = $secret_access_key"; \
    } > /root/.aws/credentials

WORKDIR "/aws-scripts"
CMD ["/bin/bash"]
