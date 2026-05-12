import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

class TimeCapsule(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Time-Capsule")
        self.connect("destroy", Gtk.main_quit)

        self.mode = "stopwatch"
        self.state = "idle"     # "idle", "editing", "running", "paused", "done"
        self.seconds = 0
        self.total_seconds = 0  # stores otiginal timer value for reset
        self.edit_pos = 0
        self.edit_digits = [0, 0, 0, 0]

        self.label = Gtk.Label(label="00:00")
        self.add(self.label)

        GLib.timeout_add(1000, self.tick)

        self.connect("key-press-event", self.on_key_press)

        self.set_decorated(False) # remove titlebar
        self.set_keep_above(True) # always on top
        self.set_resizable(False) # fixed size

        self.apply_styles()

    def digits_to_seconds(self):
        mins = self.edit_digits[0] * 10 + self.edit_digits[1]
        secs = self.edit_digits[2] * 10 + self.edit_digits[3]
        return mins * 60 + secs

    def seconds_to_text(self, s):
        mins = s // 60
        secs = s % 60
        return f"{mins:02d}:{secs:02d}"

    def editing_text(self):
        d = self.edit_digits
        text = f"{d[0]}{d[1]}:{d[2]}{d[3]}"
        pos = self.edit_pos
        chars = [d[0], d[1], ':', d[2], d[3]]
        result = ""
        digit_index = 0
        for ch in chars:
            if ch == ':':
                result += ':'
            else:
                if digit_index == pos:
                    result += f"[{ch}]"
                else:
                    result += str(ch)
                digit_index += 1
        return result

    def tick(self, *args):
        if self.state == "running":
            if self.mode == "stopwatch":
                self.seconds += 1
                self.label.set_text(self.seconds_to_text(self.seconds))
            elif self.mode == "timer":
                self.seconds -= 1
                if self.seconds <= 0:
                    self.seconds = 0
                    self.state = "done"
                    self.label.set_text("00:00")
                else:
                    self.label.set_text(self.seconds_to_text(self.seconds))
        return True

    def on_key_press(self, widget, event):
        key = event.keyval

        if key == ord('m') or key == ord('M'):
            if self.mode == "stopwatch":
                self.mode = "timer"
                self.state = "editing"
                self.edit_digits = [0, 0, 0, 0]
                self.edit_pos = 0
                self.label.set_text(self.editing_text())
            else:
                self.mode = "stopwatch"
                self.state = "idle"
                self.seconds = 0
                self.label.set_text("00:00")

        elif key == ord(' '):
            if self.mode == "stopwatch":
                if self.state in ("idle", "paused"):
                    self.state = "running"
                elif self.state == "running":
                    self.state = "paused"
            elif self.mode == "timer":
                if self.state == "editing":
                    pass
                elif self.state == "idle":
                    if self.seconds > 0:
                        self.state = "running"
                elif self.state == "running":
                    self.state = "paused"
                elif self.state == "paused":
                    self.state = "running"

        elif key == Gdk.KEY_Return:
            if self.mode == "timer" and self.state == "editing":
                self.total_seconds = self.digits_to_seconds()
                self.seconds = self.total_seconds
                if self.seconds > 0:
                    self.state = "idle"
                    self.label.set_text(self.seconds_to_text(self.seconds))

        elif key ==  ord('r') or key == ord('R'):
            if self.mode == "stopwatch":
                self.state = "idle"
                self.seconds = 0
                self.label.set_text("00:00")
            elif self.mode ==  "timer":
                self.state = "editing"
                self.edit_digits = [0, 0, 0, 0]
                self.edit_pos = 0
                self.label.set_text(self.editing_text())

        elif self.mode == "timer" and self.state == "editing":
            if key == Gdk.KEY_Left:
                self.edit_pos = max(0, self.edit_pos - 1)
                self.label.set_text(self.editing_text())
            elif key == Gdk.KEY_Right:
                self.edit_pos = min(3, self.edit_pos + 1)
                self.label.set_text(self.editing_text())
            elif key == Gdk.KEY_Up:
                limits = [5, 9, 5, 9]
                self.edit_digits[self.edit_pos] = (self.edit_digits[self.edit_pos] + 1) % (limits[self.edit_pos] + 1)
                self.label.set_text(self.editing_text())
            elif key == Gdk.KEY_Down:
                limits = [5, 9, 5, 9]
                self.edit_digits[self.edit_pos] = (self.edit_digits[self.edit_pos] - 1) % (limits[self.edit_pos] + 1)
                self.label.set_text(self.editing_text())
    
    def apply_styles(self):
        css = b"""
            window {
                background-color: rgba(0, 0, 0, 0);
            }
            label {
                background-color: #1a1a1a;
                color: #ffffff;
                font-family: monospace;
                font-size: 20px;
                padding: 8px 20px;
            }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

app = TimeCapsule()
app.show_all()
Gtk.main()