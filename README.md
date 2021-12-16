# Building a metrics dashboard
In this project, I created the dashboards that use multiple graphs to monitor our sample application that is deployed on a Kubernetes cluster. I used Prometheus, Jaeger, and Grafana in order to monitor, trace and visualize my experience.

## Main Steps :
1. Deploy the sample application in your Kubernetes cluster.
2. Use Prometheus to monitor the various metrics of the application.
3. Use Jaeger to perform traces on the application.
4. Use Grafana in order to visualize these metrics in a series of graphs that can be shared with other members on your team.
5. Document your project in a README.

![image](https://user-images.githubusercontent.com/61888364/142960531-48afd6c8-4603-49fc-ab14-8b0f23398929.png)

## Steps of Installation : 
```
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh

kubectl create namespace monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add stable https://charts.helm.sh/stable
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --kubeconfig /etc/rancher/k3s/k3s.yaml

kubectl create namespace observability
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/crds/jaegertracing.io_jaegers_crd.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/service_account.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/role.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/role_binding.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/operator.yaml
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/cluster_role.yaml
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/master/deploy/cluster_role_binding.yaml

helm repo add bitnami https://charts.bitnami.com/bitnami
helm install mongodb --set auth.rootPassword=password,auth.username=srishti,auth.password=password7,auth.database=example-mongodb bitnami/mongodb --kubeconfig /etc/rancher/k3s/k3s.yaml
```

**Note:** All the screenshots are stored in the `answer-img` directory.

## Verify the monitoring installation
Run `kubectl` command to show the running pods and services for all components. Below are the screenshots of the output to verify the installation.
- Services under namespace monitoring
![image](https://user-images.githubusercontent.com/61888364/143324110-fd7bcafe-370e-41ac-a0c3-4abdd231fc8f.png)
- Services under the namespace observability
![image](https://user-images.githubusercontent.com/61888364/143324354-d4dc35d3-a879-41f8-968b-b3802e53f8d9.png)
- Pods under namespace monitoring
![image](https://user-images.githubusercontent.com/61888364/143324989-41a8a4ef-7592-49ab-93d2-1f662a1461f7.png)
- Pods under namespace observability
![image](https://user-images.githubusercontent.com/61888364/143325151-450430b7-bf52-47b6-94c3-4a631dacfc15.png)
- All the pods in the kubernetes cluster
![image](https://user-images.githubusercontent.com/61888364/143325856-bf6ab339-0463-406a-a626-8f84bed47510.png)

## Setup the Jaeger and Prometheus source
Expose Grafana to the internet and then setup Prometheus as a data source. Below is a screenshot of the home page after logging into Grafana.
![image](https://user-images.githubusercontent.com/61888364/143328289-22278a2d-94ba-4a78-880b-ccf612d6b3e9.png)

![grafana](https://user-images.githubusercontent.com/61888364/143326363-6f38cc4e-c78a-4d3c-bb13-acb2d84f9337.PNG)

## Create a Basic Dashboard
Create a dashboard in Grafana that shows Prometheus as a source. Below is the screenshot of the same.
![image](https://user-images.githubusercontent.com/61888364/143326528-286248e8-4502-491f-aa03-a7fa7ea5b837.png)
![image](https://user-images.githubusercontent.com/61888364/143327032-bf25ba97-42d5-4804-a539-3c742d639dfc.png)

## Describe SLO/SLI
We will describe, in our own words, what the SLIs are, based on an SLO of *monthly uptime* and *request response time* :
- Service Level Indicators are the metrics that let us know if we achieved our SLOs(Service Level Objectives) or not.
- Service Level Indicators with respect to a SLO of monthly uptime would keep the track of the availability of the application via http code over a period of a month.
- Service Level Indicators with respect to a SLO of request response time would measure the requests latency.

## Creating SLI metrics.
It is important to know why we want to measure certain metrics for our customer. Describe in detail 5 metrics to measure these SLIs?
- First SLO would be **Latency**. This demonstrates the time taken to respond to a request.
- Second SLO would be **Uptime**. This demonstrates the percentage of time the websites are available and functioning.
- Third SLO would be **Failure Rate**. This demonstrates the amount of failures in unit of time.
- Fourth SLO would be **Network Capacity**. This demonstrates the average bandwidth in unit time.
- Fifth SLO would be **Resource Capacity**. This demonstrates the RAM and CPU usage amount.

## Create a Dashboard to measure our SLIs
Create a dashboard to measure the uptime of the frontend and backend services We will also want to measure to measure 40x and 50x errors. Create a dashboard that show these values over a 24 hour period and take a screenshot.
![1](https://user-images.githubusercontent.com/61888364/143501472-332f2270-bae8-4dfa-9ccc-b0749e4c0251.png)

## Tracing our Flask App
We will create a Jaeger span to measure the processes on the backend. After filling in the span, I have provided a screenshot of it here. Also I provided a (screenshot) sample Python file containing a trace and span code used to perform Jaeger traces on the backend service.
![flask app](https://user-images.githubusercontent.com/61888364/143328627-fdb6a52e-fe00-479c-9ce0-ab7ae563d7e5.png)

## Jaeger in Dashboards
Now that the trace is running, let's add the metric to our current Grafana dashboard. I have provided a screenshot of it here.
![image](https://user-images.githubusercontent.com/61888364/143328806-bf21ea2f-fb0b-47f8-a8fa-dc220fab0235.png)

## Report Error
Using the template below, we wrote a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue. A screenshot of the tracer span is included to demonstrate how we can use a tracer to locate errors easily.

TROUBLE TICKET

Name: [Error on reference-app/frontend/app.py](https://github.com/sg7801/Building-a-metrics-dashboard/blob/main/reference-app/frontend/app.py)

Date: 25/11/21 18:35:10

Subject: Cannot get any access to the url

Affected Area: [reference-app/frontend/app.py](https://github.com/sg7801/Building-a-metrics-dashboard/blob/main/reference-app/frontend/app.py)

Severity: High

Description: When I hit the frontend with the url path '/' with post request, it produces the error.


## Creating SLIs and SLOs
We want to create an SLO guaranteeing that our application has a 99.95% uptime per month. Name four SLIs that you would use to measure the success of this SLO.
- HTTP Error Rate. More than 95% of all requests must execute without any errors.
- Uptime. There must be atleast 99% uptime per month.
- Latency. The response time of the 90% requests should be less than 30ms per month.
- Resource capcity: The usage of CPU and RAM must not exceed 90% per month.

## Building KPIs for our plan
Now that we have our SLIs and SLOs, we create a list of 2-3 KPIs to accurately measure these metrics as well as a description of why those KPIs were chosen. We will make a dashboard for this, but first lets write them down here.
- Error Rate : This KPI was chosen because more than 95% of all requests must execute without any errors. Hence it will allow us to monitor the rate of error of our application.
- Uptime :  This KPI was chosen since there must be atleast 99% uptime per month. Uptime KPI allows us to accurately measure these metrics.
- Resource capcity: This KPI was chosen because the usage of CPU and RAM must not exceed 90% per month. Resource Capacity KPI allows us to monitor their consumption.

## Final Dashboard
Lets create a Dashboard containing graphs that capture all the metrics of the KPIs and adequately representing your SLIs and SLOs. We include a screenshot of the dashboard here, and write a text description of what graphs are represented in the dashboard.  

![DASH1](https://user-images.githubusercontent.com/61888364/143375159-4bac6972-7e91-4a5e-9008-fcc947c7760b.png)
![DASH2](https://user-images.githubusercontent.com/61888364/143375165-ec79c350-f646-4563-acb9-44944ba036c5.png)

- Average Response Time : It represents the **average response time measured per unit time**
- Error Responses : It represents the **number of failed requests per month**
- Successful Responses : It represents **total successful request per month**
- Memory Usage : It represents the **memory usage of the Flask App**
- Disk Usage : It represents the **consumtion of the disk drive**
- CPU Usage : It represents the **CPU usage of the Flask App**
- Deployment Uptime : It represents the **uptime of each back-end and front-end service**
- Server Uptime : It represents the **Uptime of each instance**
