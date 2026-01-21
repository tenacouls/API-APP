# Welcome to CITY-API
REST API application developed with [Flask](https://flask.palletsprojects.com/en/stable/) framework. Working with built-in database sqlite.

## Docker Image
Image used in this project: [/tenacouls/api-app](https://hub.docker.com/repository/docker/tenacouls/api-app/general)

Dockerfile provided in [Dockerfiles](./Dockerfiles/) directory

## Helm Chart

Helm chart present in [api-app](./api-app/) directory.

## Prerequisites
To run this application smoothly you need to:

1. Docker Installed: [Get Started with Docker](https://www.docker.com/get-started/)
2. Kubernetes cluster with kubectl (*Minikube*, *K8S*): [How to create Minikube cluster](https://minikube.sigs.k8s.io/docs/start/?arch=%2Fwindows%2Fx86-64%2Fstable%2F.exe+download)
3. Helm: [Install Helm](https://helm.sh/docs/intro/install/)

## Deploy application

To deploy application you can follow this steps:

1. Clone repo
 
    ```Bash
    git clone https://github.com/tenacouls/API-APP/tree/main
    ```
2. Start minikube cluster

    ```Bash
    minikube start
    ```
3. Create namespace for application and services

    ```dotnetcli
    kubectl create ns api-app
    ```
4. Run helm install command
    
    ```Sh
    helm install api-app /path/to/chart-directory --namespace api-app
    ```
    All nessecary values already provided in ```values.yaml```. But if you interested to configure app by your own feel free to do it.

5. Check status of the pod

    ```bash
    kubectl get po -n api-app
    ```
    The output will be something like this:

    ```dotnetcli
    kubectl get po -n api-app

    NAME                      READY   STATUS    RESTARTS   AGE
    api-app-89b8ff96b-h82ns   1/1     Running   0          2m49s
    ```
5. Setup port-forwarding
    ```
    kubectl port-forward service/api-app 5000:5000
    ```
    
After that, you can access the api at the URL: http://localhost:5000 -n api-app

## How to work with API

To make a request to the app, you need Curl, Postman e.g.

### Endpoints:

- ```/health``` - send info about service health. Methods - ```GET```
- ```/cities``` - endpoint for working with database. Methods - ```GET```, ```POST```, ```DELETE```, ```PUT```
- ```/health``` - Application status. Methods - ```GET```
- ```/name/city_name``` - after ```/name``` endpoint you can enter name of city to get information. Methods - ```GET``` (city_name is Key Sensetive)

## Get object
There is two ways to get object from Data Base.

1. Using ```GET``` method to ```/cities``` endpoint. After that you recive all objects from Data Base
1. Using ```GET``` method to ```/cities/name/city_name``` endpoint where ```/city_name``` is name of chosen city (```/city_name``` is key sensetive)

### Example

To get all cities in Data Base:
```
curl -X GET "http://localhost:5000/cities"
```
To get specific city:
```
curl -X GET "http://localhost:5000/cities/name/Abu-Dhabi"
```

## Add object
To add obect in DataBase you simply send request with JSON file to ```/cities``` endpoint.

### Example:
```curl -X POST "http://localhost:5000/cities" --json json.txt```

```JSON
    {
        "city": "Paris",
        "country": "FR",
        "population": 2040000
    }
```
## Update object
The process of updating objects is performed using the object ID. To update object you need to send ```PUT``` request to endpoint ```/cities/city_id``` with new values in JSON format.

### Example

```curl -X PUT "http://localhost:5000/cities/1" --json json.txt```

```JSON
    {
        "population": 123456789
    }
```


## Delete object

To delete object you need to know object id. After you recived object id you can send DELETE request to ```/cities/object_id``` endpoint where ```object_id``` is id of chosen object.
### Example:

```curl -X DELETE "http://localhost:5000/cities/1"```

## Challenges 
1. API development with a large number of endpoints on Flask.
2. Problems with configuring the Ingress controller. I had to use a simpler solution with port-forward - the solution is not suitable for production environments.
 
## Suggestions 
1. Setup NFS storage for Data Base data, and configure backup for this NFS node.
2. Setup pipeline to deploy application automaticly (in case without ArgoCD, Flux etc.)
3. Setup IngressNginx controller and certs for this controller to work with HTTPS.
4. Write error handlers for the endpoints.
5. Create separeted database for api-app service.
6. Configure authorization in the API using a key.
7. Setup security context for pods and containers to avoid security vulnerabilities.
8. Create PVC and mount it to Data Base Container to store information safely.
9. Setup RBAC acces to different API endpoints.
10. Add feature to send a few JSON obects to DB on ```/cities``` endpoint