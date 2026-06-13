# Author: Cruz Olli
$ErrorActionPreference = "Stop"
$src = Split-Path -Parent $MyInvocation.MyCommand.Path
$dest = Join-Path $HOME ".agents/skills/youtuber"
$parent = Split-Path -Parent $dest
New-Item -ItemType Directory -Force -Path $parent | Out-Null
if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
Copy-Item -Recurse -Force $src $dest
Write-Host "Installed youtuber skill to: $dest"
Write-Host "Invoke in Codex with: `$youtuber"
