from __future__ import print_function
from logging import setLogRecordFactory
from kubernetes import client, config, watch, utils
from kubernetes.client.configuration import Configuration
from kubernetes.client.rest import ApiException
from pprint import pprint
import json, os, sys

config.load_kube_config()
cwd = os.getcwd()
certdir = input('Provide your k8s cert file path :')
original_stdout = sys.stdout
configuration = client.Configuration().get_default_copy()
configuration.ssl_ca_cert = certdir
configuration.verify_ssl = False

k8_client = client.ApiClient(configuration=configuration)

os.chdir(cwd)
with open('kubeauditor/k8sWebhook.txt','w') as file:
    sys.stdout = file
    try:
        admission_list = client.AdmissionregistrationV1Api(k8_client)
        #list available webhooks 
        webhookdata = admission_list.list_validating_webhook_configuration()
        mutatingwebhook = admission_list.list_mutating_webhook_configuration()    
        i = 0 
        j = 0
        for data in webhookdata.items:
            print(i)
            print('ValidatingWebhook Name :\n', webhookdata.items[i].metadata.name, '\n')
            print('Webhook Matching Label :\n', webhookdata.items[i].metadata.labels, '\n')
            print('Webhook Annotations: \n', webhookdata.items[i].metadata.annotations, '\n')
            for webhooks in webhookdata.items[i].webhooks:
                print(j)
                print('NameSpace Matching Expressions :\n', webhookdata.items[i].webhooks[j].namespace_selector.match_expressions, '\n')
                print('Webhook AdmissionController Version :\n', webhookdata.items[i].webhooks[j].admission_review_versions, '\n')
                print('Policy Rules : \n', webhookdata.items[i].webhooks[j].rules, '\n')
                j= j+1
            i+1    
            break
        #print(type(webhookdata.items[0].webhooks[0].rules))
        
        #pprint(mutatingwebhook)
        i = 0 
        j = 0
        for data in mutatingwebhook.items:
            print(i)
            print('MutatingWebhook Name :\n', mutatingwebhook.items[i].metadata.name, '\n')
            print('MutatingWebhook Matching Label :\n', mutatingwebhook.items[i].metadata.labels, '\n')
            print('MutatingWebhook Annotations: \n', mutatingwebhook.items[i].metadata.annotations, '\n')
            for mwebhooks in mutatingwebhook.items[i].webhooks:
                print(j)
                print('MutatingWebhook NameSpace Matching Expressions :\n', mutatingwebhook.items[i].webhooks[j].namespace_selector, '\n')
                print('MutatingWebhook AdmissionController Version :\n', mutatingwebhook.items[i].webhooks[j].admission_review_versions, '\n')
                print('MutatingWebhook Policy Rules : \n', mutatingwebhook.items[i].webhooks[j].rules, '\n')
                j= j+1
            i+1    
            break   

    except ApiException as e:
        print("Exception when calling AdmissionregistrationV1Api->list_validaing/mutating_webhook_configuration: %s\n" % e)
    sys.stdout = original_stdout


with open('kubeauditor/CustomAPI.txt','w') as file:
    sys.stdout = file
    i = 0 
    j = 0
    try:
        api_extension = client.ApiextensionsV1Api(k8_client)
        customApi_list=api_extension.list_custom_resource_definition()
        for data in customApi_list.items:
            print(i)
            print('Custom API Resource name :\n', customApi_list.items[i].metadata.name, '\n')
            print('Custom API match selector labels :\n', customApi_list.items[i].metadata.labels, '\n')
            print('Custom API annotations :\n', customApi_list.items[i].metadata.annotations, '\n')
            print('Custom API CustomResourceDefinition :\n', customApi_list.items[i].spec.names, '\n')
            print('Custom API defined custom resource group :\n', customApi_list.items[i].spec.group, '\n')
            #print('\n', customApi_list.items[i].spec.versions, '\n')
            for versions in customApi_list.items[i].spec.versions:
                print(j)
                #print('\n', customApi_list.items[i].spec.versions[j].schema.open_apiv3_schema.properties)
                for key in customApi_list.items[i].spec.versions[j].schema.open_apiv3_schema.properties:
                    print(key, 'CustomResourceDefinitionVersion with a version for CRD\n', customApi_list.items[i].spec.versions[j].schema.open_apiv3_schema.properties[key], '\n')
                j=j+1
            i+1    
            break
        #pprint(len(customApi_list.items))
    except ApiException as e:
        print("Exception when calling ApiextensionsV1Api->list_custom_resource_definition: %s\n" % e)
    sys.stdout = original_stdout

with open('kubeauditor/PSP.txt','w') as file:
    sys.stdout = file
    i = 0 
    try:
        policy_list = client.PolicyV1beta1Api(k8_client)
        psp_list=policy_list.list_pod_security_policy()
        for policy in psp_list.items:
            print(i)
            print('PodSecurityPolicy Kind(REST resource this object represents) :\n', psp_list.items[i].kind, '\n')
            print('PodSecurityPolicy resource name :\n', psp_list.items[i].metadata.name, '\n')
            print('PodSecurityPolicy annotations :\n', psp_list.items[i].metadata.annotations, '\n')
            print('PodSecurityPolicy Metadata labels :\n', psp_list.items[i].metadata.labels, '\n')
            print('PodSecurityPolicy ManagedFields :\n', psp_list.items[i].metadata.managed_fields, '\n')
            print('PodSecurityPolicy specs :\n', psp_list.items[i].spec, '\n')
            i+1
        #pprint(psp_available)
    except ApiException as e:
        print("Exception when calling PolicyV1beta1Api->list_pod_security_policy: %s\n" % e)
    sys.stdout = original_stdout
