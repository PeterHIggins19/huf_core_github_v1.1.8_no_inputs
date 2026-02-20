\
# Cleanup orphan docs that confuse mkdocs navigation
# Safe behavior:
# - If docs/docs/<file> exists AND docs/<file> exists and contents are identical => delete the nested copy
# - If docs/docs/<file> exists and docs/<file> is missing => move it into docs/
# - If contents differ => move the nested copy into notes/orphaned_docs/ (no data loss)
# - Move vector_db_coherence_one_pager.patch.md out of docs/ into notes/orphaned_docs/

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$docs = Join-Path $root "docs"
$nested = Join-Path $docs "docs"
$notes = Join-Path $root "notes/orphaned_docs"

New-Item -ItemType Directory -Force $notes | Out-Null

function Get-TextHash([string]$path) {
  if (-not (Test-Path $path)) { return $null }
  $txt = Get-Content -LiteralPath $path -Raw -Encoding UTF8
  # Normalize newlines so CRLF vs LF doesn't create false diffs
  $txt = $txt -replace "`r`n", "`n"
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($txt)
  $sha = [System.Security.Cryptography.SHA256]::Create()
  ($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString("x2") }) -join ""
}

Write-Host "[root] $root"
Write-Host "[docs] $docs"

# 1) Move patch snippet out of docs/
$patch = Join-Path $docs "vector_db_coherence_one_pager.patch.md"
if (Test-Path $patch) {
  $dest = Join-Path $notes "vector_db_coherence_one_pager.patch.md"
  Move-Item -Force $patch $dest
  Write-Host "[move] docs/vector_db_coherence_one_pager.patch.md -> notes/orphaned_docs/"
}

# 2) Fix accidental docs/docs/ nesting
if (Test-Path $nested) {
  Write-Host "[found] docs/docs (nested) — reconciling..."
  Get-ChildItem -LiteralPath $nested -Recurse -File | ForEach-Object {
    $rel = $_.FullName.Substring($nested.Length).TrimStart('\','/')
    $target = Join-Path $docs $rel

    if (Test-Path $target) {
      $h1 = Get-TextHash $_.FullName
      $h2 = Get-TextHash $target
      if ($h1 -eq $h2) {
        Remove-Item -Force $_.FullName
        Write-Host "[delete] duplicate nested file: docs/docs/$rel"
      } else {
        $dest = Join-Path $notes $rel
        New-Item -ItemType Directory -Force (Split-Path $dest) | Out-Null
        Move-Item -Force $_.FullName $dest
        Write-Host "[move] differing nested file -> notes/orphaned_docs/$rel"
      }
    } else {
      New-Item -ItemType Directory -Force (Split-Path $target) | Out-Null
      Move-Item -Force $_.FullName $target
      Write-Host "[move] docs/docs/$rel -> docs/$rel"
    }
  }

  # Remove empty nested dirs
  Get-ChildItem -LiteralPath $nested -Recurse -Directory | Sort-Object FullName -Descending | ForEach-Object {
    if (-not (Get-ChildItem -LiteralPath $_.FullName -Force | Select-Object -First 1)) {
      Remove-Item -Force $_.FullName
    }
  }
  if (-not (Get-ChildItem -LiteralPath $nested -Force | Select-Object -First 1)) {
    Remove-Item -Force $nested
    Write-Host "[delete] removed empty docs/docs"
  }
} else {
  Write-Host "[ok] no docs/docs nesting found"
}

Write-Host "[done] cleanup complete. Rebuild with:"
Write-Host "       .\.venv\Scripts\python -m mkdocs build --strict"
