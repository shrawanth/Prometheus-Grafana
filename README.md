# 🛠️  Installation & Configurations
## 📦 Step 1: Create EKS Cluster

### Prerequisites
- Download and Install AWS Cli - Please Refer [this]("https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html") link.
- Setup and configure AWS CLI using the `aws configure` command.
- Install and configure eksctl using the steps mentioned [here]("https://eksctl.io/installation/").
- Install and configure kubectl as mentioned [here]("https://kubernetes.io/docs/tasks/tools/").


```bash
eksctl create cluster --name=observability \
                      --region=us-east-1 \
                      --zones=us-east-1a,us-east-1b \
                      --without-nodegroup
```
```bash
eksctl utils associate-iam-oidc-provider \
    --region us-east-1 \
    --cluster observability \
    --approve
```
```bash
eksctl create nodegroup --cluster=observability \
                        --region=us-east-1 \
                        --name=observability-ng-private \
                        --node-type=t3.medium \
                        --nodes-min=2 \
                        --nodes-max=3 \
                        --node-volume-size=20 \
                        --managed \
                        --asg-access \
                        --external-dns-access \
                        --full-ecr-access \
                        --appmesh-access \
                        --alb-ingress-access \
                        --node-private-networking

# Update ./kube/config file
aws eks update-kubeconfig --name observability
```

### 🧰 Step 2: Install kube-prometheus-stack
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

### 🚀 Step 3: Deploy the chart into a new namespace "monitoring"
```bash
kubectl create ns monitoring
```
```bash
helm install monitoring prometheus-community/kube-prometheus-stack \
-n monitoring \
-f ./custom_kube_prometheus_stack.yml
```

### ✅ Step 4: Verify the Installation
```bash
kubectl get all -n monitoring
```
- **Prometheus UI**:
```bash
kubectl port-forward service/prometheus-operated -n monitoring 9090:9090 --address 0.0.0.0
```

- **Grafana UI**: password is `prom-operator`
```bash
kubectl port-forward service/monitoring-grafana -n monitoring 8080:80
```
- **Alertmanager UI**:
```bash
kubectl port-forward service/alertmanager-operated -n monitoring 9093:9093
```
## 🐳 Step 5. Build & Push Docker Image
From the app/ directory:
```bash
docker build -t your-dockerhub-username/prometheus-demo:latest .
docker push your-dockerhub-username/prometheus-demo:latest
```
## 🚀 Step 6. Deploy the App to Kubernetes
```bash
kubectl apply -f kubernetes-manifest/monitoring-namespace.yaml
kubectl apply -f kubernetes-manifest/prometheus-app-deployment.yaml
kubectl apply -f kubernetes-manifest/prometheus-app-service.yaml
```
## Step 7. 🔎 8. Verify Prometheus Target Discovery
1. Open http://localhost:9090/targets
2. You should see prometheus-demo-app under discovered targets
3. Go to http://localhost:9090/graph and search:
```bash
app_requests_total
```
## Step 8. 📊 9. Visualize in Grafana
1. Open http://localhost:8080
- Username: admin
- Password: prom-operator (default)
2. Go to:
- Dashboards → New → Add Panel
- Query:
```bash
rate(app_requests_total[1m])
```
- Add visualization (e.g., graph)
## ✅ Summary
You now have:
- A sample app running in K8s, exposing Prometheus metrics
- Prometheus scraping the app
- Grafana showing the metrics graph
