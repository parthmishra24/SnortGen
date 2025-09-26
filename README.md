# 🛡️ VAPT Report Generator & Vulnerability Knowledge Base (CLI Suite)
![Alt text](https://github.com/parthmishra24/Report-Generator/blob/main/snortgen.png?raw=true)
A professional CLI-based toolkit to streamline your **Vulnerability Assessment & Penetration Testing (VAPT)** workflow.  
This tool helps you **document findings**, **generate clean DOCX reports**, and **manage your own AI-powered knowledge base** — all through a powerful Python terminal interface.

---

## ✨ Features

### 📄 VAPT Report Generator
- Generate professional DOCX reports using your own template
- Input vulnerabilities one-by-one (bulk-friendly)
- Auto-fill Description, Impact & Remediation from a local JSON knowledge base
- Attach multiple screenshots per vulnerability
- Export reports to `/reports/` directory
- Fully CLI-driven

### 🧠 Vulnerability Knowledge Base Manager
- Add, view, edit, or delete vulnerabilities in a JSON format
- Quick search by name (with autocomplete)
- Deep keyword search (across all fields)
- Save new vulns from `snortgen.py` or manage via `manage_kb.py`

### 📄 CSV Method
SnortGen supports automated vulnerability reporting using a CSV file for bulk import.
A pre-built template ships with the package and can be copied with:
```bash
python -c "import importlib.resources as r; print(r.files('snortgen.data') / 'snortgen_template.csv')"
```

#### ✏️ How to Use:
1. Open snortgen_template.csv in any spreadsheet editor (Excel, Google Sheets, etc.).
2. Fill in the required vulnerability details as per the headers: name, cwe_id, description, impact, remediation, affected_url, severity, status, and screenshots
3. For multiple screenshots, separate file paths using a semicolon ```;```.
4. Save the file and run the tool: ```snortgen```.
5. Enter the full path to your .csv file when asked.
---

## ⚙️ Requirements

Python 3.8+

## ⬇️ Installation

Install the latest published version directly from PyPI:

```bash
pip install snortgen
```

For local development inside this repository:

```bash
pip install -e .
```

The install process automatically exposes two console scripts:

| Command | Description |
| --- | --- |
| `snortgen` | Launch the interactive report generator |
| `snortgen-manage-kb` | Open the knowledge base management helper |

## 🚀 Usage

1. 📄 Generate a VAPT Report
```
snortgen
```
What it does:
- Prompts for the path to your DOCX template
- Asks for the number of vulnerabilities
- Supports auto-filling from a local knowledge base stored at `~/.snortgen/vuln_knowledgebase.json`
- Supports bulk screenshots per vuln
- Saves final report in `/reports` with a custom filename

2. 🧠 Manage the Knowledge Base
```
snortgen-manage-kb
```
CLI Options:
- ➕ Add a new entry
- 🔍 Quick search by name (autocomplete)
- 🧠 Deep keyword search (across all fields)
- 📖 View all entries
- ✏️ Edit an existing vulnerability
- ❌ Delete a vulnerability
- 🚪 Exit

The first time either command runs a default knowledge base will be copied into `~/.snortgen/`. Subsequent edits are persisted there so upgrades do not overwrite your changes.

### ⬆️ Upgrade

To upgrade to the latest release at any time, run:

```bash
snortgen update
```

The command invokes `pip` behind the scenes and reports whether a newer version was installed or if you are already up to date.

---

💡 Smart Autofill Features

During report generation:
- You select a vulnerability from an autocomplete list
- If the entry exists in JSON → description, impact, remediation, and CWE-ID auto-fill
- Otherwise, you enter manually and can choose to save it

---

📦 Output
- Report is generated in .docx format using your template
Includes:
- Vulnerability summary table
- Detailed findings with screenshots
- Saved inside /reports/ folder

---

👨‍💻 Author

Parth Mishra | 
Security Engineer | Red Team Enthusiast
