# Author:  Martin McBride
# Created: 2026-05-14
# Copyright (C) 2026, Martin McBride
# License: MIT

import subprocess
from dataclasses import dataclass
from pathlib import Path

from pymusic.events import Events


@dataclass
class CSoundSequencer:
    instrument: str
    events: Events

    def eventsToText(self, events: Events):
        strings = []
        for e in self.events:
            s = "i 1 " + " ".join([str(p) for p in e.parameters])
            strings.append(s)

        return "\n".join(strings)



    def run(self):
        # Path to .csd file
        csd_file = Path(self.instrument)

        # Output WAV file
        output_file = "output.wav"

        print("{{{" + self.eventsToText(self.events) + "}}}")

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

        except subprocess.CalledProcessError as e:
            print("Csound failed.")
            print("Return code:", e.returncode)
            print("Error output:")
            print(e.stderr)