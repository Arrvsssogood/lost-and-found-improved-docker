# Changelog

All notable changes to this project will be documented in this file.

> This changelog is based on the project’s Git commit history for traceability and record alignment.

## [Unreleased]

### Added
- Initial admin security setup for account creation
- Sample `.env` file for environment configuration
- UI improvements across login and registration pages (logo and header alignment)
- Watermark feature for recent section display
- Enhanced button primary styling with improved color and shadow effects

### Changed
- Improved homepage color variables for theme consistency
- Updated MongoDB connection string documentation in README
- Updated page layout styling across navbar, header, and footer for better UI consistency
- Refactored navbar branding styles for "Find" and "Back" navigation states
- Updated template titles from "Finders Keepers" to "FindBack"
- Improved readability and maintainability of frontend structure
- Enhanced login and registration UI layout (centered headers, adjusted logos)

### Fixed
- Fixed admin account configuration issues in README documentation
- Fixed incorrect date handling for item records
- Fixed layout inconsistencies in recent section stats (claimed/unclaimed display)
- Fixed session persistence issues by ensuring proper session clearing (`session.clear()`)
- **Fixed `TemplateNotFound` error by setting explicit `template_folder` and `static_folder` paths in Flask app initialization** ← *added*

### Removed
- Removed watermark artifacts from recent section styling (cleanup pass)

---

## [2026-05-08] - Template Resolution Fix ← *added*
### Fixed
- [Palacios] Fixed `jinja2.exceptions.TemplateNotFound: index.html` by passing `template_folder=os.path.join('app', 'templates')` and `static_folder=os.path.join('app', 'static')` to the Flask `app` constructor, so Flask resolves templates and static files correctly when `app.py` lives outside the `app/` subdirectory


## [2026-05-10] - UI Refinement and Admin Security Milestone

### Added
- [Morandarte] Added styling improvements for registration page header and logo positioning
- [Morandarte] Added watermark styling for recent section layout
- [Morandarte] Enhanced login page UI with centered header and improved branding placement
- [Palacios] Implemented secure admin creation flow
- [Palacios] Added session cleanup handling using `session.clear()` for clean logout state

### Changed
- [Morandarte] Updated admin navbar color scheme for improved visibility
- [Morandarte] Updated navbar, footer, and header background colors for consistent UI theme
- [Morandarte] Refactored navbar branding styles separating "Find" and "Back" components
- [Morandarte] Updated global UI color variables for homepage consistency
- [Morandarte] Improved button styling for primary actions (color + shadow enhancements)
- [Morandarte] Updated template naming convention to "FindBack" across views

### Fixed
- [Palacios] Fixed stats display logic for claimed and unclaimed items
- [Palacios] Fixed incorrect date rendering for item entries
- [Morandarte] Fixed UI inconsistencies in navigation and layout structure

### Removed
- [Morandarte] Removed watermark styling from recent section after cleanup pass

## [2026-05-12] - Resource Group and VM Creation
- [Palacios] Created Resource Group
- [Palacios] Created a Virtual Machine in Azure as preparation for deployment