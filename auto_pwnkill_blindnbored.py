import logging
import subprocess
from pwnagotchi.plugins import BasePlugin

class AutoPwnKill(BasePlugin):
    __author__ = '5T3W'
    __version__ = '1.0.0'
    __license__ = 'MIT'
    __description__ = 'Automatically runs pwnkill when blind or bored counters reach 5.'

    def __init__(self):
        self.log = logging.getLogger(__name__)
        self.pwnkill_triggered = False  # To avoid repeated triggers

    def on_loaded(self):
        self.log.info("AutoPwnKill plugin loaded!")

    def on_epoch(self, agent, epoch_data):
        blind = agent.status.get('blind', 0)
        bored = agent.status.get('bored', 0)

        self.log.debug(f"Blind: {blind}, Bored: {bored}")

        # Check if either counter reaches 5 and pwnkill hasn't been triggered yet
        if (blind >= 5 or bored >= 5) and not self.pwnkill_triggered:
            self.log.info("Blind or Bored counter reached 5. Executing pwnkill!")
            self.run_pwnkill()
            self.pwnkill_triggered = True  # Prevent multiple executions in the same session

        # Reset the trigger when counters go below threshold
        if blind < 5 and bored < 5:
            self.pwnkill_triggered = False

    def run_pwnkill(self):
        try:
            subprocess.run(['pwnkill'], check=True)
            self.log.info("pwnkill command executed successfully.")
        except subprocess.CalledProcessError as e:
            self.log.error(f"Failed to execute pwnkill: {e}")
        except FileNotFoundError:
            self.log.error("pwnkill command not found. Is it installed and in your PATH?")