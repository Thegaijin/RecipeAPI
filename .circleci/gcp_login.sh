#!/bin/bash
ROOT_DIR=$(pwd)

generateServiceAccount() {
  touch $ROOT_DIR/shared/account.json
  echo ${SERVICE_ACCOUNT} > $ROOT_DIR/shared/account.json
}

activateServiceAccount() {
  # setup kubectl auth
  gcloud auth activate-service-account --key-file $ROOT_DIR/shared/account.json
  echo $ROOT_DIR
  gcloud --quiet config set project ${GCP_PROJECT_ID}
  gcloud --quiet config set compute/zone ${COMPUTE_ZONE}
  gcloud --quiet container clusters get-credentials ${CLUSTER_NAME}
  fi
  gcloud config list
}

main(){
  generateServiceAccount
  activateServiceAccount
}

main $@