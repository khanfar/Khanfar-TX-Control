#!/usr/bin/env python3
from rpitx_chirp import RpiTX, RadioConfig
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description='RpiTX Command Line Interface')
    
    # Basic parameters
    parser.add_argument('-f', '--frequency', type=float, required=True,
                       help='Center frequency in MHz (e.g., 145.500)')
    parser.add_argument('-m', '--modulation', choices=['FM', 'AM'], default='FM',
                       help='Modulation type (default: FM)')
    parser.add_argument('-p', '--power', type=float, default=1.0,
                       help='Power level 0.0-1.0 (default: 1.0)')
    parser.add_argument('-d', '--duration', type=float, default=1.0,
                       help='Duration of transmission in seconds (default: 1.0)')
    
    # Mode selection
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--tone', type=float, const=1000, nargs='?',
                          help='Generate tone signal (frequency in Hz, default: 1000)')
    mode_group.add_argument('--chirp', action='store_true',
                          help='Generate chirp signal')
    mode_group.add_argument('--morse', type=str,
                          help='Transmit morse code message')
    mode_group.add_argument('--rtty', type=str,
                          help='Transmit RTTY message')
    mode_group.add_argument('--sstv', type=str,
                          help='Transmit SSTV image (specify image path)')
    mode_group.add_argument('--pocsag', type=str,
                          help='Transmit POCSAG pager message')
    mode_group.add_argument('--opera', type=str,
                          help='Transmit Opera beacon (specify callsign)')
    mode_group.add_argument('--ft8', type=str,
                          help='Transmit FT8 message')
    mode_group.add_argument('--spectrum', type=str,
                          help='Transmit spectrum from image (specify image path)')
    
    # Mode-specific parameters
    parser.add_argument('-s', '--sweep', type=float, default=6.0,
                       help='Frequency sweep range in MHz for chirp (default: 6.0)')
    parser.add_argument('--wpm', type=int, default=20,
                       help='Words per minute for morse code (default: 20)')
    parser.add_argument('--baud', type=int, default=45,
                       help='Baud rate for RTTY (default: 45)')
    parser.add_argument('--sstv-mode', type=str, default="Martin1",
                       choices=["Martin1", "Martin2", "Scottie1", "Scottie2"],
                       help='SSTV mode (default: Martin1)')
    parser.add_argument('--callsign', type=str, default="N0CALL",
                       help='Callsign for FT8/Opera (default: N0CALL)')
    parser.add_argument('--grid', type=str,
                       help='Grid locator for Opera beacon')
    
    args = parser.parse_args()
    
    try:
        radio = RpiTX()
        config = RadioConfig(
            frequency=int(args.frequency * 1e6),  # Convert MHz to Hz
            modulation=args.modulation,
            power=args.power,
            bandwidth=int(args.sweep * 1e6) if args.chirp else 12500,
            name="CLI Transmission"
        )
        radio.current_config = config
        
        # Handle different transmission modes
        if args.chirp:
            sweep_hz = args.sweep * 1e6  # Convert MHz to Hz
            print(f"Generating {args.duration}s chirp signal at {args.frequency}MHz")
            print(f"Sweeping ±{args.sweep/2}MHz (total {args.sweep}MHz)")
            radio.transmit_chirp(args.duration, sweep_hz)
            
        elif args.tone is not None:
            print(f"Generating {args.duration}s tone at {args.frequency}MHz using {args.modulation}")
            print(f"Tone frequency: {args.tone}Hz")
            radio.transmit_tone(args.duration, args.tone)
            
        elif args.morse:
            print(f"Transmitting morse code at {args.frequency}MHz")
            print(f"Message: {args.morse}")
            radio.transmit_morse(args.morse, args.wpm)
            
        elif args.rtty:
            print(f"Transmitting RTTY at {args.frequency}MHz")
            print(f"Message: {args.rtty}")
            radio.transmit_rtty(args.rtty, args.baud)
            
        elif args.sstv:
            print(f"Transmitting SSTV image at {args.frequency}MHz")
            print(f"Image: {args.sstv}")
            radio.transmit_sstv(args.sstv, args.sstv_mode)
            
        elif args.pocsag:
            print(f"Transmitting POCSAG message at {args.frequency}MHz")
            print(f"Message: {args.pocsag}")
            radio.transmit_pocsag(args.pocsag)
            
        elif args.opera:
            print(f"Transmitting Opera beacon at {args.frequency}MHz")
            print(f"Callsign: {args.opera}")
            radio.transmit_opera(args.opera, args.grid)
            
        elif args.ft8:
            print(f"Transmitting FT8 at {args.frequency}MHz")
            print(f"Message: {args.ft8}")
            radio.transmit_ft8(args.ft8, args.callsign)
            
        elif args.spectrum:
            print(f"Transmitting spectrum image at {args.frequency}MHz")
            print(f"Image: {args.spectrum}")
            radio.transmit_spectrum(args.spectrum)
            
        print("Transmission complete")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
