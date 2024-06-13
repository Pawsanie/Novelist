# Run Screenplay parser with shell PowerShell.
# Can get string argument with absolute path to scene configs folder.
# If have no arguments try to parse "ScreenPlay_source" folder`s files.

# Catching the path argument:
param (
    [string]$source_path
)

# Create task:
if ($source_path) {
    $parser_task = "python3 $PSScriptRoot\Screenplay_Source_Parser.py $source_path"
} else {
    $parser_task = "python3 $PSScriptRoot\Screenplay_Source_Parser.py"
}

# Execute:
Invoke-Expression $parser_task