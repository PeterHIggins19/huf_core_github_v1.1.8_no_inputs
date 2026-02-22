param(
  [string]$Root = "notes\partner_html",
  [switch]$IncludeLegacyNotes
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Patch-Folder([string]$Folder) {
  if (!(Test-Path $Folder)) {
    Write-Host "[skip] Folder not found: $Folder"
    return
  }

  # IMPORTANT: use an ordered list of replacement pairs (PowerShell hashtables are case-insensitive by default,
  # which can cause "duplicate key" parser errors for URLs that differ only by case, e.g. PeterHiggins vs PeterHIggins).
  $pairs = @(
    # Old docs site -> new docs site (with and without trailing slash)
    @("https://peterhiggins19.github.io/huf_core_github_v1.1.8_no_inputs/", "https://peterhiggins19.github.io/huf_core/"),
    @("https://peterhiggins19.github.io/huf_core_github_v1.1.8_no_inputs",  "https://peterhiggins19.github.io/huf_core/"),

    # Old repo URL -> new repo URL (correct + common typo variant)
    @("https://github.com/PeterHiggins19/huf_core_github_v1.1.8_no_inputs", "https://github.com/PeterHiggins19/huf_core"),
    @("https://github.com/PeterHIggins19/huf_core_github_v1.1.8_no_inputs", "https://github.com/PeterHiggins19/huf_core"),

    # git+ install URLs
    @("git+https://github.com/PeterHiggins19/huf_core_github_v1.1.8_no_inputs.git", "git+https://github.com/PeterHiggins19/huf_core.git"),

    # Repo slug text (non-URL) and cd instructions
    @("PeterHiggins19/huf_core_github_v1.1.8_no_inputs", "PeterHiggins19/huf_core"),
    @("cd huf_core_github_v1.1.8_no_inputs", "cd huf_core"),

    # Fallback: plain repo folder name occurrences (kept last to avoid breaking more specific replacements)
    @("huf_core_github_v1.1.8_no_inputs", "huf_core")
  )

  $files = Get-ChildItem $Folder -Recurse -File -Include *.html,*.md,*.txt
  if (!$files -or $files.Count -eq 0) {
    Write-Host "[skip] No files found in: $Folder"
    return
  }

  # Make timestamped backup (cheap insurance)
  $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
  $backup = Join-Path (Split-Path $Folder -Parent) ("partner_html_backup_" + $timestamp)
  Copy-Item $Folder $backup -Recurse -Force
  Write-Host "[ok] Backup created: $backup"

  $changed = 0
  foreach ($f in $files) {
    $txt = Get-Content -Raw -LiteralPath $f.FullName
    $new = $txt
    foreach ($pair in $pairs) {
      $from = $pair[0]
      $to   = $pair[1]
      $new = $new.Replace($from, $to)
    }
    if ($new -ne $txt) {
      Set-Content -LiteralPath $f.FullName -Value $new -Encoding utf8
      $changed++
      Write-Host ("[patched] " + $f.FullName)
    }
  }

  Write-Host "[done] Patched $changed file(s) in: $Folder"
}

Patch-Folder -Folder $Root

if ($IncludeLegacyNotes) {
  Patch-Folder -Folder "notes\legacy_md"
}
