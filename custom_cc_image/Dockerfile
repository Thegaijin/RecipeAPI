FROM ubuntu:16.04

RUN apt-get update
RUN apt-get update && apt-get install -y wget apt-transport-https curl software-properties-common
RUN apt-get install -y build-essential libpq-dev libssl-dev libffi-dev zlib1g-dev && apt-get update
RUN add-apt-repository ppa:jonathonf/python-3.6 && apt-get update && apt-get install -y python3.6 python3-venv python3-pip python3-dev
RUN apt-get update
# RUN sudo wget -q https://storage.googleapis.com/kubernetes-release/release/v1.8.7/bin/linux/amd64/kubectl && sudo chmod +x kubectl && sudo mv kubectl /usr/bin
# RUN sudo wget -q https://github.com/kubernetes/kops/releases/download/1.8.0/kops-linux-amd64 && sudo chmod +x kops-linux-amd64 && sudo mv kops-linux-amd64 /usr/bin/kops
# RUN sudo pip install awscli
# RUN sudo pip install jq
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz && \
    mkdir -p /usr/local/gcloud
RUN tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz
RUN /usr/local/gcloud/google-cloud-sdk/install.sh
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

# install beta components
RUN gcloud components install beta kubectl --quiet