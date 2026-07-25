# Author:  Martin McBride
# Created: 2026-05-14
# Copyright (C) 2026, Martin McBride
# License: MIT

import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from pymusic.audiobuffer import read_wav
from pymusic.events import Events
from pymusic.tempfileutils import create_tempfile


@dataclass
class CSoundSequencer:
    instrument: str
    events: Events
    output_file: str
    bpm: float = 120
    sample_rate: int = 44100
    channels: int = 1

    def eventsToText(self, events: Events):
        strings = []
        for e in self.events:
            s = "i " + " ".join([str(p) for p in e.parameters])
            strings.append(s)

        return "\n".join(strings)



    def run(self):

        # Create a temporary csound file including the parameters
        instr_csd_file = str(Path(self.instrument))
        try:
            with open(instr_csd_file, 'r', encoding='utf-8') as f:
                csd_str = f.read()
        except:
            print(f"Error reading {instr_csd_file}")
            exit()

        try:
            temp_csd_file = create_tempfile(suffix=".csd")
            temp_csd_file.write(csd_str.format(score=self.eventsToText(self.events), sample_rate=self.sample_rate, channels=1, bpm=self.bpm))
            temp_csd_file.close()
        except:
            print(f"Error creating temp file")
            exit()

        # Build the Csound command
        cmd = [
            "csound",
            "-o", self.output_file,
            str(temp_csd_file.name)
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
            exit(0)
        except Exception as e:
            print("Error running CSound Sequencer...")
            print("Return code:", e.returncode)
