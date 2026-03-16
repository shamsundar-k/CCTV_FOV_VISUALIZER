# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`py-fov` is a CCTV camera Field-of-View (FOV) visualiser built with PySide6 and PyOpenGL. It renders a 3-panel GUI: a 3D OpenGL view (centre), a 2D top-down view (right upper), and a 2D side-elevation view (right lower), with a slider/controls panel on the left.

## Commands

This project uses `uv` for dependency management (Python 3.12 required).

```bash
# Install dependencies
uv sync

# Run the application
uv run python main.py
```

## Package Structure

```
fov/
├── theme.py          # _LIGHT dict, TH() accessor
├── constants.py      # SENSOR_FORMATS, ASPECT_RATIOS, CAMERA_MODEL, DORI_* tables
├── geometry.py       # Pure-math FOV/geometry functions
├── dialogs.py        # CameraParamsDialog (QDialog)
├── gl_view.py        # GLView (QOpenGLWidget) — 3D FOV render
├── views2d.py        # Views2D (QWidget) — 2D top + side elevation views
├── control_panel.py  # ControlPanel (QWidget) — sliders, stats, DORI legend
└── main_window.py    # MainWindow (QMainWindow) — assembles all panels
main.py               # Entry point
```

## Architecture

### Data flow

`MainWindow._refresh()` reads slider values from `ControlPanel`, calls `compute_geometry()`, then pushes the resulting `geo` dict to `GLView.set_geometry()` and `Views2D.set_geometry()`. A 40 ms debounce timer prevents redundant redraws during slider drag.

### Key geometry functions (`fov/geometry.py`)

- `compute_geometry(f, H, target_dist, target_h, model)` — master function; returns a `geo` dict consumed by all views.
- `interpolate_angles(f, model)` — returns `(H_angle, V_angle)`. Uses manual datasheet angles (primary) or sensor-physics formula (fallback, when `sensor_width > 0`).
- `compute_tilt()` — auto-calculates camera tilt so the top FOV ray hits `target_height` at `target_distance`.
- `trapezoid_corners()` — ground-plane FOV footprint corners, used by both 3D and 2D renderers.

### Mutable globals and import rules

There is one mutable module-level global:

| Global | Module | Type | Pattern |
|---|---|---|---|
| `CAMERA_MODEL` | `fov.constants` | `dict` (mutated in place) | `from .constants import CAMERA_MODEL` then `.update()` is safe |

`TH()` in `fov/theme.py` always returns the single light theme dict; it is safe to import by name.

### Adding a new view or feature

1. Add pure logic to `geometry.py` (no Qt imports).
2. Create a new widget module in `fov/` importing from `theme`, `constants`, and `geometry`.
3. Wire it into `MainWindow` in `main_window.py`.
