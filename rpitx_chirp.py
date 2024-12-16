#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import time
import math
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class RadioConfig:
    frequency: int  # in Hz
    modulation: str  # FM, AM, etc
    power: float  # 0-1.0
    bandwidth: int  # in Hz
    name: str
    description: str = ""

class RpiTX:
    def __init__(self):
        self.configs: List[RadioConfig] = []
        self.current_config: Optional[RadioConfig] = None
        
    def add_config(self, config: RadioConfig):
        """Add a new radio configuration"""
        self.configs.append(config)
        
    def transmit_chirp(self, duration: float, bandwidth: float):
        """Transmit chirp signal using native rpitx"""
        if not self.current_config:
            raise Exception("No radio configuration set")
            
        cmd = f"pichirp {self.current_config.frequency} {int(bandwidth)} {duration}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"pichirp error: {result.stderr}")
            
    def transmit_tone(self, duration: float, tone_freq: float):
        """Transmit tone using sendiq"""
        if not self.current_config:
            raise Exception("No radio configuration set")
            
        cmd = f"sendiq -f {self.current_config.frequency} -t {duration} -s 48000"
        if self.current_config.power != 1.0:
            cmd += f" -a {self.current_config.power}"
            
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"sendiq error: {result.stderr}")
            
    def transmit_morse(self, text: str, wpm: int = 20):
        """Transmit morse code"""
        if not self.current_config:
            raise Exception("No radio configuration set")
            
        cmd = f"morse {self.current_config.frequency} {text} {wpm}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"morse error: {result.stderr}")
            
    def transmit_rtty(self, text: str, baud: int = 45):
        """Transmit RTTY"""
        if not self.current_config:
            raise Exception("No radio configuration set")
            
        cmd = f"pirtty {self.current_config.frequency} {text} {baud}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"pirtty error: {result.stderr}")
            
    def transmit_sstv(self, image_path: str, mode: str = "Martin1"):
        """Transmit SSTV image"""
        if not self.current_config:
            raise Exception("No radio configuration set")
            
        cmd = f"pisstv {self.current_config.frequency} {image_path} {mode}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"pisstv error: {result.stderr}")
            
    def transmit_pocsag(self, message: str, bitrate: int = 1200):
        """Transmit POCSAG pager message"""
        if not self.current_config:
            raise Exception("No radio configuration set")
            
        cmd = f"pocsag {self.current_config.frequency} {message} {bitrate}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"pocsag error: {result.stderr}")
            
    def transmit_opera(self, callsign: str, locator: str = ""):
        """Transmit Opera beacon"""
        if not self.current_config:
            raise Exception("No radio configuration set")
            
        cmd = f"piopera {self.current_config.frequency} {callsign}"
        if locator:
            cmd += f" {locator}"
            
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"piopera error: {result.stderr}")
            
    def transmit_ft8(self, message: str, callsign: str):
        """Transmit FT8 digital mode"""
        if not self.current_config:
            raise Exception("No radio configuration set")
            
        cmd = f"pift8 {self.current_config.frequency} {callsign} {message}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"pift8 error: {result.stderr}")
            
    def transmit_spectrum(self, image_path: str):
        """Transmit spectrum from image"""
        if not self.current_config:
            raise Exception("No radio configuration set")
            
        cmd = f"spectrumpaint {self.current_config.frequency} {image_path}"
        result = subprocess.run(cmd.split(), capture_output=True, text=True)
        if result.returncode != 0:
            raise Exception(f"spectrumpaint error: {result.stderr}")
            
    def set_frequency(self, freq_hz: int):
        """Set transmission frequency in Hz"""
        if self.current_config:
            self.current_config.frequency = freq_hz
            
    def set_modulation(self, mod: str):
        """Set modulation type (FM, AM, etc)"""
        if self.current_config:
            self.current_config.modulation = mod
            
    def save_config(self, filename: str):
        """Save radio configurations to file"""
        with open(filename, "w") as f:
            json.dump([vars(c) for c in self.configs], f, indent=2)
            
    def load_config(self, filename: str):
        """Load radio configurations from file"""
        with open(filename) as f:
            configs = json.load(f)
            self.configs = [RadioConfig(**c) for c in configs]
            
def main():
    # Example usage
    radio = RpiTX()
    
    # Create some example configurations
    configs = [
        RadioConfig(
            frequency=145500000,  # 145.5 MHz
            modulation="FM",
            power=0.5,
            bandwidth=12500,
            name="2m Amateur Band",
            description="2 meter ham radio band"
        ),
        RadioConfig(
            frequency=433920000,  # 433.92 MHz
            modulation="AM",
            power=0.3,
            bandwidth=25000,
            name="433 ISM Band",
            description="ISM band frequency"
        )
    ]
    
    for config in configs:
        radio.add_config(config)
    
    # Save configurations
    radio.save_config("radio_configs.json")
    
    # Example transmission
    radio.current_config = configs[0]  # Use first config
    radio.set_frequency(145500000)
    
    # Transmit chirp
    radio.transmit_chirp(1.0, 10000)
    
    # Transmit tone
    radio.transmit_tone(1.0, 1000)
    
    # Transmit morse code
    radio.transmit_morse("Hello World")
    
    # Transmit RTTY
    radio.transmit_rtty("Hello World")
    
    # Transmit SSTV image
    radio.transmit_sstv("image.jpg")
    
    # Transmit POCSAG pager message
    radio.transmit_pocsag("Hello World")
    
    # Transmit Opera beacon
    radio.transmit_opera("N0CALL")
    
    # Transmit FT8 digital mode
    radio.transmit_ft8("Hello World", "N0CALL")
    
    # Transmit spectrum from image
    radio.transmit_spectrum("image.jpg")

if __name__ == "__main__":
    main()
