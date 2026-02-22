param(
  [string]$Path = "docs\field_guide.md",
  [string]$Id   = "2-origin-story-wavefront-control--audit-layers"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (!(Test-Path -LiteralPath $Path)) {
  throw "File not found: $Path"
}

$txt = Get-Content -LiteralPath $Path -Raw -Encoding utf8

# If the file already contains the explicit heading id, we're done.
if ($txt -match [regex]::Escape("{#$Id}")) {
  Write-Host "[ok] Heading id already present: {#$Id}"
  exit 0
}

# Find a heading line that contains "Origin story" (level 2+ heading).
$re = [regex]"(?m)^(#+\s*(?:\d+[\.\)]\s*)?Origin story[^\r\n]*)$"
$m = $re.Match($txt)

if (!$m.Success) {
  Write-Host "[warn] Could not find an 'Origin story' heading in $Path."
  Write-Host "       Add this to your intended heading manually: {#$Id}"
  exit 1
}

$line = $m.Groups[1].Value

# If the heading already has an attribute list, append the id inside it.
if ($line -match "\{[^}]*\}$") {
  # Insert before closing brace
  $newLine = $line -replace "\}$", " #$Id}"
} else {
  $newLine = $line + " {#$Id}"
}

$txt2 = $txt.Substring(0, $m.Index) + $newLine + $txt.Substring($m.Index + $m.Length)

Set-Content -LiteralPath $Path -Value $txt2 -Encoding utf8
Write-Host "[ok] Added explicit heading id to Origin story: {#$Id}"
Write-Host "     Re-run: .\.venv\Scripts\python -m mkdocs build --strict"
