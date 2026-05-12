import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

class TimeCapsule(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Time-Capsule")
        self.connect("destroy", Gtk.main_quit)

        self.seconds = 0
        self.running = False    # will use this later for start/stop

        self.label = Gtk.Label(label="00:00")
        self.add(self.label)

        GLib.timeout_add(1000, self.tick)

        self.connect("key-press-event", self.on_key_press)

        self.set_decorated(False) # remove titlebar
        self.set_keep_above(True) # always on top
        self.set_resizable(False) # fixed size

        self.apply_styles()

    def on_key_press(self, widget, event):
        key = event.keyval

        if key == ord(' '):
            self.running = not self.running

        elif key ==  ord('r') or key == ord('R'):
            self.running = False
            self.seconds = 0
            self.label.set_text("00:00")

    def tick(self, *args):
        if self.running: 
            self.seconds += 1
            mins = self.seconds // 60
            secs = self.seconds % 60
            self.label.set_text(f"{mins:02d}:{secs:02d}")
        return True     # returning true keeps the timer repeating
    
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