param(
  [string]$Path = "README.md"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (!(Test-Path -LiteralPath $Path)) {
  throw "File not found: $Path"
}

function StrFromCodes([int[]]$codes) {
  $sb = New-Object System.Text.StringBuilder
  foreach ($c in $codes) { [void]$sb.Append([char]$c) }
  return $sb.ToString()
}

function Fix-Once([string]$s) {
  # Attempt to "unmangle" common double-encoding:
  # Treat current Unicode text as ISO-8859-1 bytes, decode as UTF-8.
  $encLatin1 = [System.Text.Encoding]::GetEncoding(28591) # ISO-8859-1
  $bytes = $encLatin1.GetBytes($s)
  return [System.Text.Encoding]::UTF8.GetString($bytes)
}

# Read as UTF-8; if it fails, read as Windows-1252.
try {
  $txt = Get-Content -LiteralPath $Path -Raw -Encoding utf8
} catch {
  $txt = [System.IO.File]::ReadAllText((Resolve-Path -LiteralPath $Path), [System.Text.Encoding]::GetEncoding(1252))
}

# If it looks double-encoded (contains "Ã" etc), try to fix up to 2 times.
for ($i=0; $i -lt 2; $i++) {
  if ($txt -match "Ã|Â|â") {
    $fixed = Fix-Once $txt
    if ($fixed -eq $txt) { break }
    $txt = $fixed
  } else {
    break
  }
}

# Build common mojibake sequences from code points (ASCII-only script file).
$A_LQ = StrFromCodes @(0x00E2,0x20AC,0x0153)  # â€œ
$A_RQ = StrFromCodes @(0x00E2,0x20AC,0x009D)  # â€ (0x9D)
$A_RS = StrFromCodes @(0x00E2,0x20AC,0x2122)  # â€™
$A_MD = StrFromCodes @(0x00E2,0x20AC,0x201D)  # â€” (often)
$A_AR = StrFromCodes @(0x00E2,0x2020,0x2019)  # â†’
$A_HY = StrFromCodes @(0x00E2,0x20AC,0x2018)  # â€‘
$A_MD2 = StrFromCodes @(0x00E2,0x20AC,0x2014) # sometimes em dash variant
$A_DOT = StrFromCodes @(0x00C2,0x00B7)        # Â·

$pairs = @(
  @($A_LQ, '"'),
  @($A_RQ, '"'),
  @($A_RS, "'"),
  @($A_MD, "--"),
  @($A_MD2, "--"),
  @($A_AR, "->"),
  @($A_HY, "-"),
  @($A_DOT, "·")
)

foreach ($p in $pairs) {
  $from = $p[0]; $to = $p[1]
  if ($from -and $txt.Contains($from)) { $txt = $txt.Replace($from, $to) }
}

# Normalize real Unicode punctuation to ASCII (helps avoid future mojibake).
$txt = $txt.Replace([string][char]0x201C, '"') `
           .Replace([string][char]0x201D, '"') `
           .Replace([string][char]0x2018, "'") `
           .Replace([string][char]0x2019, "'") `
           .Replace([string][char]0x2014, "--") `
           .Replace([string][char]0x2192, "->") `
           .Replace([string][char]0x2011, "-")

Set-Content -LiteralPath $Path -Value $txt -Encoding utf8
Write-Host "[ok] Normalized README encoding/punctuation in $Path (UTF-8)"
