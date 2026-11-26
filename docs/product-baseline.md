# ViPrima Writer — approved product baseline

Status: engineering feasibility; no production binary exists.

## Requirements
- Commercially distributable free/open-source, independently branded Windows 11 Intel/AMD x64 desktop application.
- Completely offline local storage; no AI, telemetry, account or cloud dependency.
- Modern Word-inspired ribbon, adaptive layout, accessible keyboard operation, navigation, contextual properties and focus mode.
- DOCX creation/editing, styles, lists, sections, pagination, headers/footers, images/wrapping, tables, references, comments, revisions, comparison, mail merge, print/PDF, templates, branding, clause library and quality checks.
- Safe saving, recovery, compatibility warnings, blocked macro execution and automatic external retrieval.
- Deliver a verified standalone installer, not merely source code.

## Engineering gates
M0 native Windows compiler smoke test. M1 compare LibreOffice and ONLYOFFICE, verify build resources and branding/licensing obligations, test DOCX fidelity and offline behavior. Prefer LibreOffice provisionally; no engine selected finally.
M2 application architecture and UX; M3 core and advanced operations; M4 automated regression/security/compatibility; M5 Windows 11 desktop and installer testing; M6 signed or explicitly unsigned release with hashes, source and notices.

No release until actual acceptance tests pass. No client data in public repository. Pin third-party dependencies and actions to reviewed versions; require explicit approval for any paid runners. GitHub Windows Server CI is not a replacement for Windows 11 desktop testing. Do not remove upstream legal notices. Final project licence to be established before distributing engine-derived code.

## M0 acceptance
Compile and execute an x64 native smoke executable on windows-2025; record OS, memory, disk and SHA-256. This is not a document engine or production release.
