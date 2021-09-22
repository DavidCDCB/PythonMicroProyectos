#https://developer.gnome.org/pygtk/stable/
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):
	
	def __init__(self):
		self.v="Hola Mundo"
		Gtk.Window.__init__(self, title="Hello World")
		
		self.box = Gtk.Box(spacing=10)
		self.add(self.box)

		self.la = Gtk.Label()
		self.la.set_label("Hello World")
		self.la.set_angle(25)
		self.la.set_halign(Gtk.Align.END)
		self.box.pack_start(self.la, True, True, 0)
		#print(dir(self.la.props))
		#print("-",self.la.get_label())
		
		self.button = Gtk.Button(label="Click Here")
		self.button.connect("clicked", self.on_button_clicked,self.v)
		self.box.pack_start(self.button, True, True, 0)

	def on_button_clicked(self, widget,v):
		print(v)

win = MyWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
