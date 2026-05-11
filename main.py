import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

class TimeCapsule(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Time-Capsule")
        self.connect("destroy", Gtk.main_quit)

        self.seconds = 0
        self.running = False    # will use this later for start/stop

        self.label = Gtk.Label(label="00:00")
        self.add(self.label)

        self.connect("key-press-event", self.on_key_press)

        GLib.timeout_add(1000, self.tick)

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
        

app = TimeCapsule()
app.show_all()
Gtk.main()