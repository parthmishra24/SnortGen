"""Command line interface for SnortGen."""

from __future__ import annotations

import csv
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Sequence

import questionary
from colorama import Fore, Style, init
from pyfiglet import Figlet

from .docx_report_generator import generate_docx_report
from .style import custom_style
from .vuln_input_handler import collect_vulnerabilities

init(autoreset=True)


def color_status(text: str) -> str:
    """Return a colorized representation of a vulnerability status."""
    normalized = text.strip().lower()
    if normalized == 'open':
        color = Fore.RED
    elif normalized == 'fixed':
        color = Fore.GREEN
    elif normalized == 'validated':
        color = Fore.CYAN
    else:
        color = ""
    return f"{color}{text}{Style.RESET_ALL if color else ''}"


def color_severity(text: str) -> str:
    """Return a colorized representation of a severity string."""
    normalized = text.strip().lower()
    if normalized == 'critical':
        color = Fore.LIGHTBLACK_EX
    elif normalized == 'high':
        color = Fore.RED
    elif normalized == 'medium':
        color = Fore.YELLOW
    elif normalized == 'low':
        color = Fore.GREEN
    else:
        color = ""
    return f"{color}{text}{Style.RESET_ALL if color else ''}"


def parse_csv(csv_path: Path) -> list[dict[str, str | list[str]]]:
    """Parse a CSV file into the structure expected by the report generator."""
    vulnerabilities: list[dict[str, str | list[str]]] = []
    try:
        with csv_path.open('r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                vulnerabilities.append({
                    "name": row['name'],
                    "cwe_id": row['cwe_id'],
                    "description": row['description'],
                    "impact": row['impact'],
                    "remediation": row['remediation'],
                    "affected_url": row['affected_url'],
                    "severity": row['severity'],
                    "status": row['status'],
                    "screenshots": row['screenshots'].split(';') if row.get('screenshots') else []
                })
        return vulnerabilities
    except Exception as exc:
        print(f"❌ Failed to parse CSV: {exc}")
        return []


def print_banner() -> None:
    terminal_width = shutil.get_terminal_size().columns
    f = Figlet(font='slant')
    banner = f.renderText("SnortGen")

    for line in banner.splitlines():
        print(Fore.CYAN + Style.BRIGHT + line.center(terminal_width))

    print(Fore.YELLOW + Style.BRIGHT + "by Parth Mishra".center(terminal_width))
    print(Fore.MAGENTA + "🔐 CLI VAPT Report Generator".center(terminal_width))
    print(Fore.WHITE + "────────────────────────────────────────────────────────".center(terminal_width))


def prompt_template_path() -> Path:
    while True:
        try:
            template_path = questionary.path("Enter path to the report template (.docx):", style=custom_style).ask()
            if template_path is None:
                print("\n🛑 Cancelled by user.")
                sys.exit(0)
            candidate = Path(template_path)
            if not candidate.is_file():
                print(f"❌ File not found: {candidate}")
            else:
                return candidate
        except KeyboardInterrupt:
            print("\n🛑 Cancelled by user.")
            sys.exit(0)


def render_vulnerability_table(vulns: Sequence[dict[str, str | list[str]]]) -> None:
    print("╭────┬──────────────────────────────┬──────────────┬────────────╮")
    print("│ No │ Vulnerability                │ Severity     │ Status     │")
    print("├────┼──────────────────────────────┼──────────────┼────────────┤")
    for index, vuln in enumerate(vulns, 1):
        name = str(vuln['name'])[:28].ljust(28)
        severity = str(vuln['severity']).capitalize().ljust(12)
        status = str(vuln['status']).capitalize().ljust(10)
        print(
            f"│ {str(index).rjust(2)} │ {name} │ {color_severity(severity)} │ {color_status(status)} │"
        )
    print("╰────┴──────────────────────────────┴──────────────┴────────────╯")


def ensure_reports_directory(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def automated_flow(reports_dir: Path) -> None:
    template_path = prompt_template_path()
    vulnerabilities = collect_vulnerabilities()
    if not vulnerabilities:
        return

    render_vulnerability_table(vulnerabilities)

    confirm = questionary.confirm("📝 Proceed to generate the report?", style=custom_style).ask()
    if not confirm:
        print("❌ Report generation cancelled.")
        sys.exit(0)

    generate_docx_report(
        vulnerabilities=vulnerabilities,
        template_path=str(template_path),
        output_path=str(reports_dir)
    )


def csv_flow(reports_dir: Path) -> None:
    csv_path = questionary.path("📄 Enter path to CSV file:", style=custom_style).ask()
    if not csv_path:
        print("❌ Invalid or missing CSV file path.")
        return
    candidate = Path(csv_path)
    if not candidate.is_file():
        print("❌ Invalid or missing CSV file path.")
        return
    vulnerabilities = parse_csv(candidate)
    if not vulnerabilities:
        return
    template_path = prompt_template_path()
    generate_docx_report(
        vulnerabilities=vulnerabilities,
        template_path=str(template_path),
        output_path=str(reports_dir)
    )


def main() -> None:
    reports_dir = ensure_reports_directory(Path.cwd() / "reports")

    mode = questionary.select(
        "🔰 How do you want to proceed?",
        choices=["Automated Method", "CSV Method"],
        style=custom_style
    ).ask()

    if mode == "Automated Method":
        automated_flow(reports_dir)
    elif mode == "CSV Method":
        csv_flow(reports_dir)
    else:
        print("🛑 Cancelled by user.")


def _get_installed_version() -> str | None:
    try:
        from importlib.metadata import PackageNotFoundError, version
    except ImportError:  # pragma: no cover
        from importlib_metadata import PackageNotFoundError, version  # type: ignore
    try:
        return version("snortgen")
    except PackageNotFoundError:
        return None


def update_package() -> None:
    """Update SnortGen via pip."""
    print("🔄 Checking for SnortGen updates...\n")
    before = _get_installed_version()
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "snortgen"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        print("❌ Failed to update SnortGen.")
        output = (exc.stdout or "") + ("\n" + exc.stderr if exc.stderr else "")
        if output.strip():
            print(output.strip())
        return

    combined_output = (result.stdout or "") + ("\n" + result.stderr if result.stderr else "")
    if combined_output.strip():
        print(combined_output.strip())

    after = _get_installed_version()
    if before and after and before == after:
        print(f"✅ SnortGen {after} is already up to date.")
    elif after:
        print(f"✅ SnortGen has been updated to version {after}.")
    else:
        print("✅ SnortGen is up to date.")


def run(argv: Sequence[str] | None = None) -> None:
    args = list(argv if argv is not None else sys.argv[1:])
    if args and args[0].lower() in {"update", "upgrade"}:
        update_package()
        return

    try:
        print_banner()
        main()
    except KeyboardInterrupt:
        print("\n🛑 Exiting... Operation cancelled by user (Ctrl+C)")
        sys.exit(0)


if __name__ == "__main__":  # pragma: no cover
    run()
