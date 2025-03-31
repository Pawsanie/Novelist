#!/usr/bin/env pwsh
#requires -Version 5.1
# Continues to deploy a proper Python environment for Windows
# after problems with incorrect installation in the past.

# Path settings:
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetDir = @(
    $(
        Split-Path -Parent `
        $(Split-Path -Parent $ScriptDir)
    ),
    "Requirements",
    "Python"
) -join "\"
$PythonExe = "$TargetDir\python-3.10.11-amd64.exe"

function Execute {
    Write-Host "Creating a virtual environment from a local version of Python.3.10..." `
        -ForegroundColor Blue
    & "$TargetDir\python.exe" `
            -m venv `
            --copies $TargetDir `
            $TargetDir

    Write-Host "Get requirements libs..." `
        -ForegroundColor Blue
    & "$TargetDir\Scripts\python.exe" `
        -m pip install `
        -r "$(Split-Path -Parent $ScriptDir)\requirements.txt" `
        | Out-Null

    if (
        (Test-Path $PythonExe)
    ) {
         Write-Host "Removing the installation python.exe file..." `
            -ForegroundColor Blue
         Remove-Item $PythonExe
    }

    Write-Host "The creation of a Python virtual environment has been successful!`n" `
        "Location: $TargetDir" `
        -ForegroundColor Green

}

Execute