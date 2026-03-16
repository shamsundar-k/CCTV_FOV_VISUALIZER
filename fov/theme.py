_LIGHT = {
    "bg":          "#f5f5f7",
    "bg2":         "#ffffff",
    "panel":       "#eaeaf0",
    "border":      "#c0c0d0",
    "text":        "#1a1a2e",
    "text2":       "#444466",
    "accent":      "#4040aa",
    "accent2":     "#6060cc",
    "warn":        "#c0392b",
    "info":        "#2471a3",
    "sep":         "#c8c8dc",
    # 2D canvas colours
    "canvas_bg":   "#f8f8fc",
    "canvas_bg2":  "#ffffff",
    "grid":        "#dcdce8",
    "grid2":       "#ebebf5",
    "ground":      "#888899",
    "fov_ray":     "#333355",
    "fov_near":    "#888899",
    "tgt_dist":    "#996600",
    "tgt_h":       "#006688",
    "cam_body":    "#333355",
    "cam_pole":    "#555577",
    "axis_lbl":    "#333355",
    "tick":        "#555577",
    "title":       "#1a1a44",
    "divider":     "#c0c0d8",
    # 3D canvas always dark
    "gl_bg":       (0.10, 0.10, 0.16, 1.0),
    "gl_ground":   (0.12, 0.12, 0.20, 0.7),
    "gl_grid":     (0.22, 0.22, 0.38, 0.8),
    "gl_fov":      (0.9,  0.9,  0.9,  0.9),
    "gl_cam":      "#dddddd",
}


def TH(key=None):
    """Return the active theme dict, or a single value if key given."""
    return _LIGHT[key] if key else _LIGHT
