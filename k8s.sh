echo "Get s3 bucket..."
# Check available buckets
buckets="$(aws s3api list-buckets | jq -r '.Buckets')"
found_bucket=false
echo "This is a bucket: ${BUCKET_NAME}"
# check if bucket already exists
for name in $( echo ${buckets} | jq -c '.[]'); do
	bucket_names=$(echo ${name} | jq -r '.Name')
	the_bucket=$(echo ${bucket_names} | grep ${BUCKET_NAME})
	if [[ ${the_bucket} == ${BUCKET_NAME} ]]; then
	found_bucket=true
	break
	fi
done

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

CLUSTERS="$(kops get clusters)"
FOUND_CLUSTER=false
THE_CLUSTER=$(echo ${CLUSTER_NAMES} | grep ${CLUSTER_NAME})
if [[ ${THE_CLUSTER} == ${CLUSTER_NAME} ]]; then
	FOUND_CLUSTER=true
	break
	fi
if


if [ $THE_CLUSTER == false ]; then
	echo "Creating cluster..."
	kops create cluster --dns-zone thegaijin.xyz --zones us-east-1a --master-size t2.micro --node-size t2.micro --name $CLUSTER_NAME --ssh-public-key /home/ubuntu/.ssh/id_rsa.pub --yes
	echo "************************ validate cluster **************************"
	while true; do
	kops validate cluster --name $CLUSTER_NAME | grep 'is ready' &> /dev/null
	if [ $? == 0 ]; then
		break
	fi
	  sleep 30
done
fi

echo "<<<<<<<<<<<<< get the cluster >>>>>>>>>>>>>"
kops get cluster
kubectl cluster-info
# kubectl apply namespace ingress

echo "Add Dashboard"
kubectl create -f https://raw.githubusercontent.com/kubernetes/kops/master/addons/kubernetes-dashboard/v1.4.0.yaml