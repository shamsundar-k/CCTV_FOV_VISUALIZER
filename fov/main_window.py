import json

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QTabWidget, QDialog, QFileDialog,
)
from PySide6.QtCore import QTimer
from PySide6.QtGui import QColor, QPalette

from .theme import TH
from .constants import CAMERA_MODEL
from .geometry import compute_geometry
from .dialogs import CameraParamsDialog
from .gl_view import GLView
from .views2d import Views2D
from .control_panel import ControlPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CCTV FOV Visualiser — 3D + 2D DORI Analysis")
        self.resize(1600, 900)

        self._debounce = QTimer()
        self._debounce.setSingleShot(True)
        self._debounce.setInterval(40)
        self._debounce.timeout.connect(self._refresh)

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(4, 4, 4, 4)
        root.setSpacing(4)

        self._ctrl = ControlPanel(
            on_change=lambda: self._debounce.start(),
            on_cam_params=self._open_cam_params,
        )
        root.addWidget(self._ctrl)

        self._tabs = QTabWidget()
        self._tabs.setStyleSheet(self._tab_style())
        self._gl  = GLView()
        self._v2d = Views2D()
        self._tabs.addTab(self._gl,  "3D View")
        self._tabs.addTab(self._v2d, "2D View")
        root.addWidget(self._tabs, 1)

        self._geo = None
        self._build_menu()
        self._apply_palette()
        self._refresh()

    def _build_menu(self):
        mb = self.menuBar()
        fm = mb.addMenu("File")
        fm.addAction("Save Config…",  self._save_config)
        fm.addAction("Load Config…",  self._load_config)
        fm.addSeparator()
        fm.addAction("Export 2D View…", lambda: self._v2d.save_image(self, self._geo, CAMERA_MODEL))
        fm.addAction("Export 3D View…", lambda: self._gl.save_image(self, self._geo, CAMERA_MODEL))

    def _save_config(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Configuration", "fov_config.json",
            "JSON Files (*.json)")
        if not path:
            return
        pr = self._ctrl.get_params()
        cfg = {
            "focal_mm":       pr["f"],
            "height_m":       pr["H"],
            "target_dist_m":  pr["tgt_d"],
            "target_h_m":     pr["tgt_h"],
            "bearing_deg":    pr["bearing"],
            "camera_model":   dict(CAMERA_MODEL),
        }
        with open(path, "w") as fh:
            json.dump(cfg, fh, indent=2)

    def _load_config(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Configuration", "",
            "JSON Files (*.json)")
        if not path:
            return
        with open(path) as fh:
            cfg = json.load(fh)
        s = self._ctrl._sliders
        if "focal_mm"      in cfg: s["focal"].setValue(  int(cfg["focal_mm"]      * 10))
        if "height_m"      in cfg: s["height"].setValue( int(cfg["height_m"]      * 10))
        if "target_dist_m" in cfg: s["tgt_d"].setValue(  int(cfg["target_dist_m"] * 10))
        if "target_h_m"    in cfg: s["tgt_h"].setValue(  int(cfg["target_h_m"]    * 10))
        if "bearing_deg"   in cfg: s["bearing"].setValue(int(cfg["bearing_deg"]))
        if "camera_model"  in cfg:
            CAMERA_MODEL.update(cfg["camera_model"])
            self._ctrl.refresh_model_label()
            self._ctrl.refresh_focal_slider()
            self._ctrl.refresh_fov_label()
        self._debounce.start()

    def _tab_style(self):
        return f"""
            QTabWidget::pane {{
                border:1px solid {TH('border')}; border-radius:4px;
                background:{TH('bg2')};
            }}
            QTabBar::tab {{
                background:{TH('panel')}; color:{TH('text')};
                border:1px solid {TH('border')}; border-bottom:none;
                border-radius:4px 4px 0 0;
                padding:6px 24px; font-size:11px; font-weight:bold;
            }}
            QTabBar::tab:selected {{
                background:{TH('accent')}; color:#ffffff;
            }}
            QTabBar::tab:hover:!selected {{
                background:{TH('bg')}; color:{TH('text')};
            }}
        """

    def _apply_palette(self):
        app = QApplication.instance()
        pal = QPalette()
        pal.setColor(QPalette.Window,          QColor(TH("bg")))
        pal.setColor(QPalette.WindowText,      QColor(TH("text")))
        pal.setColor(QPalette.Base,            QColor(TH("bg2")))
        pal.setColor(QPalette.AlternateBase,   QColor(TH("panel")))
        pal.setColor(QPalette.Text,            QColor(TH("text")))
        pal.setColor(QPalette.Button,          QColor(TH("panel")))
        pal.setColor(QPalette.ButtonText,      QColor(TH("text")))
        pal.setColor(QPalette.Highlight,       QColor(TH("accent")))
        pal.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        pal.setColor(QPalette.Mid,             QColor(TH("border")))
        pal.setColor(QPalette.Dark,            QColor(TH("border")))
        pal.setColor(QPalette.Light,           QColor(TH("bg2")))
        app.setPalette(pal)
        self.update()

    def _open_cam_params(self):
        dlg = CameraParamsDialog(CAMERA_MODEL, parent=self)
        if dlg.exec() == QDialog.Accepted:
            CAMERA_MODEL.update(dlg.get_model())
            self._ctrl.refresh_model_label()
            self._ctrl.refresh_focal_slider()
            self._ctrl.refresh_fov_label()
            self._debounce.start()

    def _refresh(self):
        pr = self._ctrl.get_params()
        geo, warn = compute_geometry(
            pr["f"], pr["H"], pr["tgt_d"], pr["tgt_h"], CAMERA_MODEL)
        self._geo = geo
        self._ctrl.update_stats(geo, warn)
        if geo:
            self._gl.set_geometry(geo, pr["bearing"])
            self._v2d.set_geometry(geo)
