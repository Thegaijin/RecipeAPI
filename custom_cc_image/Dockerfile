FROM ubuntu:16.04

RUN apt-get update
RUN apt-get update && apt-get install -y wget apt-transport-https curl software-properties-common ca-certificates
RUN apt-get install -y build-essential libpq-dev libssl-dev libffi-dev zlib1g-dev && apt-get update
RUN add-apt-repository ppa:jonathonf/python-3.6 && apt-get update && apt-get install -y python3.6 python3-venv python3-pip python3-dev
RUN apt-get update
# RUN sudo wget -q https://storage.googleapis.com/kubernetes-release/release/v1.8.7/bin/linux/amd64/kubectl && sudo chmod +x kubectl && sudo mv kubectl /usr/bin
# RUN sudo wget -q https://github.com/kubernetes/kops/releases/download/1.8.0/kops-linux-amd64 && sudo chmod +x kops-linux-amd64 && sudo mv kops-linux-amd64 /usr/bin/kops
# RUN sudo pip install awscli
# RUN sudo pip install jq
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
RUN apt-get update && apt-get -y install docker-ce
RUN curl https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.tar.gz > /tmp/google-cloud-sdk.tar.gz && \
    mkdir -p /usr/local/gcloud
RUN tar -C /usr/local/gcloud -xvf /tmp/google-cloud-sdk.tar.gz
RUN /usr/local/gcloud/google-cloud-sdk/install.sh
ENV PATH $PATH:/usr/local/gcloud/google-cloud-sdk/bin

# install beta components
RUN gcloud components install beta kubectl --quiet
RUN curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
RUN chmod +x /usr/local/bin/docker-compose
RUN apt-add-repository ppa:ansible/ansible && apt-get update && apt-get install -y ansible
RUN apt-get install -y python-pip && pip install openshift
