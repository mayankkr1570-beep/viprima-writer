"""M1b: synthetic Writer UNO editing probe; run with LibreOffice Python."""
import pathlib
import subprocess
import sys
import tempfile
import time
import uuid
import uno
from com.sun.star.beans import PropertyValue

def prop(name, value):
    p = PropertyValue()
    p.Name = name
    p.Value = value
    return p

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def main():
    engine = pathlib.Path(sys.argv[1]).resolve()
    with tempfile.TemporaryDirectory(prefix="viprima-uno-") as tmp:
        root = pathlib.Path(tmp)
        pipe = "viprima_" + uuid.uuid4().hex
        process = subprocess.Popen([
            str(engine), "-env:UserInstallation=" + (root / "profile").as_uri(),
            "--headless", "--norestore", "--nodefault", "--nofirststartwizard",
            "--accept=pipe,name=" + pipe + ";urp;StarOffice.ServiceManager"
        ])
        desktop = None
        doc = None
        try:
            local = uno.getComponentContext()
            resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
            for attempt in range(60):
                try:
                    remote = resolver.resolve("uno:pipe,name=" + pipe + ";urp;StarOffice.ComponentContext")
                    break
                except Exception:
                    time.sleep(0.5)
            else:
                raise RuntimeError("UNO connection failed")
            desktop = remote.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", remote)
            options = (
                prop("Hidden", True),
                prop("MacroExecutionMode", uno.getConstantByName("com.sun.star.document.MacroExecMode.NEVER_EXECUTE")),
                prop("UpdateDocMode", uno.getConstantByName("com.sun.star.document.UpdateDocMode.NO_UPDATE")),
            )
            doc = desktop.loadComponentFromURL("private:factory/swriter", "_blank", 0, options)
            require(doc is not None, "Writer document creation failed")
            text = doc.Text
            cursor = text.createTextCursor()
            cursor.ParaStyleName = "Heading 1"
            text.insertString(cursor, "ViPrima Writer UNO probe", False)
            text.insertControlCharacter(cursor, uno.getConstantByName("com.sun.star.text.ControlCharacter.PARAGRAPH_BREAK"), False)
            cursor.ParaStyleName = "Text Body"
            cursor.CharWeight = 150.0
            text.insertString(cursor, "Edited through UNO", False)
            cursor.CharWeight = 100.0
            text.insertControlCharacter(cursor, uno.getConstantByName("com.sun.star.text.ControlCharacter.PARAGRAPH_BREAK"), False)
            page = doc.StyleFamilies.getByName("PageStyles").getByName("Standard")
            page.HeaderIsOn = True
            page.HeaderText.String = "ViPrima test header"
            page.FooterIsOn = True
            page.FooterText.String = "ViPrima test footer"
            table = doc.createInstance("com.sun.star.text.TextTable")
            table.initialize(2, 2)
            text.insertTextContent(cursor, table, False)
            for cell, value in (("A1", "Item"), ("B1", "Result"), ("A2", "UNO"), ("B2", "Verified")):
                table.getCellByName(cell).String = value
            path = root / "probe.docx"
            doc.storeAsURL(path.as_uri(), (prop("FilterName", "Office Open XML Text"), prop("Overwrite", True)))
            require(path.is_file() and path.stat().st_size > 0, "DOCX missing")
            doc.close(True)
            doc = None
            doc = desktop.loadComponentFromURL(path.as_uri(), "_blank", 0, options)
            require(doc is not None, "DOCX reopening failed")
            require("ViPrima Writer UNO probe" in doc.Text.String, "Heading content missing")
            require("Edited through UNO" in doc.Text.String, "Edited text missing")
            tables = doc.TextTables
            require(tables.Count == 1, "Table missing")
            require(tables.getByIndex(0).getCellByName("B2").String == "Verified", "Table cell missing")
            pages = doc.StyleFamilies.getByName("PageStyles")
            require(any(pages.getByName(n).HeaderIsOn and "ViPrima test header" in pages.getByName(n).HeaderText.String for n in pages.ElementNames), "Header missing")
            require(any(pages.getByName(n).FooterIsOn and "ViPrima test footer" in pages.getByName(n).FooterText.String for n in pages.ElementNames), "Footer missing")
            pdf = root / "probe.pdf"
            doc.storeToURL(pdf.as_uri(), (prop("FilterName", "writer_pdf_Export"), prop("Overwrite", True)))
            require(pdf.read_bytes().startswith(b"%PDF-"), "PDF invalid")
            print("PASS: UNO document creation, editing, table, header/footer, DOCX reopen and PDF export")
        finally:
            try:
                if doc is not None:
                    doc.close(True)
            finally:
                try:
                    if desktop is not None:
                        desktop.terminate()
                finally:
                    try:
                        process.wait(timeout=15)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()

if __name__ == "__main__":
    main()
