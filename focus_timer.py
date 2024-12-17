"""
Focus Timer - A Modern Pomodoro Timer Application

A clean and efficient Pomodoro timer built with Python/Tkinter, featuring:
- Customizable work/break intervals
- Session tracking and statistics
- Platform-specific UI optimizations
- Sound notifications
- Always-on-top window option

Author: Zhuo Han Ye
Date: December 2023
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import platform
import os
from datetime import datetime, timedelta
import json

class PomodoroConfig:
    DEFAULT_SETTINGS = {
        'work_time': 25,
        'break_time': 5,
        'long_break_time': 15,
        'sessions_before_long_break': 4,
        'sound_enabled': True,
        'auto_start_breaks': False
    }
    
    def __init__(self):
        self.settings = self.load_settings()
        
    def load_settings(self):
        try:
            with open('pomodoro_settings.json', 'r') as f:
                return {**self.DEFAULT_SETTINGS, **json.load(f)}
        except FileNotFoundError:
            return self.DEFAULT_SETTINGS.copy()
            
    def save_settings(self):
        with open('pomodoro_settings.json', 'w') as f:
            json.dump(self.settings, f)

class PomodoroStats:
    def __init__(self):
        self.completed_pomodoros = 0
        self.total_focus_time = 0
        self.start_time = None
        
    def start_session(self):
        self.start_time = time.time()
        
    def end_session(self):
        if self.start_time:
            session_duration = time.time() - self.start_time
            self.total_focus_time += session_duration
            self.completed_pomodoros += 1
            self.start_time = None

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        self.config = PomodoroConfig()
        self.stats = PomodoroStats()
        
        self._setup_ui()
        self._setup_variables()
        
    def _setup_variables(self):
        self.remaining_time = self.config.settings['work_time'] * 60
        self.running = False
        self.is_break = False
        self.sessions_completed = 0
        self.last_tick = None
        
    def _setup_ui(self):
        self.master.title("Focus Timer - For your paper")
        self.master.geometry("500x500")
        self.master.configure(bg='#FFF5E1')
        self.master.attributes('-topmost', True)
        
        self._create_header()
        self._create_timer_display()
        self._create_progress_bar()
        self._create_controls()
        self._create_stats_display()
        
    def _create_header(self):
        header_frame = tk.Frame(self.master, bg='#FFF5E1')
        header_frame.pack(fill=tk.X, pady=20)
        
        self.title_label = tk.Label(
            header_frame,
            text="Paper!!! Your paper!!!",
            font=("SF Pro Display", 20, "bold"),
            fg='#FF6B6B',
            bg='#FFF5E1'
        )
        self.title_label.pack()
        
    def _create_timer_display(self):
        self.timer_label = tk.Label(
            self.master,
            text=f"{self.config.settings['work_time']:02d}:00",
            font=("SF Pro Display", 80, "bold"),
            fg='#4ECDC4',
            bg='#FFF5E1'
        )
        self.timer_label.pack(pady=20)
        
    def _create_progress_bar(self):
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            self.master,
            variable=self.progress_var,
            maximum=100,
            length=300,
            mode='determinate'
        )
        self.progress_bar.pack(pady=10)
        
    def _create_controls(self):
        control_frame = tk.Frame(self.master, bg='#FFF5E1')
        control_frame.pack(pady=20)
        
        buttons = [
            ("START", self.start_timer, '#45B7D1'),
            ("BREAK", self.start_break, '#4CAF50'),
            ("RESET", self.reset_timer, '#FF6B6B')
        ]
        
        # Check if running on macOS
        is_macos = platform.system() == 'Darwin'
        
        for text, command, color in buttons:
            button_style = {
                'text': text,
                'command': command,
                'font': ("SF Pro Display", 14, "bold"),
                'width': 8
            }
            
            if is_macos:
                # macOS specific style
                button_style.update({
                    'bg': '#FFFFFF',
                    'fg': color,
                    'activebackground': '#F0F0F0',
                    'activeforeground': color,
                    'bd': 2,
                    'relief': 'raised'
                })
            else:
                # Windows/Linux style
                button_style.update({
                    'bg': color,
                    'fg': 'white',
                    'relief': 'solid',
                    'highlightbackground': color,
                    'highlightcolor': color
                })
            
            btn = tk.Button(control_frame, **button_style)
            btn.pack(side=tk.LEFT, padx=10)
            
    def _create_stats_display(self):
        stats_frame = tk.Frame(self.master, bg='#FFF5E1')
        stats_frame.pack(pady=20, fill=tk.X, padx=20)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Come on, start your Pomodoro!\nToday focus: 0 tomato\nTotal focus: 0 min",
            font=("SF Pro Text", 13),
            fg='#4A4A4A',
            bg='#FFF5E1',
            justify=tk.LEFT
        )
        self.stats_label.pack(anchor=tk.W)
        
    def update_stats_display(self):
        total_minutes = int(self.stats.total_focus_time / 60)
        self.stats_label.config(
            text=f"today focus: {self.stats.completed_pomodoros} tomatoes\n"
                f"total focus: {total_minutes} mins"
        )
        
    def countdown(self):
        if not self.running:
            return
            
        current_time = time.time()
        if self.last_tick:
            self.remaining_time -= int(current_time - self.last_tick)
        self.last_tick = current_time
        
        if self.remaining_time <= 0:
            self.timer_complete()
            return
            
        minutes, seconds = divmod(self.remaining_time, 60)
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        
        # Update progress bar
        total_time = (self.config.settings['break_time'] if self.is_break else self.config.settings['work_time']) * 60
        progress = ((total_time - self.remaining_time) / total_time) * 100
        self.progress_var.set(progress)
        
        self.master.after(1000, self.countdown)
        
    def timer_complete(self):
        if not self.is_break:
            self.sessions_completed += 1
            self.stats.end_session()
            self.update_stats_display()
            
        self.play_notification()
        self.show_completion_message()
        
        # Auto-start next session if configured
        if self.config.settings['auto_start_breaks']:
            if self.is_break:
                self.start_timer()
            else:
                self.start_break()
        else:
            self.reset_timer()
            
    def start_timer(self):
        if self.running:
            self.reset_timer()
        
        self.running = True
        self.is_break = False
        self.remaining_time = self.config.settings['work_time'] * 60
        self.last_tick = time.time()
        self.stats.start_session()
        self.countdown()
        
    def start_break(self):
        if self.running:
            self.reset_timer()
            
        self.running = True
        self.is_break = True
        
        # Determine if it should be a long break
        if self.sessions_completed >= self.config.settings['sessions_before_long_break']:
            self.remaining_time = self.config.settings['long_break_time'] * 60
            self.sessions_completed = 0
        else:
            self.remaining_time = self.config.settings['break_time'] * 60
            
        self.last_tick = time.time()
        self.countdown()
        
    def reset_timer(self):
        self.running = False
        self.is_break = False
        self.remaining_time = self.config.settings['work_time'] * 60
        self.last_tick = None
        self.progress_var.set(0)
        minutes = self.config.settings['work_time']
        self.timer_label.config(text=f"{minutes:02d}:00")
        
    def play_notification(self):
        if self.config.settings['sound_enabled']:
            if platform.system() == 'Darwin':
                os.system('afplay /System/Library/Sounds/Glass.aiff')
                
    def show_completion_message(self):
        self.master.lift()
        self.master.attributes('-topmost', True)
        
        msg_window = tk.Toplevel(self.master)
        msg_window.title("Pomodoro Timer")
        msg_window.geometry("300x150")
        msg_window.configure(bg='#FFF5E1')
        msg_window.attributes('-topmost', True)
        
        message = "It's time to take a break!" if not self.is_break else "It's time to focus!"
        
        msg_label = tk.Label(
            msg_window,
            text=message,
            font=("SF Pro Display", 16),
            bg='#FFF5E1',
            wraplength=250
        )
        msg_label.pack(pady=20)
        
        # Check if running on macOS for OK button style
        is_macos = platform.system() == 'Darwin'
        button_style = {
            'text': "OK",
            'command': msg_window.destroy,
            'font': ("SF Pro Display", 13, "bold")
        }
        
        if is_macos:
            button_style.update({
                'bg': '#FFFFFF',
                'fg': '#45B7D1',
                'activebackground': '#F0F0F0',
                'activeforeground': '#45B7D1',
                'bd': 2,
                'relief': 'raised'
            })
        else:
            button_style.update({
                'bg': '#45B7D1',
                'fg': 'white',
                'relief': 'solid'
            })
        
        ok_button = tk.Button(msg_window, **button_style)
        ok_button.pack(pady=10)

def main():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()