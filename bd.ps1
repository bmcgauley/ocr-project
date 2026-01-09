# Wrapper script for bd (beads) command
# Usage: ./bd.ps1 <command> <args>
# Example: ./bd.ps1 status

$bdPath = Join-Path $PSScriptRoot "bin\bd.exe"

if (-not (Test-Path $bdPath)) {
    Write-Host "Error: bd.exe not found at $bdPath" -ForegroundColor Red
    Write-Host "Please run setup script first" -ForegroundColor Yellow
    exit 1
}

& $bdPath $args
