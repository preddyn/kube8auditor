#  Kubernetes Audit script 

Audit script can audit for validating AdmissionControllers, CustomAPI &  Pod Security Policies

## Prerequisites 

- Verify Python >= 3.7 is installed.  Check the installed version using:
```
python -V
```
    or
```
python3 -V
```
- Create a working directory and make it the current directory.  Note: the path shown is for illustration only.
```
mkdir /path/to/working_directory
cd /path/to/working_dir
```

```
- Import module dependencies using:
```
pip install -r ./requirements.txt
```
    or
```
pip3 install -r ./requirements.txt
```
- Install Kubectl with Homebrew on macOS
```
    brew install kubectl
```
- Test your installation of kubectl
```
    kubectl version --client
```
- Login into your kubernetes cluster to gain Kubectl access, below example provides access to AKS cluster(azure):
```
az login 
az account set --subscription "Provide_your_subscription_name/ID"
az aks get credentials --resource-group "Provide_your_RG" --name "cluster_name"
kubectl get pods -A
```
## Execute the Audit Script
```
python3 KubeAudit.py
``` 
- After executing the script, 'KubeAudit.py' will ask for Cluster CA cert file path "Provide you k8s cert file path:". Please provide, as shown in example below 
```
    Provide you k8s cert file path :/Users/XXXXX/projects/k8s/certs/webhook.crt
```
### Note: Currently SSL Verification is set to false in line 15 of KubeAudit.py. Reason Client supports from within the cluster environment.
### Output Results
- Output of AdmissionController information is saved in current directory as 'k8sWebhook.txt' file
- Output of Custome API results is saved in current directory as 'CustomAPI.txt' file
- Output of PodSecurityPolicy information is saved in current directory as 'PSP.txt' file

## [Reference](https://github.com/kubernetes-client/python)

