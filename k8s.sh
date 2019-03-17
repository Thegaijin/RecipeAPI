echo "Get s3 bucket..."
# Check available buckets
buckets="$(aws s3api list-buckets | jq -r '.Buckets')"
found_bucket=false
echo "This is a bucket: ${BUCKET_NAME}"
# check if bucket already exists
echo "Checking for bucket"
for name in $( echo ${buckets} | jq -c '.[]'); do
	bucket_names=$(echo ${name} | jq -r '.Name')
	the_bucket=$(echo ${bucket_names} | grep ${BUCKET_NAME})
	if [[ ${the_bucket} == ${BUCKET_NAME} ]]; then
	found_bucket=true
	break
	fi
done

echo "creating bucket"
if [ ${found_bucket} == false ]; then
	echo "Create the bucket..."
	export BUCKET_NAME=${BUCKET_NAME}
	aws s3api create-bucket --bucket ${BUCKET_NAME}
	export KOPS_STATE_STORE=s3://${BUCKET_NAME}
fi

echo "setting env vars"
export FLASK_CONFIG="$(echo ${FLASK_CONFIG})"
export SECRET_KEY="$(echo ${SECRET_KEY})"
export DATABASE_URL="$(echo ${DATABASE_URL})"

echo "Creating the deployment yml file"
sudo cat <<EOF > ~/project/k8s/recipeapi_deployment.yml
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: recipeapi
spec:
  replicas: 1
  template:
    metadata:
      labels:
        app: recipeapi
    spec:
      containers:
        - name: recipeapi
          image: thegaijin/recipeapi:{{ IMG_TAG }}
          env:
            - name: FLASK_CONFIG
              value: ${FLASK_CONFIG}
            - name: SECRET_KEY
              value: ${SECRET_KEY}
            - name: DATABASE_URL
              value: ${DATABASE_URL}
          ports:
            - containerPort: 80
---
apiVersion: v1
kind: Service
metadata:
  name: recipeapi
  labels:
    app: recipeapi
spec:
  type: LoadBalancer
  externalTrafficPolicy: Cluster
  ports:
    - port: 80
      targetPort: 80
      nodePort: 31818
  selector:
    app: recipeapi
---
apiVersion: batch/v1
kind: Job
metadata:
  name: recipeapi-migrations-job
  namespace: default
spec:
  ttlSecondsAfterFinished: 100
  template:
    metadata:
      name: recipeapi-migrations
    spec:
      containers:
        - name: recipeapi-migrations
          image: thegaijin/recipeapi:{{ IMG_TAG }}
          command:
            - python
            - manage.py
            - db
            - upgrade
          env:
          - name: FLASK_CONFIG
            value: ${FLASK_CONFIG}
          - name: DATABASE_URL
            value: "{{ DATABASE_URL }}"
      restartPolicy: Never
EOF

CLUSTER_NAMES="$(kops get clusters --state=s3://${BUCKET_NAME})"
for name in ${CLUSTER_NAMES}; do
  if [ ${name} == ${CLUSTER_NAME} ]; then
    echo "this is the name ${name} of the cluster"
    echo $IMG_TAG
    # kops export kubecfg ${CLUSTER_NAME} --state=s3://${BUCKET_NAME}
    kubectl apply -f ~/project/k8s/recipeapi_deployment.yml
  else
    echo "There is no cluster to deploy to.."
  fi
done
