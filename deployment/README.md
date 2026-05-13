# Deployment Guide: FindBack Project
**Date:** 2026-05-13

This guide outlines the sequential procedure for provisioning the cloud environment and implementing the CI/CD pipeline for the FindBack application.

---

## 1. Resource Group Provisioning
The first step is to establish a logical container for all Azure resources to ensure organized management and billing.

1. Navigate to the **Resource Groups** blade in the Azure Portal.
2. Click **Create** and specify the name `findback-deployment-finals`.
3. Select the region (e.g., East Asia) and review + create.

![Resource Group Provisioning](/deployment/screenshots/Resource-Group.png)

---

## 2. Infrastructure Setup (Virtual Machine)
With the group created, we provision the host hardware.

1. **Create Virtual Machine:** Initiate the VM creation process, ensuring it is assigned to the `findback-deployment-finals` group.
   
![Creating VM Process](/deployment/screenshots/Creating-VM.png)

2. **Configure FindBackVM:** * **OS:** Ubuntu Server 22.04 LTS.
   * **Size:** Standard B1s (Burstable).
   * **Authentication:** SSH Public Key.

![FindBackVM Configuration](/deployment/screenshots/FindBackVM.png)

3. **Networking (Inbound Rules):**
   * Configure the Network Security Group to allow traffic on **Port 22** (SSH), **Port 80** (HTTP), and **Port 443** (HTTPS).

---

## 3. Server Preparation
Access the VM via SSH to install the necessary containerization engine.

```bash
# Update system packages
sudo apt-get update

# Install Docker and Docker Compose
sudo apt-get install docker.io docker-compose -y

# Enable Docker service
sudo systemctl start docker
sudo systemctl enable docker