param(
  [string]$Path = "README.md"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (!(Test-Path -LiteralPath $Path)) {
  throw "File not found: $Path"
}

# --- Helpers ---
function FixOnceCp1252ToUtf8([string]$s) {
  # If UTF-8 bytes were decoded as CP1252 (e.g., â€œ), this reverses it.
  $enc1252 = [System.Text.Encoding]::GetEncoding(1252)
  $bytes = $enc1252.GetBytes($s)
  return [System.Text.Encoding]::UTF8.GetString($bytes)
}

# --- Read file ---
# Read as UTF-8 (works for most cases). If anything goes wrong, fall back to CP1252.
try {
  $txt = Get-Content -LiteralPath $Path -Raw -Encoding utf8
} catch {
  $txt = [System.IO.File]::ReadAllText((Resolve-Path -LiteralPath $Path), [System.Text.Encoding]::GetEncoding(1252))
}

# --- Unmangle up to 2 times (handles double-encoding like Ã¢â‚¬Å“) ---
for ($i = 0; $i -lt 2; $i++) {
  if ($txt -match "Ã|Â|â") {
    $fixed = FixOnceCp1252ToUtf8 $txt
    if ($fixed -eq $txt) { break }
    $txt = $fixed
  } else {
    break
  }
}

# --- Normalize punctuation to ASCII (prevents future mojibake) ---
# Curly quotes / apostrophes
$txt = $txt.Replace([string][char]0x201C, '"')  # “
$txt = $txt.Replace([string][char]0x201D, '"')  # ”
$txt = $txt.Replace([string][char]0x2018, "'")  # ‘
$txt = $txt.Replace([string][char]0x2019, "'")  # ’

# Dashes / hyphens
$txt = $txt.Replace([string][char]0x2014, "--") # —
$txt = $txt.Replace([string][char]0x2013, "-")  # –
$txt = $txt.Replace([string][char]0x2011, "-")  # ‑ (non-breaking hyphen)

# Arrow
$txt = $txt.Replace([string][char]0x2192, "->")  # →

# Middle dot (keep as-is)
$txt = $txt.Replace([string][char]0x00B7, "·")   # ·

# --- Save as UTF-8 ---
Set-Content -LiteralPath $Path -Value $txt -Encoding utf8
Write-Host "[ok] Normalized README encoding/punctuation in $Path (UTF-8)"
