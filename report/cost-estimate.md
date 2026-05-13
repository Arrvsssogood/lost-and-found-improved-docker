# FindBack: Cloud Cost Estimation Report
**Date:** May 13, 2026

---

## 1. Architecture Summary
The **FindBack** platform is deployed on **Microsoft Azure** using a robust, containerized IaaS architecture designed for scalability and persistence. The design prioritizes cost-efficiency for a student-led startup while ensuring production-grade security and low-latency access for users in the Philippines.

* **Compute:** **Azure Virtual Machine (Linux)** running a **burstable B1s instance**. The platform hosts a containerized stack utilizing **Docker Compose** to manage the Flask web server and MongoDB database. The B-series was selected to leverage CPU credits for performance bursts during demonstrations.
* **Storage:** **Azure Managed Disks (Standard SSD)** with a capacity of **32GB (E4 tier)**. By decoupling the disk from the VM, the architecture ensures data persistence for the MongoDB collections even if the virtual machine is redeployed.
* **Networking:** **Standard Static Public IP** and **Network Security Groups (NSG)**. The NSG acts as a stateful firewall, while the static IP ensures consistent DNS mapping and reliable endpoint connectivity.
* **Monitoring:** **Azure Monitor** and **Log Analytics** are integrated to provide deep telemetry, performance monitoring, and error tracking for the Python backend.
* **Optimization (Durability):** **Locally Redundant Storage (LRS)** is implemented for all persistent data, providing 11 nines of durability at the most cost-effective price point.

---

## 2. Itemized Cost Breakdown (Monthly)
*Prices based on Azure Pricing Calculator for the East Asia (Hong Kong) Region.*

| Service Category | Component | Configuration | Monthly Cost (Est.) |
| :--- | :--- | :--- | :--- |
| **Compute** | Virtual Machines | 1 B1s (1 Core, 1 GB RAM) x 730 Hours | **$10.66** |
| **Storage** | Managed Disks | Standard SSD, E4 (32 GiB), LRS | **$2.60** |
| **Networking** | IP Addresses | Standard (ARM), 1 Static IP Address | **$3.65** |
| **Networking** | Bandwidth | Inter-Region Transfer, 5 GB | **$0.00 (Free)** |
| **Management** | Azure Monitor | Log Analytics: Log Data Ingestion | **$0.00 (Free)** |
| **Support** | Support Plan | Basic (Included) | **$0.00** |
| **ESTIMATED TOTAL** | | | **$16.91 USD** |

---
## 3. Pricing Calculator Screenshot

![Pricing Calculator](/report/screenshots/pricing-calculator.png)

---
## 4. Cost Optimization Notes

### 4.1 Selection Logic
* **Regional Strategy:** The architecture is centralized in **East Asia (Hong Kong)** to minimize latency for users in the Philippines, justifying the minor price difference compared to US regions.
* **Tier Optimization:** Utilized **Standard SSD** instead of Premium SSD to reduce storage overhead by approximately **40%**, meeting the I/O needs of the MongoDB deployment without unnecessary cost.
* **Free Tier Utilization:** The design leverages Azure's "Always Free" allowances for Bandwidth and Azure Monitor to keep operational overhead at zero for management services.

### 4.2 Proposed Strategy: Automated Deallocation
To further optimize the budget, an **automated shutdown schedule** is proposed via Azure Automation.
* **Action:** Stop the VM daily from 12:00 AM to 7:00 AM PHT.
* **Impact:** Reduces compute hours from 730 to ~517 per month.
* **Estimated Savings:** Lowers VM cost from $10.66 to **~$7.55**, resulting in an **18% reduction** in total project costs.

---

*Note: This estimation reflects standard Pay-As-You-Go rates, modeling long-term sustainability beyond the initial student credit period.*