# FindBack — Cloud-Native Campus Lost & Found System
**CSEC 3 – Cloud Computing (Microsoft Azure) | Final Project**

## Project Overview
**FindBack** is a professional redesign of a traditional campus lost and found application, migrated into a cloud-native architecture on **Microsoft Azure**. The project demonstrates the transition from a local development environment to a containerized, production-ready system. Utilizing **Flask**, **MongoDB**, and **Docker**, FindBack provides a secure platform for students and faculty to report, track, and claim lost items while maintaining high operational standards through automated CI/CD and cost-efficient cloud resource management.

## Table of Contents
1. [Final Project Deliverables](#final-project-deliverables)
2. [Cloud Architecture and Optimizations](#cloud-architecture-and-optimizations)
3. [Repository Structure](#repository-structure)
4. [Technical Stack](#technical-stack)
5. [Project Team](#project-team)
6. [Testing Credentials](#testing-credentials)

---

## Final Project Deliverables

### Deliverable 1: Architecture Diagram
The FindBack architecture utilizes an IaaS (Infrastructure as a Service) approach to maintain full control over the container environment.
* **Region:** East Asia (Hong Kong)

> [Check the full discussion for the diagram here](./diagram/diagram.md)

### Deliverable 2: Deployment Documentation
Comprehensive setup guides and automated pipeline configurations are located in the [deployment/](./deployment/) directory.

#### Quick Start Deployment Guide
**Prerequisites**
* Docker and Docker Compose installed.
* Azure CLI for infrastructure management.
* GitHub Repository Secrets configured for CI/CD.

**Deployment Execution**
1. **Cloud Environment Setup**
   Access the VM via SSH and prepare the engine:
   ```bash
   sudo apt-get update
   sudo apt-get install docker.io docker-compose -y
   ```
2. **CI/CD Automation**
   The project uses **GitHub Actions** to automatically build and push images to the container registry upon every push to the main branch.

For full instructions, see the [Detailed Deployment Guide](./deployment/README.md).

### Deliverable 3: Cost Estimate Report
The following itemized monthly cost estimate is based on the **East Asia (Hong Kong)** region.

| Azure Service | Configuration Details | Estimated Monthly Cost |
| :--- | :--- | :--- |
| **Virtual Machine** | B1s (1 Core, 1 GB RAM) x 730 Hours | $10.66 |
| **Managed Disk** | 32 GiB Standard SSD (E4), LRS | $2.60 |
| **Public IP** | Standard (ARM), 1 Static IP Address | $3.65 |
| **Azure Monitor** | Log Analytics: Log Data Ingestion (Free Tier) | $0.00 |
| **Bandwidth** | 5 GB Inter-Region Transfer (Free Tier) | $0.00 |
| **Total Estimated Cost** | | **$16.91 / Month** |

For the complete analysis and optimization strategies, view the [Full Cost Estimate Report](./report/cost-estimate.md).

### Deliverable 4: Live Demo
* **Live Application URL:** `http://20.239.17.38:5000`
* **Youtube Video Link:** `Place Holder`

---

## Cloud Architecture and Optimizations
FindBack prioritizes transparency, resource efficiency, and disaster resilience.

### Azure Service Stack
| Service | Function |
| :--- | :--- |
| **Virtual Machines (B1s)** | Host for Dockerized Flask and MongoDB containers. |
| **Managed Disks (LRS)** | Persistent storage for the MongoDB database, decoupled from compute. |
| **Standard Static IP** | Provides a consistent endpoint for the application address. |
| **GitHub Actions** | CI/CD pipeline for automated builds and deployment. |
| **Azure Monitor** | Performance monitoring and operational telemetry. |

### Implemented Cloud Optimizations
* **Container Orchestration (Docker Compose):** Simplifies deployment by managing both the web and database layers as a single unit, ensuring environment parity between local and production stages.
* **Storage Decoupling:** By using **Azure Managed Disks**, the MongoDB data persists independently of the VM instance lifecycle, protecting against data loss during hardware failures.
* **Resource Recovery Protocols:** Implemented manual recovery procedures via **Azure Cloud Shell** to manage memory exhaustion (RAM) on burstable instances, ensuring 24/7 availability.
* **Automated CI/CD:** Integrated **GitHub Container Registry** to move build-heavy processes away from the B1s VM, saving critical system memory for application performance.

---

## Repository Structure

```text
finders-keepers/
├── .github/workflows/   # CI/CD Pipeline Definitions
├── app/                 # Frontend (Templates & Static)
├── deployment/          # Deployment Guide & Setup Screenshots
│   └── screenshots/     # Infrastructure provisioning visuals
├── diagram/             # Architectural Diagram
│   └── screenshots/  
├── report/              # Cost Estimation & Optimization Reports
│   └── screenshots/     # Azure Calculator exports
├── app.py               # Main Flask Entry Point
├── Dockerfile           # Image build instructions
├── docker-compose.yml   # Multi-container orchestration
├── Changelog.md         # Documented development history
└── requirements.txt     # Python Dependencies
```

---

## Technical Stack
* **Backend:** Flask (Python)
* **Database:** MongoDB (NoSQL)
* **Containerization:** Docker & Docker Compose
* **Cloud:** Microsoft Azure
* **CI/CD:** GitHub Actions

---

## Project Team
| Member Name | Role |
| :--- | :--- |
| **Palacios** | Lead Programmer & Technical Architect |
| **Morandarte** | UI/UX Developer | 

---

## Testing Credentials
| Account Role | Username | Password |
| :--- | :--- | :--- |
| **Admini Account** | `keepers` | `LaFkeep3r123` |

