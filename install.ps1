# Install the pack's coding-* skills for Claude Code.
#   .\install.ps1            install for every project (~\.claude\skills)
#   .\install.ps1 -Project   install into the current directory's .claude\skills
param([switch]$Project)

$ErrorActionPreference = 'Stop'

$sourceDir = Join-Path $PSScriptRoot 'dist\skills'
if ($Project) {
    $targetDir = Join-Path (Get-Location) '.claude\skills'
} else {
    $targetDir = Join-Path $HOME '.claude\skills'
}

if (-not (Test-Path $sourceDir)) {
    throw "install: $sourceDir not found; run 'python scripts/build_skills.py' first"
}

New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
foreach ($skill in Get-ChildItem -Directory -Path $sourceDir -Filter 'coding-*') {
    $destination = Join-Path $targetDir $skill.Name
    if (Test-Path $destination) {
        Remove-Item -Recurse -Force -Path $destination
    }
    Copy-Item -Recurse -Path $skill.FullName -Destination $destination
    Write-Output "installed $($skill.Name)"
}
Write-Output "Skills installed to $targetDir. Start a new Claude Code session to load them."
