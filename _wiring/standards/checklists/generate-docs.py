from __future__ import annotations

import datetime
import json
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
CONFIG_ROOT = REPO_ROOT / "_config" / "standards" / "checklists"
TEMPLATE_ROOT = REPO_ROOT / "_templates" / "standards" / "checklists"
OUTPUT_ROOT = REPO_ROOT / "docs" / "standards" / "checklists"
DOCS_ROOT = OUTPUT_ROOT / "docs"

DATA_FILE = CONFIG_ROOT / "checklists.json"
TEMPLATE_FILE = TEMPLATE_ROOT / "index.html"
ICON_DIR = CONFIG_ROOT / "icons"
OUTPUT_ICON_DIR = DOCS_ROOT / "icons"


def render_template(template: str, replacements: dict[str, str]) -> str:
    content = template
    for key, value in replacements.items():
        content = content.replace("${" + key + "}", value)
    return content


def copy_icons() -> None:
    if OUTPUT_ICON_DIR.exists():
        shutil.rmtree(OUTPUT_ICON_DIR)
    if ICON_DIR.exists():
        shutil.copytree(ICON_DIR, OUTPUT_ICON_DIR)


def write_root_redirect() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    OUTPUT_ROOT.joinpath("index.html").write_text(
        """<!DOCTYPE html>
<html>
<head><meta http-equiv="refresh" content="0; url='docs/index.html'" /></head>
<body></body>
</html>""",
        encoding="utf-8",
    )


def main() -> None:
    DOCS_ROOT.mkdir(parents=True, exist_ok=True)
    copy_icons()

    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    template = TEMPLATE_FILE.read_text(encoding="utf-8")
    rendered = render_template(
        template,
        {
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "data": json.dumps(data),
        },
    )

    DOCS_ROOT.joinpath("index.html").write_text(rendered, encoding="utf-8")
    write_root_redirect()
    print(DOCS_ROOT / "index.html")


if __name__ == "__main__":
    main()
