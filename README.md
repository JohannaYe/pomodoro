# pomodoro
A clean and efficient Pomodoro timer built with Python/Tkinter. Also called "番茄钟" or "tomato clock" in Chinese.
# Focus Timer - A Modern Pomodoro App

A sleek and minimal Pomodoro Timer application built with Python and Tkinter, designed to help you maintain focus while working on your papers or projects.

## Features

- 🎯 Clean and modern UI design
- ⏱️ Customizable work/break intervals
- 🔄 Auto-switch between work and break sessions
- 📊 Track your daily focus sessions and total time
- 🎨 Platform-specific styling (optimized for both macOS and Windows)
- 🔔 Sound notifications for session completion
- 📌 Always-on-top window option

## Default Settings

- Work session: 25 minutes
- Short break: 5 minutes
- Long break: 15 minutes
- Long break interval: Every 4 sessions
- Sound notifications: Enabled
- Auto-start breaks: Optional

## Requirements

- Python 3.x
- Tkinter (usually comes with Python)

## Usage

1. Clone the repository
2. Run the timer:
```bash
python tomato_clock.py
```

## Customization

Settings can be customized by modifying the `DEFAULT_SETTINGS` in the `PomodoroConfig` class:
- Work/break durations
- Session counts before long breaks
- Sound notifications
- Auto-start preferences

## Platform Support

- Optimized for macOS with native-looking controls
- Fully compatible with Windows and Linux
- Adaptive UI styling based on the operating system

## Contributing

Feel free to fork, submit PRs, or suggest improvements!
