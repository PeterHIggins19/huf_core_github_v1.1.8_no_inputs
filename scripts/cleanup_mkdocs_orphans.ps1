\
# scripts/cleanup_mkdocs_orphans.ps1
# Optional PowerShell equivalent to cleanup_mkdocs_orphans.py.
#
# If your machine blocks unsigned scripts, run this in the same PowerShell session first:
#   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
#
# Then:
#   .\scripts\cleanup_mkdocs_orphans.ps1

$ErrorActionPreference = "Stop"

$root   = Split-Path -Parent $PSScriptRoot
$docs   = Join-Path $root "docs"
$nested = Join-Path $docs "docs"
$notes  = Join-Path $root "notes/orphaned_docs"

New-Item -ItemType Directory -Force $notes | Out-Null

function Get-TextHash([string]$path) {
  if (-not (Test-Path -LiteralPath $path)) { return $null }
  $txt = Get-Content -LiteralPath $path -Raw -Encoding UTF8
  $txt = $txt -replace "`r`n", "`n"
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($txt)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  ($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") }) -join ""
}

Write-Host ("[root] {0}" -f $root)
Write-Host ("[docs] {0}" -f $docs)

# Move patch snippet out of docs/
$patch = Join-Path $docs "vector_db_coherence_one_pager.patch.md"
if (Test-Path -LiteralPath $patch) {
  $dest = Join-Path $notes "vector_db_coherence_one_pager.patch.md"
  Move-Item -Force -LiteralPath $patch -Destination $dest
  Write-Host "[move] docs/vector_db_coherence_one_pager.patch.md -> notes/orphaned_docs/"
}

# Reconcile docs/docs nesting
if (Test-Path -LiteralPath $nested) {
  Write-Host "[found] docs/docs (nested) — reconciling..."
  Get-ChildItem -LiteralPath $nested -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($nested.Length).TrimStart('\','/')
    $target = Join-Path $docs $rel

    if (Test-Path -LiteralPath $target) {
      $h1 = Get-TextHash $_.FullName
      $h2 = Get-TextHash $target
      if ($h1 -eq $h2) {
        Remove-Item -Force -LiteralPath $_.FullName
        Write-Host ("[delete] duplicate nested file: docs/docs/{0}" -f $rel)
      } else {
        $dest = Join-Path $notes $rel
        New-Item -ItemType Directory -Force (Split-Path $dest) | Out-Null
        Move-Item -Force -LiteralPath $_.FullName -Destination $dest
        Write-Host ("[move] differing nested file -> notes/orphaned_docs/{0}" -f $rel)
      }
    } else {
      New-Item -ItemType Directory -Force (Split-Path $target) | Out-Null
      Move-Item -Force -LiteralPath $_.FullName -Destination $target
      Write-Host ("[move] docs/docs/{0} -> docs/{0}" -f $rel)
    }
  }

  # Remove empty nested dirs
  Get-ChildItem -LiteralPath $nested -Recurse -Directory |
    Sort-Object FullName -Descending | ForEach-Object {
      if (-not (Get-ChildItem -LiteralPath $_.FullName -Force | Select-Object -First 1)) {
        Remove-Item -Force -LiteralPath $_.FullName
      }
    }

  if (-not (Get-ChildItem -LiteralPath $nested -Force | Select-Object -First 1)) {
    Remove-Item -Force -LiteralPath $nested
    Write-Host "[delete] removed empty docs/docs"
  }
} else {
  Write-Host "[ok] no docs/docs nesting found"
}

Write-Host "[done] cleanup complete. Rebuild with:"
Write-Host '       .\.venv\Scripts\python -m mkdocs build --strict'
