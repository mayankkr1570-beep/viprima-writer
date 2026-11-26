"""First native ribbon resource customization, applied only to a pinned source tree.
No command bindings, upstream notices or runtime binaries are removed."""
import argparse
import pathlib
import subprocess
import xml.etree.ElementTree as ET

REVISION = "861effc5289d539f15c4c18d1ba8579ffd78728b"
RESOURCE = pathlib.Path("sw/uiconfig/swriter/ui/notebookbar.ui")
LABELS = {
    "TabbedWriter|labelHomeStyle": ("Style", "Styles"),
    "TabbedWriter|labelInsertGraphic": ("Graphic", "Pictures"),
    "TabbedWriter|labelReferencesIndex": ("Index", "Contents & Index"),
    "TabbedWriter|labelViewWidgets": ("Widgets", "Workspace"),
}
def customize(root):
    actual = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
    if actual != REVISION:
        raise RuntimeError("Unexpected upstream revision: " + actual)
    path = root / RESOURCE
    original = path.read_bytes()
    text = original.decode("utf-8")
    tree = ET.fromstring(text)
    for context, (old, new) in LABELS.items():
        nodes = [n for n in tree.iter("property") if n.get("name") == "label" and n.get("context") == context]
        if len(nodes) != 1 or nodes[0].text != old:
            raise RuntimeError("Upstream label mismatch: " + context)
        prefix = 'context="' + context + '">'
        before = prefix + old + "</property>"
        after = prefix + new.replace("&", "&amp;") + "</property>"
        if text.count(before) != 1:
            raise RuntimeError("Unexpected XML serialization: " + context)
        text = text.replace(before, after, 1)
    changed = ET.fromstring(text)
    def commands(t):
        return [(n.tag, tuple(sorted(n.attrib.items())), n.text) for n in t.iter("property") if n.get("name") in ("action-name", "command", "action_name")]
    if commands(tree) != commands(changed):
        raise RuntimeError("Command binding changed")
    path.write_bytes(text.encode("utf-8"))
    print("Customized four native ribbon labels; command bindings preserved.")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=pathlib.Path)
    customize(parser.parse_args().source)
