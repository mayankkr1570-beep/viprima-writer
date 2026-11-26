# Native build and UI integration plan (M1c)

Candidate upstream: LibreOffice core, evaluated binary build ID 861effc5289d539f15c4c18d1ba8579ffd78728b (26.8.3.1). Resolve this exact commit in upstream before any patching. Official reference: https://github.com/LibreOffice/core and https://dev.blog.documentfoundation.org/2024/10/17/wsl-for-building-libreoffice/ .

The Windows runner has demonstrated MSVC 2026, not the upstream documented VS 2022 baseline. Probe WSL distribution, VS 2022 C++ installation, disk and upstream revision first. Do not silently substitute compiler or spend money on larger runners. The preflight does not compile the office engine.

## Native interface work
Use the existing Writer VCL/Notebookbar UI and command dispatch; inspect sw/uiconfig/swriter/ui/notebookbar.ui at the exact revision. Preserve editing, accessibility and undo/redo semantics. Customize native resources in a maintained patch series rather than edit installed binaries. Keep a separate profile, disable automatic online functionality and enforce macro and external-content policies; verify with network-denied tests. Provide Writer-focused entry point and independent original icons after trademark review. Do not strip upstream legal notices.

## Distribution gates
Review MPL and third-party licensing, trademark policy, source availability, security updates, reproducible dependency manifest and installer coexistence with existing LibreOffice. Do not ship an upstream installer renamed as ViPrima. GUI acceptance requires Windows 11 desktop testing. Native build and actual UI integration remain unverified.
