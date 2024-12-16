#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from rpitx_chirp import RpiTX, RadioConfig

class RpiTXGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Khanfar-TX Control - Developed by Khanfar Systems")
        self.radio = RpiTX()
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.basic_frame = ttk.Frame(self.notebook)
        self.digital_frame = ttk.Frame(self.notebook)
        self.image_frame = ttk.Frame(self.notebook)
        self.memory_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.basic_frame, text='Basic')
        self.notebook.add(self.digital_frame, text='Digital')
        self.notebook.add(self.image_frame, text='Image')
        self.notebook.add(self.memory_frame, text='Memory')
        
        # Setup each tab
        self.setup_basic_tab()
        self.setup_digital_tab()
        self.setup_image_tab()
        self.setup_memory_tab()
        
        # Load saved configurations
        try:
            self.radio.load_config("radio_configs.json")
            self.update_channel_list()
        except:
            pass
            
    def setup_basic_tab(self):
        """Setup basic transmission controls"""
        frame = self.basic_frame
        
        # Frequency control
        ttk.Label(frame, text="Frequency (MHz):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.freq_var = tk.StringVar(value="464.210")
        self.freq_entry = ttk.Entry(frame, textvariable=self.freq_var)
        self.freq_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Signal Type
        ttk.Label(frame, text="Signal Type:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.signal_var = tk.StringVar(value="Tone")
        signal_combo = ttk.Combobox(frame, textvariable=self.signal_var)
        signal_combo['values'] = ('Tone', 'Chirp')
        signal_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        signal_combo.bind('<<ComboboxSelected>>', self.on_signal_change)
        
        # Modulation control
        ttk.Label(frame, text="Modulation:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.mod_var = tk.StringVar(value="FM")
        mod_combo = ttk.Combobox(frame, textvariable=self.mod_var)
        mod_combo['values'] = ('FM', 'AM', 'USB', 'LSB')
        mod_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Power control
        ttk.Label(frame, text="Power:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.power_var = tk.DoubleVar(value=1.0)
        power_scale = ttk.Scale(frame, from_=0, to=1, variable=self.power_var, orient=tk.HORIZONTAL)
        power_scale.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Duration control
        ttk.Label(frame, text="Duration (s):").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.duration_var = tk.StringVar(value="1.0")
        duration_entry = ttk.Entry(frame, textvariable=self.duration_var)
        duration_entry.grid(row=4, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Parameters Frame
        self.params_frame = ttk.LabelFrame(frame, text="Signal Parameters", padding="5")
        self.params_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Tone frequency
        self.tone_label = ttk.Label(self.params_frame, text="Tone (Hz):")
        self.tone_label.grid(row=0, column=0, sticky=tk.W)
        self.tone_var = tk.StringVar(value="1000")
        self.tone_entry = ttk.Entry(self.params_frame, textvariable=self.tone_var)
        self.tone_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Sweep range (initially hidden)
        self.sweep_label = ttk.Label(self.params_frame, text="Sweep (MHz):")
        self.sweep_var = tk.StringVar(value="6.0")
        self.sweep_entry = ttk.Entry(self.params_frame, textvariable=self.sweep_var)
        
        # Transmit button
        ttk.Button(frame, text="Transmit", command=self.transmit_basic).grid(row=6, column=0, columnspan=2, pady=10)
        
    def setup_digital_tab(self):
        """Setup digital mode controls"""
        frame = self.digital_frame
        
        # Mode selection
        ttk.Label(frame, text="Digital Mode:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.digital_mode_var = tk.StringVar(value="Morse")
        mode_combo = ttk.Combobox(frame, textvariable=self.digital_mode_var)
        mode_combo['values'] = ('Morse', 'RTTY', 'POCSAG', 'Opera', 'FT8')
        mode_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        mode_combo.bind('<<ComboboxSelected>>', self.on_digital_mode_change)
        
        # Message entry
        ttk.Label(frame, text="Message:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.message_var = tk.StringVar()
        message_entry = ttk.Entry(frame, textvariable=self.message_var)
        message_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        
        # Parameters Frame
        self.digital_params_frame = ttk.LabelFrame(frame, text="Mode Parameters", padding="5")
        self.digital_params_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        # Morse WPM
        self.wpm_label = ttk.Label(self.digital_params_frame, text="WPM:")
        self.wpm_var = tk.StringVar(value="20")
        self.wpm_entry = ttk.Entry(self.digital_params_frame, textvariable=self.wpm_var)
        
        # RTTY Baud
        self.baud_label = ttk.Label(self.digital_params_frame, text="Baud:")
        self.baud_var = tk.StringVar(value="45")
        self.baud_entry = ttk.Entry(self.digital_params_frame, textvariable=self.baud_var)
        
        # Callsign
        self.callsign_label = ttk.Label(self.digital_params_frame, text="Callsign:")
        self.callsign_var = tk.StringVar(value="N0CALL")
        self.callsign_entry = ttk.Entry(self.digital_params_frame, textvariable=self.callsign_var)
        
        # Grid locator
        self.grid_label = ttk.Label(self.digital_params_frame, text="Grid:")
        self.grid_var = tk.StringVar()
        self.grid_entry = ttk.Entry(self.digital_params_frame, textvariable=self.grid_var)
        
        # Show initial morse parameters
        self.wpm_label.grid(row=0, column=0, sticky=tk.W)
        self.wpm_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Transmit button
        ttk.Button(frame, text="Transmit", command=self.transmit_digital).grid(row=3, column=0, columnspan=2, pady=10)
        
    def setup_image_tab(self):
        """Setup image transmission controls"""
        frame = self.image_frame
        
        # Mode selection
        ttk.Label(frame, text="Image Mode:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.image_mode_var = tk.StringVar(value="SSTV")
        mode_combo = ttk.Combobox(frame, textvariable=self.image_mode_var)
        mode_combo['values'] = ('SSTV', 'Spectrum')
        mode_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        mode_combo.bind('<<ComboboxSelected>>', self.on_image_mode_change)
        
        # Image selection
        ttk.Label(frame, text="Image:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.image_path_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.image_path_var).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(frame, text="Browse", command=self.browse_image).grid(row=1, column=2)
        
        # SSTV mode selection
        self.sstv_frame = ttk.LabelFrame(frame, text="SSTV Parameters", padding="5")
        self.sstv_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5, padx=5)
        
        ttk.Label(self.sstv_frame, text="Mode:").grid(row=0, column=0, sticky=tk.W)
        self.sstv_mode_var = tk.StringVar(value="Martin1")
        sstv_combo = ttk.Combobox(self.sstv_frame, textvariable=self.sstv_mode_var)
        sstv_combo['values'] = ('Martin1', 'Martin2', 'Scottie1', 'Scottie2')
        sstv_combo.grid(row=0, column=1, sticky=(tk.W, tk.E))
        
        # Transmit button
        ttk.Button(frame, text="Transmit", command=self.transmit_image).grid(row=3, column=0, columnspan=3, pady=10)
        
    def setup_memory_tab(self):
        """Setup memory channel controls"""
        frame = self.memory_frame
        
        # Channel list
        ttk.Label(frame, text="Memory Channels:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.channel_list = tk.Listbox(frame, height=10)
        self.channel_list.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=5)
        self.channel_list.bind('<<ListboxSelect>>', self.on_channel_select)
        
        # Buttons
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Add Channel", command=self.add_channel).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Channel", command=self.remove_channel).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Channel", command=self.load_channel).pack(side=tk.LEFT, padx=5)
        
    def on_signal_change(self, event=None):
        """Handle signal type change"""
        if self.signal_var.get() == "Chirp":
            self.tone_label.grid_remove()
            self.tone_entry.grid_remove()
            self.sweep_label.grid(row=0, column=0, sticky=tk.W)
            self.sweep_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        else:
            self.sweep_label.grid_remove()
            self.sweep_entry.grid_remove()
            self.tone_label.grid(row=0, column=0, sticky=tk.W)
            self.tone_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
            
    def on_digital_mode_change(self, event=None):
        """Handle digital mode change"""
        # Clear all parameters
        for widget in self.digital_params_frame.grid_slaves():
            widget.grid_remove()
            
        mode = self.digital_mode_var.get()
        if mode == "Morse":
            self.wpm_label.grid(row=0, column=0, sticky=tk.W)
            self.wpm_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        elif mode == "RTTY":
            self.baud_label.grid(row=0, column=0, sticky=tk.W)
            self.baud_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
        elif mode in ("Opera", "FT8"):
            self.callsign_label.grid(row=0, column=0, sticky=tk.W)
            self.callsign_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))
            if mode == "Opera":
                self.grid_label.grid(row=1, column=0, sticky=tk.W)
                self.grid_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))
                
    def on_image_mode_change(self, event=None):
        """Handle image mode change"""
        if self.image_mode_var.get() == "SSTV":
            self.sstv_frame.grid()
        else:
            self.sstv_frame.grid_remove()
            
    def browse_image(self):
        """Open file dialog to select image"""
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if filename:
            self.image_path_var.set(filename)
            
    def transmit_basic(self):
        """Handle basic transmission"""
        try:
            freq = float(self.freq_var.get()) * 1e6
            duration = float(self.duration_var.get())
            
            config = RadioConfig(
                frequency=int(freq),
                modulation=self.mod_var.get(),
                power=self.power_var.get(),
                bandwidth=12500,
                name="GUI Transmission"
            )
            self.radio.current_config = config
            
            if self.signal_var.get() == "Chirp":
                sweep = float(self.sweep_var.get()) * 1e6
                print(f"Transmitting {duration}s chirp at {freq/1e6:.3f}MHz")
                print(f"Sweeping ±{float(self.sweep_var.get())/2}MHz")
                self.radio.transmit_chirp(duration, sweep)
            else:
                tone = float(self.tone_var.get())
                print(f"Transmitting {duration}s tone at {freq/1e6:.3f}MHz")
                print(f"Tone frequency: {tone}Hz")
                self.radio.transmit_tone(duration, tone)
                
        except Exception as e:
            messagebox.showerror("Error", f"Transmission failed: {str(e)}")
            
    def transmit_digital(self):
        """Handle digital mode transmission"""
        try:
            freq = float(self.freq_var.get()) * 1e6
            message = self.message_var.get()
            
            if not message:
                messagebox.showerror("Error", "Please enter a message")
                return
                
            config = RadioConfig(
                frequency=int(freq),
                modulation=self.mod_var.get(),
                power=self.power_var.get(),
                bandwidth=12500,
                name="Digital Transmission"
            )
            self.radio.current_config = config
            
            mode = self.digital_mode_var.get()
            if mode == "Morse":
                wpm = int(self.wpm_var.get())
                self.radio.transmit_morse(message, wpm)
            elif mode == "RTTY":
                baud = int(self.baud_var.get())
                self.radio.transmit_rtty(message, baud)
            elif mode == "POCSAG":
                self.radio.transmit_pocsag(message)
            elif mode == "Opera":
                callsign = self.callsign_var.get()
                grid = self.grid_var.get()
                self.radio.transmit_opera(callsign, grid)
            elif mode == "FT8":
                callsign = self.callsign_var.get()
                self.radio.transmit_ft8(message, callsign)
                
        except Exception as e:
            messagebox.showerror("Error", f"Transmission failed: {str(e)}")
            
    def transmit_image(self):
        """Handle image transmission"""
        try:
            freq = float(self.freq_var.get()) * 1e6
            image_path = self.image_path_var.get()
            
            if not image_path:
                messagebox.showerror("Error", "Please select an image")
                return
                
            config = RadioConfig(
                frequency=int(freq),
                modulation=self.mod_var.get(),
                power=self.power_var.get(),
                bandwidth=12500,
                name="Image Transmission"
            )
            self.radio.current_config = config
            
            mode = self.image_mode_var.get()
            if mode == "SSTV":
                sstv_mode = self.sstv_mode_var.get()
                self.radio.transmit_sstv(image_path, sstv_mode)
            else:  # Spectrum
                self.radio.transmit_spectrum(image_path)
                
        except Exception as e:
            messagebox.showerror("Error", f"Transmission failed: {str(e)}")
            
    def add_channel(self):
        """Add current settings as a new channel"""
        try:
            freq = float(self.freq_var.get()) * 1e6
            config = RadioConfig(
                frequency=int(freq),
                modulation=self.mod_var.get(),
                power=self.power_var.get(),
                bandwidth=12500,
                name=f"Channel {len(self.radio.configs) + 1}"
            )
            self.radio.add_config(config)
            self.update_channel_list()
            self.radio.save_config("radio_configs.json")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
            
    def remove_channel(self):
        """Remove selected channel"""
        selection = self.channel_list.curselection()
        if selection:
            index = selection[0]
            del self.radio.configs[index]
            self.update_channel_list()
            self.radio.save_config("radio_configs.json")
            
    def load_channel(self):
        """Load selected channel settings"""
        selection = self.channel_list.curselection()
        if selection:
            config = self.radio.configs[selection[0]]
            self.freq_var.set(f"{config.frequency/1e6:.3f}")
            self.mod_var.set(config.modulation)
            self.power_var.set(config.power)
            
    def update_channel_list(self):
        """Update the channel listbox"""
        self.channel_list.delete(0, tk.END)
        for config in self.radio.configs:
            self.channel_list.insert(tk.END, f"{config.name}: {config.frequency/1e6:.3f}MHz {config.modulation}")
            
    def on_channel_select(self, event):
        """Handle channel selection"""
        selection = self.channel_list.curselection()
        if selection:
            config = self.radio.configs[selection[0]]
            self.freq_var.set(f"{config.frequency/1e6:.3f}")
            self.mod_var.set(config.modulation)
            self.power_var.set(config.power)

def main():
    root = tk.Tk()
    app = RpiTXGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
