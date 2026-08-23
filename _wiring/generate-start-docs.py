from __future__ import annotations

import datetime
import json
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_ROOT = REPO_ROOT / "_config" / "start"
CONFIG_PATH = CONFIG_ROOT / "apps.json"
TEMPLATE_ROOT = REPO_ROOT / "_templates" / "start"
TEMPLATE_PATH = TEMPLATE_ROOT / "index.html"
DOCS_ROOT = REPO_ROOT / "docs" / "start"

DEFAULT_DOMAIN_NAME = "Data Explorers and Dashboards"
DEFAULT_DOMAIN_DESCRIPTION = "A launcher for controls, standards, and data explorers. Available free on <a href= 'https://github.com/zeljkoobrenovic/lightweight-data-explorers' target='_blank'>GitHub</a>."


def copy_directory(source: Path, target: Path) -> None:
    if source.exists():
        shutil.copytree(source, target, dirs_exist_ok=True)


def render_template(template: str, replacements: dict[str, str]) -> str:
    content = template
    for key, value in replacements.items():
        content = content.replace("${" + key + "}", value)
    return content


def value_from_config(data: dict, *keys: str, default: str) -> str:
    config = data.get("config", {})
    for key in keys:
        value = data.get(key) or config.get(key)
        if value:
            return str(value)
    return default


def main() -> None:
    if DOCS_ROOT.exists():
        shutil.rmtree(DOCS_ROOT)
    DOCS_ROOT.mkdir(parents=True, exist_ok=True)

    copy_directory(TEMPLATE_ROOT / "icons", DOCS_ROOT / "icons")
    copy_directory(CONFIG_ROOT / "icons", DOCS_ROOT / "icons")

    apps = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    rendered = render_template(
        template,
        {
            "date": datetime.date.today().strftime("%Y-%m-%d"),
            "apps": json.dumps(apps),
            "domain_name": value_from_config(
                apps,
                "domain_name",
                "domainName",
                "name",
                default=DEFAULT_DOMAIN_NAME,
            ),
            "domain_description": value_from_config(
                apps,
                "domain_description",
                "domainDescription",
                "description",
                default=DEFAULT_DOMAIN_DESCRIPTION,
            ),
        },
    )

    output_path = DOCS_ROOT / "index.html"
    output_path.write_text(rendered, encoding="utf-8")
    print(output_path)


if __name__ == "__main__":
    main()
