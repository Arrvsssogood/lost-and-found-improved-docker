# Deployment Guide: FindBack Project
**Date:** 2026-05-13

This guide provides a professional, step-by-step procedure for deploying the FindBack application to an Azure Virtual Machine environment using Docker and CI/CD pipelines.

---

## 1. Cloud Infrastructure Setup
Before deploying the code, the host environment must be provisioned.

1.  **Create Resource Group:**
    * Create a Resource Group named `findback-deployment-finals` to contain all project assets.
2.  **Provision Virtual Machine:**
    * **OS:** Ubuntu Server 20.04 or 22.04 LTS.
    * **Size:** Standard B1s (1 vCPU, 1 GiB memory) — *Note: This is a burstable instance suited for small-scale student projects.*
3.  **Network Security Group (NSG) Configuration:**
    * Navigate to **Networking** in the Azure Portal.
    * Add Inbound Port Rules for:
        * **Port 22:** SSH access for management.
        * **Port 80:** Standard HTTP web traffic.
        * **Port 443:** Secure HTTPS traffic.

---

## 2. Server Environment Preparation
Once the VM is running, access the terminal via SSH and install the containerization engine.

```bash
# Update package list
sudo apt-get update

# Install Docker and Docker Compose
sudo apt-get install docker.io docker-compose -y

# Start and enable the Docker service
sudo systemctl start docker
sudo systemctl enable docker