from __future__ import annotations

import json
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CONFIG_ROOT = REPO_ROOT / "_config" / "data" / "scorecard"
TEMPLATE_ROOT = REPO_ROOT / "_templates" / "scorecard"
IMPORTS_ROOT = REPO_ROOT / "_templates" / "_imports"
DOCS_ROOT = REPO_ROOT / "docs" / "data-explorers" / "scorecard"

DATA_FILE = CONFIG_ROOT / "scorecard.json"
TEMPLATE_FILE = TEMPLATE_ROOT / "index.html"
BREADCRUMBS_FILE = TEMPLATE_ROOT / "index_breadcrumbs.json"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def render_template(template: str, replacements: dict[str, str]) -> str:
    content = template
    for key, value in replacements.items():
        content = content.replace("${" + key + "}", value)
    return content


def render_breadcrumbs(home_label: str) -> str:
    return render_template(read_text(BREADCRUMBS_FILE), {"domain_name": home_label})


def copy_directory(source: Path, target: Path) -> None:
    if source.exists():
        shutil.copytree(source, target, dirs_exist_ok=True)


def company_name(payload: dict) -> str:
    return payload.get("company", {}).get("name", "Business Scorecard")


def main() -> None:
    if DOCS_ROOT.exists():
        shutil.rmtree(DOCS_ROOT)
    DOCS_ROOT.mkdir(parents=True, exist_ok=True)

    copy_directory(TEMPLATE_ROOT / "icons", DOCS_ROOT / "icons")
    copy_directory(CONFIG_ROOT / "icons", DOCS_ROOT / "icons")

    payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    page_title = f"{company_name(payload)} Business Scorecard"
    rendered = render_template(
        read_text(TEMPLATE_FILE),
        {
            "page_title": page_title,
            "tabs_style": read_text(IMPORTS_ROOT / "tabs" / "style.html"),
            "tabs_script": read_text(IMPORTS_ROOT / "tabs" / "script.html"),
            "breadcrumbs_style": read_text(IMPORTS_ROOT / "breadcrumbs" / "style.html"),
            "breadcrumbs_script": read_text(IMPORTS_ROOT / "breadcrumbs" / "script.html"),
            "breadcrumbs": render_breadcrumbs("Data Explorers"),
            "data": json.dumps(payload),
        },
    )

    output_path = DOCS_ROOT / "index.html"
    output_path.write_text(rendered, encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
