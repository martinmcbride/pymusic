# Author:  Martin McBride
# Created: 2026-05-14
# Copyright (C) 2026, Martin McBride
# License: MIT

import subprocess
from pathlib import Path

# Path to your .csd file
csd_file = Path("simple_piano.csd")

# Optional output WAV file
output_file = "output.wav"

# Build the Csound command
cmd = [
    "csound",
    "-o", output_file,
    str(csd_file)
]

try:
    # Run Csound
    result = subprocess.run(
        cmd,
        check=True,
        capture_output=True,
        text=True
    )

    print("Csound completed successfully.")
    print(result.stdout)

except subprocess.CalledProcessError as e:
    print("Csound failed.")
    print("Return code:", e.returncode)
    print("Error output:")
    print(e.stderr)