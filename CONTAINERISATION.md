# Containerising the app

The first step was to create a custom CI image installing all the deployment related tools that will be used for deployment that way we don't lose time during CI/CD installing them every time. The Dockerfile for this image can be found in the custom_cc_image folder. If you want to use the same image, change into the custom_ci_image directory and build the image and tag it with this command.

    docker build -t <your_dockerhub_username>/<image_name> .

To check the integrity of the image created you can run the command below. It should return `OK` if it is, otherwise, `Corrupted`. If it returns the latter, try to recreate the image and check it again.

    docker save <your_dockerhub_username>/<image_name> > /dev/null && echo 'OK' || echo 'Corrupted'

Once you have verified that the image is OK, push it to your dockerhub account

    docker push <your_dockerhub_username>/<image_name>

After pushing the image, head over to the circleci `config.yml` file and change the image used to this one.

The second step was to create a Dockerfile for the application image as well as a docker-compose file to use to configure it and an env file with the variables. The env file is to be used if you would like to build the image locally. It should not be pushed to github. For the CI, we set the variables in the CircleCI environment variables.

Once the Dockerfile and docker-compose files have been created, test if they have been setup correctly by running, `docker-compose up`. When you want to stop the container, run `docker-compose down`. Once you confirm the integrity of the created files, you are ready to use the containers for deployment.

### DEPLOYMENT

---

We shall be deploying to a Kubernetes cluster on AWS. If you have never used Kubernetes before, the documentation is a great place to start.

First we install the [aws cli](https://aws.amazon.com/cli/) tool. Assumptions have been made that you are running them on a MacOS machine that has [brew](https://brew.sh/) installed and that you already have an [AWS](https://aws.amazon.com/) account and an [IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) role setup.

- To install run `brew install awscli`
- Setup your awscli to work with your aws account run `aws configure`. This brings up a prompt to enter your AWS_ACCESS_KEY_ID and the AWS_SECRET_KEY_ID the default region you would like to work with and the default output format. We will only focus on the the access key and secret key. These can be found under your user credentials on AWS. Once you have set them we can proceed.
- We create an S3 bucket by running `aws s3api create-bucket --bucket <your_bucket_name>`.
  Then create the cluster (An assumption has also been made here that you already have a public key. If you don't have one, create one)
- To create the cluster, we need to install [kops](https://github.com/kubernetes/kops), a tool for managing clusters. run `brew install kops` to install kops.
- Create the cluster by running the command below.

  kops create cluster --node-count 2 --zones us-east-1a --master-zones us-east-1a --node-size t2.micro --master-size t2.micro <name of cluster> --yes

- Once the cluster has been created, validate that it is up and running.
  Run `kops validate cluster <name of cluster>`

The created cluster is where we will be deploying our application. Set the name of that bucket and the cluster in the circleci variables as **BUCKET_NAME** and **CLUSTER_NAME** respectively. These variable names have already been set in the script `k8s.h` which is run to handle the kubernetes deployment. Should you choose to use different variable names, you will have to change them in the script as well.

In the CI/CD pipeline, once the tests have passed, we build the docker image and push it to dockerhub at this [step](https://github.com/Thegaijin/RecipeAPI/blob/da63804392d6ab6f2f1850453fc81edff491b50d/.circleci/config.yml#L64). That is followed by running the `k8s.sh` script.

### The script

In the [script](https://github.com/Thegaijin/RecipeAPI/blob/api_defence/k8s.sh) we verify that the S3 bucket exists, if it doesn't it is created. Then we append the details of the kubernetes deployment and service to an empty yaml file in the k8s directory. After that we check for the cluster by the name we created earlier. If the cluster is present, we then pick the cluster config file from the S3 bucket and set it in the working context and then run the command which uses the configurations in the yaml file to setup the pods and service for our application. The `pods` are created using the Docker application image created in pushed a few steps ago in the pipeline.

To access the app, you need be able to access the created resources. For that we install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/).

- To install kubectl run `brew install kubectl`
- Once it has been installed, run `kubectl get pods`. You should be able to see the created pods, depending on how many you set in the deployment configuration to be created. The **status** should be `running`.
- We then run `kubectl get svc -o wide`. This command will output the services you have running. Find the service that has the service name you set in your service configurations. It should have loadbalancer DNS link as part of it's results. When you click on it, it should redirect you to the app.

<img width="1680" alt="screen shot 2018-08-29 at 17 17 39" src="https://user-images.githubusercontent.com/5388763/44795518-901b3d00-abb3-11e8-8e53-fe2f9822d3e2.png">

The loadbalancer DNS link can be mapped to a subdomain if you have a domain setup. I have mapped mine to http://api.thegaijin.xyz. Should you find this link down, I have probably torn down the infrastructure.
