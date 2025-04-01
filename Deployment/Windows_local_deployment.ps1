#!/usr/bin/env pwsh
#requires -Version 5.1
# Deploys a suitable local Python environment for Windows.

# Path settings:
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TargetDir = @(
    $(Split-Path -Parent $ScriptDir),
    "Requirements",
    "Python"
) -join "\"
$PythonExe = "$TargetDir\python-3.10.11-amd64.exe"

function Check-Python-Existence {
    # Checks that the required version of Python is installed.
    $Instance = $false
    foreach (
    $Path in @(
            "$Env:ProgramFiles\Python310\python.exe",
            "$Env:LOCALAPPDATA\Programs\Python\Python310\python.exe",
            "$Env:LOCALAPPDATA\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.10_qbz5n2kfra8p0\python.exe"
        )
    ) {
        if (Test-Path $Path) {
            $Instance = $Path
            break
        }
    }
    return $Instance
}

function Get-Python {
    # Download Python from the official website and install it.
    Write-Host "Getting Python from the official website..." `
        -ForegroundColor Blue
    Invoke-WebRequest `
        -Uri "https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe" `
        -OutFile $PythonExe

    Write-Host "Deploying Python..." `
        -ForegroundColor Blue
    Start-Process `
        -FilePath $PythonExe `
        -ArgumentList $(
            @(
                "/quiet",
                "InstallAllUsers=0",
                "InstallLauncherAllUsers=0",
                "PrependPath=0",
                "Include_launcher=0",
                "TargetDir=$TargetDir"
            ) -join " "
        ) `
        -Wait `
        -NoNewWindow
}

function Execute {
    if (
        !(Test-Path $TargetDir)
    ) {
        New-Item `
            -ItemType Directory `
            -Path $TargetDir `
            | Out-Null
    }

    $PythonEntity = Check-Python-Existence
    if ($PythonEntity) {
        Write-Host "Creating a virtual environment from a local version of Python.3.10..." `
            -ForegroundColor Blue
        & $PythonEntity -m venv $TargetDir
    }
    else {
        Get-Python
        & "$TargetDir\python.exe" `
            -m venv `
            --copies $TargetDir `
            $TargetDir
    }

    try {
        $Success = $true
        Write-Host "Get requirements libs..." `
            -ForegroundColor Blue
        & "$TargetDir\Scripts\python.exe" `
            -m pip install `
            -r "$ScriptDir\requirements.txt" `
            | Out-Null
    }
    catch {
        $Success = $false
        Write-Host "An error occurred during deployment...`n" `
            "It looks like you already had Python 3.10.11 installed and uninstalled incorrectly.`n" `
            "Try restoring the version from the installation file:`n" `
            "$TargetDir\python-3.10.11-amd64.exe`n" `
            "After that, re-run this script to complete the local deployment." `
            -ForegroundColor Red
    }
    if ($Success) {
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
}

Execute