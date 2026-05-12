# Time Capsule

<p>
  <img src="https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54" alt="Python" />
  <img src="https://img.shields.io/badge/GTK-3.0-4A86CF?style=flat&logo=gnome&logoColor=white" alt="GTK3" />
  <img src="https://img.shields.io/badge/AUR-1793D1?style=flat&logo=archlinux&logoColor=white" alt="AUR" />
  <img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat" alt="License: MIT" />
</p>

A tiny always-on-top GTK stopwatch and countdown timer that stays out of your way.

<p>
  <img src="assets/timer.png" alt="Timer" width="300"/>
  <img src="assets/help-dialog.png" alt="Help Dialog" width="300"/>
</p>

---

## Install

**From AUR:**

```bash
yay -S time-capsule
```

AUR page: https://aur.archlinux.org/packages/time-capsule

---

## Usage

Launch from your app launcher by searching **Time Capsule**, or run `time-capsule` in terminal.

### Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Start / Pause |
| `R` | Reset |
| `M` | Toggle Stopwatch / Timer mode |
| `H` | Show help |
| `+` / `-` | Resize capsule |

### Timer mode

When switched to timer mode with `M`, the digits become editable:

| Key | Action |
|-----|--------|
| `← →` | Move between digits |
| `↑ ↓` | Change digit value |
| `Enter` | Confirm and arm timer |
| `R` | Go back to editing |

---

## Dependencies

- `python`
- `python-gobject`
- `gtk3`