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

# echo "Generate public key from pem file"
# echo ${PEM_FILE} > ~/project/key-pair.pem
# ls -la
# pwd
# chmod 400 ~/project/key-pair.pem
# ssh-keygen -y -f ~/project/key-pair.pem > ~/project/id_rsa.pub

echo "checking for clusters"
export FLASK_CONFIG="$(echo ${FLASK_CONFIG})"
export SECRET_KEY="$(echo ${SECRET_KEY})"

echo "This is the flask config $FLASK_CONFIG"
echo "This is the secret key $SECRET_KEY"


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
        - name: apache
          image: thegaijin/recipeapi
          env:
            - name: FLASK_CONFIG
              value: ${FLASK_CONFIG}
            - name: SECRET_KEY
              value: ${SECRET_KEY}
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
EOF

CLUSTER_NAMES="$(kops get clusters --state=s3://${BUCKET_NAME})"
for name in ${CLUSTER_NAMES}; do
  if [ ${name} == ${CLUSTER_NAME} ]; then
    echo "this is the name ${name}"

    kubectl apply -f ~/project/k8s/recipeapi_deployment.yml
  else
    echo "There is no cluster to deploy to.."
  fi
done


# echo "These are the $CLUSTERS"
# FOUND_CLUSTER=false
# THE_CLUSTER=$(echo ${CLUSTERS} | grep ${CLUSTER_NAME})
# if [[ ${THE_CLUSTER} == ${CLUSTER_NAME} ]]; then
# 	FOUND_CLUSTER=true
# 	break
# fi


# if [ $THE_CLUSTER == false ]; then
# echo "There is no cluster..."
# fi


# if [ $THE_CLUSTER == false ]; then
# 	echo "Creating cluster..."
# 	kops create cluster --dns-zone thegaijin.xyz --zones us-east-1a --master-size t2.micro --node-size t2.micro --name $CLUSTER_NAME --ssh-public-key /home/ubuntu/.ssh/id_rsa.pub --yes
# 	echo "************************ validate cluster **************************"
# 	while true; do
# 	kops validate cluster --name $CLUSTER_NAME | grep 'is ready' &> /dev/null
# 	if [ $? == 0 ]; then
# 		break
# 	fi
# 	  sleep 30
# done
# fi

echo "<<<<<<<<<<<<< get the cluster >>>>>>>>>>>>>"
# kops get clusters
# kubectl cluster-info
# kubectl apply namespace ingress

echo "Add Dashboard"
# kubectl create -f https://raw.githubusercontent.com/kubernetes/kops/master/addons/kubernetes-dashboard/v1.4.0.yaml