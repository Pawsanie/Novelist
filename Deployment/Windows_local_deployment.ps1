#!/usr/bin/env pwsh
#requires -Version 5.1
# Deploys a suitable local Python environment for Windows.

# Path settings:
$ScriptDir = Split-Path `
    -Parent $MyInvocation.MyCommand.Path

$TargetDir = @(
    $(
        Split-Path `
            -Parent $ScriptDir
    ),
    "Requirements",
    "Python"
) `
    -join "\"

# Python settings:
$PythonVersionFull = "3.13.15"
$PythonVersionShort = "3.13"
$PythonVersionFolder = "313"

$PythonExe = "$TargetDir\python-$PythonVersionFull-amd64.exe"

$PythonSigner = "Python Software Foundation"
$PythonFileSHA256 = "edec09c4853aeae9ac36efb8c9f95b6b8e2fee65eee56d9767a8b7c69c574403"

<#
.SYNOPSIS
Checks that the required version of Python is installed.
#>
function Test-Python-Existence {

    $Instance = $false

    foreach (
        $Path in @(
            "$Env:ProgramFiles\Python$($PythonVersionFolder)\python.exe",
            "$Env:LOCALAPPDATA\Programs\Python\Python$($PythonVersionFolder)\python.exe",
            "$Env:LOCALAPPDATA\Microsoft\WindowsApps\PythonSoftwareFoundation.$($PythonVersionShort)_qbz5n2kfra8p0\python.exe",
            "$TargetDir\python.exe"
        )
    ) {

        if (Test-Path $Path) {

            try {

                if (
                    (
                        & $Path `
                            -V
                    ) `
                    -eq "Python $($PythonVersionFull)"
                ) {

                    $Instance = $Path
                    break

                }

            }
            catch {

                continue

            }

        }

    }

    return $Instance

}

<#
.SYNOPSIS
Download Python from the official website and install it.
#>
function Get-Python {

    if (
        (Test-Path $PythonExe) `
        -and (
                (
                    Get-AuthenticodeSignature `
                        -FilePath $PythonExe
                ).Status `
                    -eq "Valid"
            ) `
        -and (
                (
                    Get-AuthenticodeSignature `
                        -FilePath $PythonExe
                ).SignerCertificate.Subject `
                    -like "*$PythonSigner*"
            ) `
        -and (
                (
                    Get-FileHash `
                        $PythonExe `
                        -Algorithm SHA256
                ).Hash.ToUpper() `
                    -eq $PythonFileSHA256.ToUpper()
        )
    ) {

        Write-Host `
            "Python.$PythonVersionFull installation file already exists...`n" `
            "File path: $PythonExe`n" `
            "No download required." `
            -ForegroundColor Blue

    }
    else {

        Write-Host `
            "Getting Python.$PythonVersionFull from the official website..." `
            -ForegroundColor Blue

        Invoke-WebRequest `
            -Uri "https://www.python.org/ftp/python/$PythonVersionFull/python-$PythonVersionFull-amd64.exe" `
            -OutFile $PythonExe

    }

    Write-Host `
        "Deploying Python..." `
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
                "Include_pip=1",
                "TargetDir=$TargetDir"
            ) `
                -join " "
        ) `
        -Wait `
        -NoNewWindow

}

<#
.SYNOPSIS
Deploys a suitable local Python environment for Windows.
#>
function Install-Python {

    if (
        !(Test-Path $TargetDir)
    ) {

        New-Item `
            -ItemType Directory `
            -Path $TargetDir `
            | Out-Null

    }

    if (
        $PythonEntity = Test-Python-Existence
    ) {

        Write-Host `
            "Creating a virtual environment from a local version of Python.$PythonVersionShort...`n" `
            "Base Path: $PythonEntity`n" `
            "Venv Path: $TargetDir\Scripts\python.exe" `
            -ForegroundColor Blue

        & $PythonEntity `
            -m venv `
            --copies `
            $TargetDir

    }
    else {

        Get-Python

        $Success = $true

        try {

            Write-Host `
            "Creating a Python virtual environment..." `
            "Venv Path: $TargetDir\Scripts\python.exe" `
            -ForegroundColor Blue

            & "$TargetDir\python.exe" `
                -m venv `
                --copies `
                $TargetDir

        }
        catch {

            $Success = $false

            Write-Host `
                "An error occurred during deployment...`n" `
                "It looks like you already had Python $PythonVersionFull installed and uninstalled incorrectly.`n" `
                "Try restoring the version from the installation file:`n" `
                "$TargetDir\python-$PythonVersionFull-amd64.exe`n" `
                "After that, re-run this script to complete the local deployment." `
                -ForegroundColor Red

        }

    }

    if (
        $PythonEntity `
        -or $Success
    ) {

        Write-Host `
            "Get Python requirements libs..." `
            -ForegroundColor Blue

        # Base:
        & "$TargetDir\python.exe" `
            -m pip install `
            -r "$ScriptDir\requirements.txt" `
            2>$null `
            | Out-Null

        # Venv:
        if ($LASTEXITCODE -ne 0) {

            & "$TargetDir\Scripts\python.exe" `
                -m pip install `
                -r "$ScriptDir\requirements.txt" `
                | Out-Null

        }

        if (
            (Test-Path $PythonExe)
        ) {

             Write-Host `
                "Removing the installation python.exe file..." `
                -ForegroundColor Blue

             Remove-Item $PythonExe

        }

        Write-Host `
            "The creation of a Python virtual environment has been successful!`n" `
            "Location: $TargetDir" `
            -ForegroundColor Green

    }

}

<#
.SYNOPSIS
Runs aaplication requirements deployment pipeline.
#>
function Main {

    Write-Host `
        "Application requirements deployment script has been launched."`
        -ForegroundColor Blue

    Install-Python

    Write-Host `
        "Application requirements deployment scenario completed." `
        -ForegroundColor Blue

}

# Entry point:
Main
