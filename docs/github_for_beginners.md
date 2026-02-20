# GitHub for HUF (Beginner, GUI-first)

This is a **plain-language** guide to using HUF on GitHub with **minimal jargon**.
You do **not** need to learn command-line git to run HUF.

---

## What is GitHub?

GitHub is a website that stores a project folder online and keeps a **history of every change**.

For HUF, GitHub is where:

- the **code** lives (the library + CLI)
- the **docs** live (Handbook + Reference Manual)
- fixes and improvements can be shared safely

---

## The easiest way: GitHub Desktop (point-and-click)

### 1) Create a GitHub account (optional but recommended)

- Go to GitHub and create an account.
- You can still download HUF without an account, but GitHub Desktop works best when signed in.

### 2) Install GitHub Desktop

- Download and install GitHub Desktop.

### 3) Get HUF onto your computer (“Clone”)

1. Open GitHub Desktop
2. **File → Clone repository…**
3. Paste the HUF repository URL
4. Choose a local folder (example: `Documents/HUF`)
5. Click **Clone**

Now HUF is a normal folder on your computer.

---

## How to run HUF after cloning

From the HUF folder:

- Windows: double-click `START_HERE_WINDOWS.bat`
- macOS: right-click `START_HERE_MAC.command` → **Open**
- Linux: run `./start_here_linux.sh`

Then fetch data (Windows PowerShell copy/paste):

```powershell
.\.venv\Scripts\python scripts/fetch_data.py --markham --toronto --yes
```

Run a demo:

```powershell
.\.venv\Scripts\huf --help
```

---

## How to get updates (no command line)

In GitHub Desktop:

1. Open the HUF repository
2. Click **Fetch origin**
3. If updates are available, click **Pull origin**

That’s it — your local folder updates.

---

## Do I need branches and pull requests?

Not to run HUF. Branches and pull requests matter when you want to **propose changes** or safely test edits.

- **Branch** = a safe copy of the project to experiment in
- **Pull Request** = a polite way to ask: “Can we add my changes?”
