# Architecture decision 001 — document engine

Status: provisional, M1a passed. Evidence: https://github.com/mayankkr1570-beep/viprima-writer/actions/runs/45872722065

LibreOffice 26.8.3.1 installed on Windows Server 2025 and converted HTML to DOCX, DOCX to DOCX and DOCX to PDF. Text, bold/italic and table XML checks passed. This does not validate visual fidelity or a custom editor.

Prefer a native LibreOffice Writer derivative using its existing layout, editing, accessibility and UNO command infrastructure, rather than a second HTML editor or conversion-only wrapper. Evaluate customization of Notebookbar, Writer-only entry point, local profile, branding and distribution. Preserve upstream notices and source obligations; review trademark policy and component licenses before shipping. The full upstream build is not yet demonstrated. No paid runner or proprietary SDK approved.

## Next gates
- M1b: programmatic document editing through bundled Python UNO, not merely conversion; generate document, header/footer, table, save DOCX, reopen and inspect content, export PDF.
- M1c: establish reproducible native source build, exact upstream revision, toolchain/resource requirements, licensing review and UI customization feasibility.
- M2: independent application UI and packaging, only after architecture validated.
- Later: visual Word interoperability, Windows 11 GUI testing, accessibility, security/offline isolation, recovery, signing and installer validation.

No production installer or commercial readiness claim until release gates pass.
