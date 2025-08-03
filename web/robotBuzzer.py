#!/usr/bin/env python3
# File name   : robotBuzzer.py
# Website     : www.adeept.com
# Author      : Adeept
# Date        : 2025/05/15
import time
from gpiozero import TonalBuzzer

class RobotBuzzer:
    def __init__(self, pin=18):
        """
        Initialize the robot buzzer.
        
        Args:
            pin (int): GPIO pin number for the buzzer (default: 18)
        """
        self.buzzer = TonalBuzzer(pin)
        self.is_playing = False
    
    def play_note(self, note, duration=1.0):
        """
        Play a single note for a specified duration.
        
        Args:
            note (str): Note to play (e.g., 'C4', 'A5', etc.)
            duration (float): Duration to play the note in seconds
        """
        try:
            self.is_playing = True
            self.buzzer.play(note)
            time.sleep(duration)
            self.buzzer.stop()
            self.is_playing = False
        except Exception as e:
            print(f"Error playing note {note}: {e}")
            self.is_playing = False
    
    def play_sequence(self, notes):
        """
        Play a sequence of notes.
        
        Args:
            notes (list): List of tuples (note, duration)
                         e.g., [('C4', 1), ('D4', 0.5), ('E4', 1)]
        """
        try:
            self.is_playing = True
            for note, duration in notes:
                self.buzzer.play(note)
                time.sleep(float(duration))
            self.buzzer.stop()
            self.is_playing = False
        except Exception as e:
            print(f"Error playing sequence: {e}")
            self.is_playing = False
    
    def play_startup_sound(self):
        """Play a startup sound sequence."""
        startup_notes = [
            ('C4', 0.2),
            ('E4', 0.2),
            ('G4', 0.2),
            ('C5', 0.4)
        ]
        self.play_sequence(startup_notes)
    
    def play_shutdown_sound(self):
        """Play a shutdown sound sequence."""
        shutdown_notes = [
            ('C5', 0.2),
            ('G4', 0.2),
            ('E4', 0.2),
            ('C4', 0.4)
        ]
        self.play_sequence(shutdown_notes)
    
    def play_alert_sound(self):
        """Play an alert/warning sound."""
        alert_notes = [
            ('C4', 0.3),
            ('C4', 0.3),
            ('C4', 0.3)
        ]
        self.play_sequence(alert_notes)
    
    def play_beep(self, count=1, note='C4', duration=0.2, pause=0.1):
        """
        Play a series of beeps.
        
        Args:
            count (int): Number of beeps
            note (str): Note to play for beeps
            duration (float): Duration of each beep
            pause (float): Pause between beeps
        """
        try:
            self.is_playing = True
            for i in range(count):
                self.buzzer.play(note)
                time.sleep(duration)
                self.buzzer.stop()
                if i < count - 1:  # Don't pause after the last beep
                    time.sleep(pause)
            self.is_playing = False
        except Exception as e:
            print(f"Error playing beeps: {e}")
            self.is_playing = False
    
    def stop(self):
        """Stop any currently playing sound."""
        try:
            self.buzzer.stop()
            self.is_playing = False
        except Exception as e:
            print(f"Error stopping buzzer: {e}")
    
    def is_busy(self):
        """Check if the buzzer is currently playing."""
        return self.is_playing
    
    def cleanup(self):
        """Clean up buzzer resources."""
        self.stop()

if __name__ == '__main__':
    # Test the buzzer functionality
    print("Testing Robot Buzzer...")
    
    buzzer = RobotBuzzer()
    
    try:
        print("Playing startup sound...")
        buzzer.play_startup_sound()
        time.sleep(1)
        
        print("Playing 3 beeps...")
        buzzer.play_beep(3)
        time.sleep(1)
        
        print("Playing alert sound...")
        buzzer.play_alert_sound()
        time.sleep(1)
        
        print("Playing single note...")
        buzzer.play_note('A4', 1.0)
        time.sleep(1)
        
        print("Playing shutdown sound...")
        buzzer.play_shutdown_sound()
        
        print("Test completed!")
        
    except KeyboardInterrupt:
        print("\nTest interrupted.")
    finally:
        buzzer.cleanup()