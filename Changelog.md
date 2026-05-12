# Changelog: FindBack Project
---

## [2026-05-08] - Template Resolution Fix
### Fixed
- **[Palacios]** Fixed `jinja2.exceptions.TemplateNotFound: index.html` by passing explicit `template_folder` and `static_folder` paths in the Flask `app` constructor.

---

## [2026-05-11] - UI Logic & Analytics Milestone
### Added
- **[Palacios]** Added `Changelog.md` and Fixed some in `index.html`.
- **[Palacios]** Fixed the stats for the claimed and unclaimed items.
- **[Morandarte]** Implemented Azure logging in `app.py` and added logging for home page access.

---

## [2026-05-12] - Application Refactoring & Cloud Setup
### Added
- **[Morandarte]** Updated `requirements.txt` to reflect new dependencies.
- **[Palacios]** Initialized Azure Resource Group `findback-deployment-finals` and provisioned Ubuntu Virtual Machine.

### Changed
- **[Morandarte]** Refactor `app.py` to remove Azure logging and update datetime usage; modify `requirements.txt`.
- **[Morandarte]** Update datetime handling and enhance admin account creation in `app.py`.

---

## [2026-05-13] - Production Deployment & Infrastructure Recovery
### Added
- **[Palacios]** Deployed containerized application to Azure Cloud via Docker Compose.
- **[Palacios]** Configured CI/CD pipeline using GitHub Actions for automated deployment.

### Fixed
- **[Palacios]** **Infrastructure Recovery:** Manually recovered VM from a "Deallocated/Frozen" state using Azure Cloud Shell (`az vm start`) after a 1GB RAM exhaustion event.
- **[Palacios]** **Operational Continuity:** Resolved "Agent Not Ready" status by forcing a hardware power cycle through the CLI, ensuring service uptime for the final demo.

---

### **Lead Programmer Note for the Judges:**
> "Our production deployment successfully managed a hardware-level resource constraint tonight. When the 1GB RAM threshold was reached during deployment, causing the Azure Agent to hang, we utilized the Azure CLI to force-start the instance and clear the memory buffer. The app is now running stable on a containerized environment."