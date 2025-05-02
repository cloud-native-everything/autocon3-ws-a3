# **Lab 1 Guide: Dynamic Traffic Generation**

The first Hands-on Lab is about Deploying a containerized **iPerf** app within **Kind** to generate and test traffic scenarios. This solution will leverage **custom reconcilers** for dynamic configuration. By combining **Containerlab** and **Kind**, the lab enhances network simulation and automation, creating a more realistic and flexible test environment.

| Item | Details |
| --- | --- |
| Short Description | Dynamic Traffic Generation with IPerf with Containerlab and Kind |
| Skill Level | Intermediate |
| Tools Used | Containerlab, Kind, Github Codespaces, Visual Studio Code, iPerf |

## Summary and Objective
The first Hands-on Lab is about Deploying a containerized **iPerf** app within **Kind** to generate and test traffic scenarios. This solution will leverage **custom reconcilers** for dynamic configuration. By combining **Containerlab** and **Kind**, the lab enhances network simulation and automation, creating a more realistic and flexible test environment.

## **Step 1: Infrastructure Setup**

The first part is to setup the Infrastructure for the deployment of the cluster afterwards.

Navigate to the workspace folder for the section of lab1.

```shell
# change into Part 1 directory
cd /workspaces/autocon3-ws-a3/lab1
```

---

### Build the IPerf Docker images

The next step is to build the iPerf Docker images for both the client and server. These images include all the necessary network tools for deploying their respective containers and automatically configure the required environment variables.

```shell
docker build -t iperf3-client:0.1a -f iperf-images/Dockerfile.iperf3client .
docker build -t iperf3-server:0.1a -f iperf-images/Dockerfile.iperf3server .
```

---

### Load pre-cached Container Images
The container images for the NOS, in this case, SRLinux, have already been pre-cached and just need to be loaded in the next step.

```shell
# import the locally cached sr-linux container image
docker image load -i /var/cache/srlinux.tar
```

The Kind container image has also been pre-cached locally and only needs to be loaded.

```shell
# import the locally cached kind container image
docker image load -i /var/cache/kindest-node.tar
```

---

### Setting up the Container Networking
To prevent issues with running Kind in Codespaces, we need to pre-create the Kind Docker bridge. This ensures that the containers can communicate properly.

```shell
# pre-creating the kind docker bridge. This is to avoid an issue with kind running in codespaces. 
docker network create -d=bridge \
    -o com.docker.network.bridge.enable_ip_masquerade=true \
    -o com.docker.network.driver.mtu=1500 \
    --subnet fc00:f853:ccd:e793::/64 kind
```
Additionally, we need to add iptable rules to enable communication between the Kubernetes cluster and the later-created ContainerLab topology.

```shell
# Allow the kind cluster to communicate with the later created containerlab topology
sudo iptables -I DOCKER-USER -o br-$(docker network inspect -f '{{ printf "%.12s" .ID }}' kind) -j ACCEPT
```


## **Step 2:  Setup Kubernetes Kind App**
The second step focuses on setting up the Kubernetes clusters and configuring the router for communication.

1. **Start ContainerLab Topology** 
   - Creating the kubernetes clusters and router via containerlab:
      ```shell
      # deploy Nokia SRL containers via containerlab or use the vscode extension
      cd clab-topology
      sudo containerlab deploy
      cd ..
      ```

2. **Kubernestes Contexts**
  - Verify that the cluster are running. You should be able to see both contexts, and '*' showing the current one.
    ```
    sudo kubectl config get-contexts
    CURRENT   NAME         CLUSTER      AUTHINFO     NAMESPACE
              kind-k8s01   kind-k8s01   kind-k8s01   
    *         kind-k8s02   kind-k8s02   kind-k8s02  
    ```

3. **Preload the iperf3 Docker Images to Kind Kubernetes**  
   - Load the previously build iperf3 image into both kubernetes clusters:
     ```bash
     kind load docker-image iperf3-client:0.1a --name k8s01
     kind load docker-image iperf3-server:0.1a --name k8s02
     ```


4. **Set Srlinux dev1 Basic Configuration**
  - Connect to dev1 and configure a basic configuration
    ```shell
    docker exec -ti dev1 sr_cli
    ```
  - The terminal should show the following output:
    ```
      ❯ docker exec -ti dev1 sr_cli
      Using configuration file(s): []
      Welcome to the srlinux CLI.
      Type 'help' (and press <ENTER>) if you need any help using this.
      --{ + running }--[  ]--
      A:dev1#
    ```

  - Now, paste the following configuration for the router:
    ```
    enter candidate
        network-instance default {
          interface ethernet-1/10.0 {
          }
          interface ethernet-1/11.0 {
          }
      }
      interface ethernet-1/10 {
          admin-state enable
          subinterface 0 {
              admin-state enable
              ipv4 {
                  admin-state enable
                  address 172.254.101.1/24 {
                  }
              }
          }
      }
      interface ethernet-1/11 {
          admin-state enable
          subinterface 0 {
              admin-state enable
              ipv4 {
                  admin-state enable
                  address 172.254.102.1/24 {
                  }
              }
          }
      }
    commit now
    quit      
    ```
  - dev1 should now be configured and ready to communicate between the iperf instances

---

## **Step 3: Transition to CRDs and Controller**
This section introduces a Custom Resource Definition (CRD) for managing iperf3 traffic generator clients in Kubernetes. By defining IperfClient resources, we can declaratively configure client pods to connect to specific server IPs and ports. A custom controller ensures that pods are created or updates (or even deleted, that is out of the scope of this test) based on the CRD's state, enabling seamless scaling and dynamic updates. The client pods continuously run iperf3 commands in a loop, providing automated and reliable traffic generation for performance testing. This approach simplifies deployment, enhances flexibility, and leverages Kubernetes-native features for robust traffic management.

### **Creating a Custom Resource Definition**
1. Define a `TrafficGenerator` CRD for iperf-server and iperf-client.
    ```shell
    sudo kubectl apply -f ./CRDs/iperf-server-crd.yaml --context kind-k8s02
    sudo kubectl apply -f ./CRDs/iperf-client-crd.yaml --context kind-k8s01
    ```

2. Check iperf-server CRD setup:
    ```shell
    sudo kubectl get CustomResourceDefinition  --context kind-k8s02
    NAME                       CREATED AT
    iperfservers.example.com   2025-01-07T21:52:04Z
    sudo kubectl get CustomResourceDefinition  --context kind-k8s01
    NAME                       CREATED AT
    iperfclients.example.com   2025-01-07T21:52:04Z    
    ```
3. Add python code for reconciler in ConfigMap and start the controller using it:
    ```shell
    sudo kubectl apply -f ./CRDs/iperf-server-configmap.yaml --context kind-k8s02
    sudo kubectl apply -f ./CRDs/iperf-server-controller.yaml --context kind-k8s02
    sudo kubectl apply -f ./CRDs/iperf-client-configmap.yaml --context kind-k8s01
    sudo kubectl apply -f ./CRDs/iperf-client-controller.yaml --context kind-k8s01    
    ```
4. Check if the controller is running via `sudo kubectl get pods --context kind-k8s02` in the server side:     
    ```bash
    NAME                      READY   STATUS             RESTARTS         AGE
    iperf-server-controller   1/1     Running            0                2m36s
    ```
    Now, in the client side `sudo kubectl get pods --context kind-k8s01`:
    ```bash
    NAME                      READY   STATUS             RESTARTS         AGE
    iperf-client-controller   1/1     Running            0                2m36s
    ```    

5. If both are running, then now you can add the server CRDs values. Open `./CRDs/iperf-server-setup.yaml` and inspect the values used, and execute it:
    ```shell
    sudo kubectl apply -f ./CRDs/iperf-server-setup.yaml --context kind-k8s02
    ```
6. You should see 10 instances running after a few minutes. 
    ```shell
    sudo kubectl get pods --context kind-k8s02
    ```
    You should see something like this:
    ```shell
    NAME                               READY   STATUS    RESTARTS   AGE
    iperf-server-controller            1/1     Running   0          4m17s
    iperf3-server-0-cdfcf7f6b-98ccm    1/1     Running   0          10s
    iperf3-server-1-66597c5d6f-lph4j   1/1     Running   0          10s
    iperf3-server-2-78469bdcbd-7rzkl   1/1     Running   0          10s
    iperf3-server-3-58779bc979-c2knl   1/1     Running   0          10s
    iperf3-server-4-656545d446-6m54g   1/1     Running   0          10s
    iperf3-server-5-5cd44f9cf7-87kwx   1/1     Running   0          10s
    iperf3-server-6-6b5fd6cc9b-rbqmc   1/1     Running   0          10s
    iperf3-server-7-5594487d47-p7pk9   1/1     Running   0          9s
    iperf3-server-8-76b5fb8794-p9x77   1/1     Running   0          9s
    iperf3-server-9-5b469c667c-xwhd7   1/1     Running   0          9s
    ```

8. Now, let;s do the same with the client. Open `./CRDs/iperf-client-setup.yaml` and inspect the values used, and execute them:
    ```shell
    sudo kubectl apply -f ./CRDs/iperf-client-setup.yaml --context kind-k8s01
    ```

9.  Inspect the instances `sudo kubectl get pods --context kind-k8s01`. You should see something like:
    ```shell
    NAME                      READY   STATUS    RESTARTS   AGE
    iperf-client-controller   1/1     Running   0          100m
    iperf3-client-30001       1/1     Running   0          99m
    iperf3-client-30002       1/1     Running   0          99m
    iperf3-client-30003       1/1     Running   0          99m
    iperf3-client-30004       1/1     Running   0          99m
    iperf3-client-30005       1/1     Running   0          87m
    ```
10. Now you can modify `endPort: 30005` to `endPort: 30010` in `./CRDs/iperf-client-setup.yaml` and reapply it via `sudo kubectl apply -f ./CRDs/iperf-client-setup.yaml --context kind-k8s01` you should see a change in the amount of instances with `sudo kubectl get pods --context kind-k8s01`:

    ```shell
    NAME                      READY   STATUS    RESTARTS   AGE
    iperf-client-controller   1/1     Running   0          100m
    iperf3-client-30001       1/1     Running   0          99m
    iperf3-client-30002       1/1     Running   0          99m
    iperf3-client-30003       1/1     Running   0          99m
    iperf3-client-30004       1/1     Running   0          99m
    iperf3-client-30005       1/1     Running   0          87m
    iperf3-client-30006       1/1     Running   0          87m
    iperf3-client-30007       1/1     Running   0          87m
    iperf3-client-30008       1/1     Running   0          87m
    iperf3-client-30009       1/1     Running   0          87m
    iperf3-client-30010       1/1     Running   0          87m
    ```

    **Note:** the code is limited then additional testing, like deleting instances, would require changes in the controller code.

11. Inspect the activity in the instances via  `sudo kubectl logs iperf3-client-30001 --context kind-k8s01` and/or check the traffic stats flowing thru the switch.

12. Cleaning up everything

    ```shell
    sudo kubectl delete -f ./CRDs/iperf-client-setup.yaml --context kind-k8s01
    sudo kubectl delete -f ./CRDs/iperf-server-setup.yaml --context kind-k8s02
    sudo kubectl delete -f ./CRDs/iperf-server-controller.yaml --context kind-k8s02
    sudo kubectl delete -f ./CRDs/iperf-server-configmap.yaml --context kind-k8s02
    sudo kubectl delete -f ./CRDs/iperf-client-controller.yaml --context kind-k8s01 
    sudo kubectl delete -f ./CRDs/iperf-client-configmap.yaml --context kind-k8s01
    sudo kubectl delete -f ./CRDs/iperf-server-crd.yaml --context kind-k8s02
    sudo kubectl delete -f ./CRDs/iperf-client-crd.yaml --context kind-k8s01    
    ```
---

## **Summary**
 
- **Objective**: CRD with a custom controller for full declarative automation.  
- **Outcome**: Simplified management, scalability, and better monitoring using Kubernetes-native tools.