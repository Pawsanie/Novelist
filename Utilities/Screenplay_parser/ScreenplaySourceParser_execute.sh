#!/bin/bash
# Run Screenplay parser with shell Bash.
# Can get string argument with absolute path to scene configs folder.
# If have no arguments try to parse "ScreenPlay_source" folder`s files.

# Catching the path argument:
source_path="$1"

# Execute task:
if [ -n "$source_path" ]; then
    python3 -B -m "./Screenplay_Source_Parser.py" "$source_path"
else
    python3 -B -m "./Screenplay_Source_Parser.py"
fi

