# Khanfar-TX Control

A comprehensive Python-based interface for controlling RF transmission using the rpitx project. Features both GUI and CLI interfaces with support for multiple transmission modes.

**Developed by Khanfar Systems**

## Features

### Basic Transmission
- Tone generation with frequency control
- Chirp signals with sweep control
- Multiple modulation modes (FM, AM, USB, LSB)
- Power level control
- Frequency control (VHF/UHF ranges)
- Memory channel management

### Digital Modes
- Morse Code (with WPM control)
- RTTY (Radio Teletype)
- POCSAG pager messages
- Opera beacon mode
- FT8 digital mode

### Image Transmission
- SSTV (Slow Scan TV) with multiple modes:
  - Martin 1 & 2
  - Scottie 1 & 2
- Spectrum painting from images

## Requirements

- Raspberry Pi (2, 3, or 4 recommended)
- rpitx installed and configured
- Python 3.7 or higher
- Required Python packages (see requirements.txt)

## Installation

1. Install rpitx following the main project instructions
2. Install Python dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
3. Make the Python scripts executable:
   ```bash
   chmod +x rpitx_gui.py
   chmod +x rpitx_cli.py
   chmod +x rpitx_chirp.py
   ```

## Usage

### GUI Interface

1. Start the GUI:
   ```bash
   ./rpitx_gui.py
   ```

2. Basic Tab:
   - Set frequency in MHz (e.g., 145.500)
   - Choose signal type (Tone or Chirp)
   - Select modulation type
   - Adjust power level
   - Set duration and signal parameters
   - Click "Transmit"

3. Digital Tab:
   - Select digital mode
   - Enter message
   - Configure mode-specific parameters
   - Click "Transmit"

4. Image Tab:
   - Choose SSTV or Spectrum mode
   - Select image file
   - Configure SSTV mode if applicable
   - Click "Transmit"

5. Memory Tab:
   - Add current settings to memory
   - Load saved channels
   - Remove unused channels

### CLI Interface

The CLI tool supports all transmission modes with the following commands:

1. Basic Transmission:
   ```bash
   # Tone transmission
   ./rpitx_cli.py --freq 145.500 --mode tone --tone-freq 1000 --duration 5
   
   # Chirp transmission
   ./rpitx_cli.py --freq 145.500 --mode chirp --sweep 6.0 --duration 5
   ```

2. Digital Modes:
   ```bash
   # Morse Code
   ./rpitx_cli.py --freq 145.500 --mode morse --message "CQ CQ" --wpm 20
   
   # RTTY
   ./rpitx_cli.py --freq 145.500 --mode rtty --message "TEST" --baud 45
   
   # POCSAG
   ./rpitx_cli.py --freq 145.500 --mode pocsag --message "Alert!"
   
   # Opera
   ./rpitx_cli.py --freq 145.500 --mode opera --callsign "N0CALL" --grid "JO01"
   
   # FT8
   ./rpitx_cli.py --freq 145.500 --mode ft8 --message "CQ N0CALL JO01"
   ```

3. Image Transmission:
   ```bash
   # SSTV
   ./rpitx_cli.py --freq 145.500 --mode sstv --image path/to/image.jpg --sstv-mode Martin1
   
   # Spectrum
   ./rpitx_cli.py --freq 145.500 --mode spectrum --image path/to/image.jpg
   ```

Common Options:
- `--freq`: Frequency in MHz
- `--power`: Power level (0.0 to 1.0)
- `--mod`: Modulation type (FM, AM, USB, LSB)
- `--duration`: Transmission duration in seconds
you can test directly : sudo ./pichirp 464210000 600000 10
## Warning

Make sure you have the appropriate licenses and permissions before transmitting. Only transmit on frequencies you are authorized to use.

## License

This project is licensed under the same terms as rpitx.
