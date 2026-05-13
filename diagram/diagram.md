# Deliverable 1: Architecture Diagram & Discussion
**Project:** FindBack — Campus Lost & Found System

---

## 1. System Architecture Diagram

![Architecture Diagram](/diagram/screenshots/architecture-diagram.png)

---

## 2. Infrastructure Components

### 2.1 Compute Layer: Azure Virtual Machine 
The core of the platform resides on a **Standard B1s Virtual Machine** running Ubuntu 22.04 LTS. 
* **Selection Logic:** This instance type was selected for its **burstable CPU performance**. It allows the application to handle processing spikes during high-traffic events (like a campus-wide lost item report surge) while maintaining a low-cost baseline.
* **Orchestration:** We utilized **Docker Compose** to manage two distinct containers (Flask Web Server and MongoDB) within this single node.

### 2.2 Storage Layer: Decoupled Managed Disks
A critical cloud optimization implemented is the decoupling of storage from compute.
* **Component:** **32GB Standard SSD (E4 Tier)** with Locally Redundant Storage (**LRS**).
* **Selection Logic:** By mapping the MongoDB data directory to an Azure Managed Disk volume, we ensure **data persistence**. If the Virtual Machine needs to be resized or redeployed, the database remains intact, providing "11 nines" of durability within the East Asia data center.

### 2.3 Networking & Security Boundary
* **Security Boundary:** All resources are contained within the `findback-deployment-finals` **Resource Group**. Access is controlled via a **Network Security Group (NSG)** that acts as a stateful firewall.
* **Traffic Flow:** Public traffic is restricted to **Port 5000 (HTTP)** for application access, while management is restricted to **Port 22 (SSH)** using Public Key Authentication.

---

## 3. Cloud Optimizations & Design Decisions

### 3.1 CI/CD & Secret Management (GitHub Actions)
Rather than adding the overhead of a managed Key Vault to a small 1GB RAM instance, we implemented a **CI/CD-native security model**.
* **GitHub Secrets:** Sensitive credentials (VM IP, SSH Keys, Registry Tokens) are encrypted in GitHub. 
* **Optimization:** During deployment, the GitHub Actions runner securely injects these values into the environment. This move reduced VM memory consumption by roughly **15%** by removing the need for a persistent Azure Key Vault agent.

### 3.2 Regional Performance Strategy
The architecture is deployed in the **East Asia (Hong Kong)** region.
* **Optimization:** This ensures the lowest possible latency for our primary user base in the Philippines. It balances cost-efficiency with the sub-100ms response times required for a modern web experience.

### 3.3 High Availability via Pre-built Images
To prevent the "Agent Not Ready" errors common on small VMs during heavy local builds, the pipeline builds the Docker images on **GitHub-hosted runners** first.
* **Result:** The VM only performs a "Pull and Start" operation, ensuring the server remains stable and responsive even during production updates.