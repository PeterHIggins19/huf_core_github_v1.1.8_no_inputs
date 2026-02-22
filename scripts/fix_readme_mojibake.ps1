param(
  [string]$Path = "README.md"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (!(Test-Path $Path)) {
  throw "File not found: $Path"
}

# Read as UTF-8, fix common mojibake sequences, write as UTF-8.
$txt = Get-Content $Path -Raw -Encoding utf8

$pairs = @(
  @("â€œ", '"'),
  @("â€", '"'),
  @("â€™", "'"),
  @("â€”", "--"),
  @("â†’", "->"),
  @("â€‘", "-"),
  @("Â·", "·")
)

foreach ($p in $pairs) {
  $txt = $txt.Replace($p[0], $p[1])
}

Set-Content -Path $Path -Value $txt -Encoding utf8
Write-Host "[ok] Fixed mojibake (UTF-8) in $Path"
