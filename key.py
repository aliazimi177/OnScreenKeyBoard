from keyboard import suggest
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

#css style 
def apply_custom_theme():
    style_provider = Gtk.CssProvider()
    style_provider.load_from_path('custom_theme.css')
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


class ModifiedSimpleKeyboard(Gtk.Window):
    def __init__(self):
        super().__init__(title="On-Screen Keyboard with Suggestions")
        self.set_border_width(10)
        self.set_size_request(600, 400)

        self.set_type_hint(Gdk.WindowTypeHint.UTILITY)
        self.set_skip_taskbar_hint(True)
        self.set_keep_above(True)

        vbox = Gtk.VBox(spacing=6)
        self.add(vbox)

        self.textview = Gtk.TextView()
        self.textview.set_cursor_visible(True)  
        vbox.pack_start(self.textview, True, True, 0)

        # Define the keys with Persian characters
        rows = [
            ['۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '۰'],
            ['ض', 'ق', 'ف', 'غ', 'ع', 'ه', 'خ', 'ح'],
            ['ج', 'چ', 'ش', 'س', 'ی', 'ب', 'ل', 'ا', 'ت', 'ن'],
            ['م', 'ک', 'گ', 'ز', 'ر', 'د', 'پ', 'و'],
            ['Space', 'Backspace']
        ]

        for row in rows:
            hbox = Gtk.HBox(spacing=6)
            vbox.pack_start(hbox, True, True, 0)
            for key in row:
                button = Gtk.Button(label=key)
                button.connect("clicked", self.on_key_clicked, key)
                if key == "Space":
                    button.set_hexpand(True)
                hbox.pack_start(button, True, True, 0)

        self.suggestions_box = Gtk.HBox(spacing=6)
        vbox.pack_start(self.suggestions_box, True, True, 0)
    
    def word_exists(self, word):
        return find(self.root, lambda node: node.name == word) is not None
    def on_key_clicked(self, widget, key):
        buffer = self.textview.get_buffer()
        if key == "Space":
            buffer.insert_at_cursor(' ')
        elif key == "Backspace":
            start, end = buffer.get_bounds()
            cursor_mark = buffer.get_insert()
            cursor_iter = buffer.get_iter_at_mark(cursor_mark)
            if cursor_iter.starts_line():
                pass  # Do not delete if at the start
            else:
                cursor_iter.backward_char()
                buffer.delete(cursor_iter, buffer.get_iter_at_mark(cursor_mark))
        else:
            buffer.insert_at_cursor(key)

        self.update_suggestions()
        start, end = buffer.get_bounds()
        text = buffer.get_text(start, end, True)
        words = text.split()
        current_word = words[-1] if words else ""
        if current_word and not self.word_exists(current_word):
            # Underline the word in red if it's misspelled
            start_offset = end.get_offset() - len(current_word)
            start_iter = buffer.get_iter_at_offset(start_offset)
            tag = buffer.create_tag(None, underline=Pango.Underline.ERROR, underline_set=True)
            buffer.apply_tag(tag, start_iter, end)


    def update_suggestions(self):
        for widget in self.suggestions_box.get_children():
            self.suggestions_box.remove(widget)

        buffer = self.textview.get_buffer()
        start, end = buffer.get_bounds()
        text = buffer.get_text(start, end, True)
        words = text.split()
        current_word = words[-1] if words else ""

        suggested_words = suggest(current_word)
        for word in suggested_words:
            button = Gtk.Button(label=word.name)
            button.connect("clicked", self.on_suggestion_clicked, word.name)
            self.suggestions_box.pack_start(button, False, False, 0)
            button.show()

    def on_suggestion_clicked(self, widget, word):
        buffer = self.textview.get_buffer()
        start, end = buffer.get_bounds()
        text = buffer.get_text(start, end, True)
        words = text.split()
        if words:
            words[-1] = word + " "
            new_text = ' '.join(words)
            buffer.set_text(new_text)
            

style_provider = Gtk.CssProvider()
style_provider.load_from_data(b'''
    * {
        -GtkWidget-cursor-color: blue;
        -GtkWidget-secondary-cursor-color: red;
    }
''')
Gtk.StyleContext.add_provider_for_screen(
    Gdk.Screen.get_default(),
    style_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
)
apply_custom_theme()
win = ModifiedSimpleKeyboard()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
