import gi
import math
import cairo
from gi.repository import Gtk, Adw, Gio, GLib, Gdk
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")

class BatteryHealthWidget(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.set_content_width(120)  # Veći widget za veći krug
        self.set_content_height(120)
        self.set_draw_func(self.on_draw)
        self.health_percentage = 100  # Inicijalno postavi na 100%

    def set_health_percentage(self, percentage):
        self.health_percentage = percentage
        self.queue_draw()  # Redraw kad se promeni procenat

    def on_draw(self, widget, context, width, height):
        radius = min(width, height) / 2 - 10  # Definiši radijus kruga
        context.set_line_width(15)  # Debljina linije kruga

        # Centar kruga
        xc, yc = width / 2, height / 2

        # Pozadinski krug
        context.arc(xc, yc, radius, 0, 2 * math.pi)
        context.set_source_rgb(0.8, 0.8, 0.8)  # Svetlija siva boja za pozadinu
        context.stroke()

        # Popunjeni deo kruga (u zavisnosti od procenta)
        angle = (self.health_percentage / 100) * 2 * math.pi
        context.arc(xc, yc, radius, -math.pi / 2, -math.pi / 2 + angle)
        context.set_source_rgb(0.2, 0.6, 0.2)  # Zelena boja za procenat
        context.stroke()

        # Prikaz procenta unutar kruga
        context.select_font_face("Sans", cairo.FontSlant.NORMAL, cairo.FontWeight.BOLD)
        context.set_font_size(20)  # Veći font za bolju vidljivost
        text = f"{self.health_percentage:.2f}%"
        xb, yb, width, height = context.text_extents(text)[:4]
        context.move_to(xc - width / 2, yc + height / 2)
        context.set_source_rgb(1, 1, 1)  # Bela boja za tekst
        context.show_text(text)

class VoltageChartWidget(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.set_content_width(300)  # Širina widgeta
        self.set_content_height(100)  # Visina widgeta
        self.set_draw_func(self.on_draw)
        self.voltage_data = []

    def set_voltage_data(self, data):
        if data:  # Proveri da li su podaci validni
            self.voltage_data += data
            self.queue_draw()  # Redraw kad se podaci promene
        else:
            print("No data to update.")

    def on_draw(self, widget, context, width, height):
        # Očisti prethodni crtež
        context.set_source_rgb(1, 1, 1)  # Bela boja za pozadinu
        context.rectangle(0, 0, width, height)
        context.fill()

        # Crtanje grid linija
        context.set_source_rgb(0.9, 0.9, 0.9)  # Svetlo siva boja za grid
        context.set_line_width(1)

        num_lines = 5
        for i in range(num_lines):
            y = i * height / (num_lines - 1)
            context.move_to(0, y)
            context.line_to(width, y)
            context.stroke()
            
            # Prikazivanje vrednosti
            value = (1 - i / (num_lines - 1)) * (5 - 3) + 3
            context.move_to(5, y - 5)
            context.set_source_rgb(0, 0, 0)  # Crna boja za tekst
            context.show_text(f"{value:.2f}")

        # Crtanje grafikona
        if len(self.voltage_data) < 2:
            return

        context.set_source_rgb(0, 0, 1)  # Plava boja za liniju
        context.set_line_width(2)

        # Fiksni opseg između 3 i 5
        min_voltage = 3
        max_voltage = 5
        y_scale = height / (max_voltage - min_voltage)
        x_step = width / (len(self.voltage_data) - 1)

        prev_x = 0
        prev_y = height - (self.voltage_data[0] - min_voltage) * y_scale

        context.move_to(prev_x, prev_y)  # Počni crtanje linije
        for i, voltage in enumerate(self.voltage_data):
            x = i * x_step
            y = height - (voltage - min_voltage) * y_scale
            context.line_to(x, y)

        context.stroke()

        # Dodavanje legende
        legend_x = width - 70  # X pozicija legende
        legend_y = 15  # Y pozicija legende
        context.set_source_rgb(0, 0, 0)  # Crna boja za tekst
        context.set_font_size(12)

        # Prikaz boje legende
        context.set_source_rgb(0, 0, 1)  # Boja linije u legendi
        context.rectangle(legend_x - 20, legend_y - 10, 15, 10)  # Pravougaonik za boju
        context.fill()

        # Prikaz tekstualne oznake
        context.set_source_rgb(0, 0, 0)  # Crna boja za tekst
        context.move_to(legend_x - 5, legend_y)
        context.show_text("Voltage")

class CurrentChartWidget(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.set_content_width(300)  # Širina widgeta
        self.set_content_height(100)  # Visina widgeta
        self.set_draw_func(self.on_draw)
        self.current_data = []

    def set_current_data(self, data):
        if data:  # Proveri da li su podaci validni
            self.current_data += data
            self.queue_draw()  # Redraw kad se podaci promene
        else:
            print("No data to update.")

    def on_draw(self, widget, context, width, height):
        # Očisti prethodni crtež
        context.set_source_rgb(1, 1, 1)  # Bela boja za pozadinu
        context.rectangle(0, 0, width, height)
        context.fill()

        # Crtanje grid linija
        context.set_source_rgb(0.9, 0.9, 0.9)  # Svetlo siva boja za grid
        context.set_line_width(1)

        num_lines = 5
        for i in range(num_lines):
            y = i * height / (num_lines - 1)
            context.move_to(0, y)
            context.line_to(width, y)
            context.stroke()
            
            # Prikazivanje vrednosti
            value = (1 - i / (num_lines - 1)) * (1100 - 700) + 700
            context.move_to(5, y - 5)
            context.set_source_rgb(0, 0, 0)  # Crna boja za tekst
            context.show_text(f"{value:.2f}")

        # Crtanje grafikona
        if len(self.current_data) < 2:
            return

        context.set_source_rgb(0, 1, 0)  # Zelena boja za liniju
        context.set_line_width(2)

        # Fiksni opseg između 4 i 5
        min_current = 700
        max_current = 1100
        y_scale = height / (max_current - min_current)
        x_step = width / (len(self.current_data) - 1)

        prev_x = 0
        prev_y = height - (self.current_data[0] - min_current) * y_scale

        context.move_to(prev_x, prev_y)  # Počni crtanje linije
        for i, current in enumerate(self.current_data):
            x = i * x_step
            y = height - (current - min_current) * y_scale
            context.line_to(x, y)

        context.stroke()

        # Dodavanje legende
        legend_x = width - 70  # X pozicija legende
        legend_y = 15  # Y pozicija legende
        context.set_source_rgb(0, 0, 0)  # Crna boja za tekst
        context.set_font_size(12)

        # Prikaz boje legende
        context.set_source_rgb(0, 1, 0)  # Boja linije u legendi
        context.rectangle(legend_x - 20, legend_y - 10, 15, 10)  # Pravougaonik za boju
        context.fill()

        # Prikaz tekstualne oznake
        context.set_source_rgb(0, 0, 0)  # Crna boja za tekst
        context.move_to(legend_x - 5, legend_y)
        context.show_text("Current")

class TemperatureChartWidget(Gtk.DrawingArea):
    def __init__(self):
        super().__init__()
        self.set_content_width(300)  # Širina widgeta
        self.set_content_height(100)  # Visina widgeta
        self.set_draw_func(self.on_draw)
        self.temperature_data = []

    def set_temperature_data(self, data):
        if data:  # Proveri da li su podaci validni
            self.temperature_data += data
            self.queue_draw()  # Redraw kad se podaci promene
        else:
            print("No data to update.")

    def on_draw(self, widget, context, width, height):
        # Očisti prethodni crtež
        context.set_source_rgb(1, 1, 1)  # Bela boja za pozadinu
        context.rectangle(0, 0, width, height)
        context.fill()

        # Crtanje grid linija
        context.set_source_rgb(0.9, 0.9, 0.9)  # Svetlo siva boja za grid
        context.set_line_width(1)

        num_lines = 5
        for i in range(num_lines):
            y = i * height / (num_lines - 1)
            context.move_to(0, y)
            context.line_to(width, y)
            context.stroke()
            
            # Prikazivanje vrednosti
            value = (1 - i / (num_lines - 1)) * (40 - 30) + 30
            context.move_to(5, y - 5)
            context.set_source_rgb(0, 0, 0)  # Crna boja za tekst
            context.show_text(f"{value:.2f}")

        # Crtanje grafikona
        if len(self.temperature_data) < 2:
            return

        context.set_source_rgb(1, 0, 0)  # Zelena boja za liniju
        context.set_line_width(2)

        # Fiksni opseg između 4 i 5
        min_current = 30
        max_current = 40
        y_scale = height / (max_current - min_current)
        x_step = width / (len(self.temperature_data) - 1)

        prev_x = 0
        prev_y = height - (self.temperature_data[0] - min_current) * y_scale

        context.move_to(prev_x, prev_y)  # Počni crtanje linije
        for i, current in enumerate(self.temperature_data):
            x = i * x_step
            y = height - (current - min_current) * y_scale
            context.line_to(x, y)

        context.stroke()

        # Dodavanje legende
        legend_x = width - 70  # X pozicija legende
        legend_y = 15  # Y pozicija legende
        context.set_source_rgb(0, 0, 0)  # Crna boja za tekst
        context.set_font_size(12)

        # Prikaz boje legende
        context.set_source_rgb(1, 0, 0)  # Boja linije u legendi
        context.rectangle(legend_x - 20, legend_y - 10, 15, 10)  # Pravougaonik za boju
        context.fill()

        # Prikaz tekstualne oznake
        context.set_source_rgb(0, 0, 0)  # Crna boja za tekst
        context.move_to(legend_x - 5, legend_y)
        context.show_text("Temperature")


class BatteryMonitorApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="lol.janjic.battmon")
        self.temperature_data = []
        self.labels = {}  # Inicijalizuj labels kao prazan rečnik
        self.voltage_chart_widget = VoltageChartWidget()
        self.current_chart_widget = CurrentChartWidget()
        self.temperature_chart_widget = TemperatureChartWidget()

        # Dodajemo About akciju
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.do_about)
        self.add_action(about_action)

        self.indicator = None


    def do_activate(self):
        window = Adw.ApplicationWindow(application=self)
        window.set_default_size(400, 400)

        # Header bar sa menijem i naslovom
        header_bar = Adw.HeaderBar()

        # Menu button (hamburger)
        menu_button = Gtk.MenuButton()
        icon = Gtk.Image()
        icon.set_from_icon_name("open-menu-symbolic")
        menu_button.set_child(icon)
        header_bar.pack_end(menu_button)

        # Popover menu sa About akcijom
        popover_menu = Gio.Menu()
        popover_menu.append("About", "app.about")
        menu_button.set_menu_model(popover_menu)

        # Naslov u centru
        title_label = Gtk.Label(label="Battmon")
        title_label.set_css_classes(["title"])
        header_bar.set_title_widget(title_label)

        # Glavni box za header i sadržaj
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        window.set_content(main_box)

        # Dodajemo header bar u glavni box
        main_box.append(header_bar)

        notebook = Gtk.Notebook()
        main_box.append(notebook)

        main_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        main_page.set_margin_top(10)  # Bez margine na vrhu
        main_page.set_margin_bottom(0)
        main_page.set_margin_start(0)
        main_page.set_margin_end(0)

        # Dodajemo scrollable window
        scroll_window = Gtk.ScrolledWindow()
        scroll_window.set_vexpand(True)  # Omogućava vertikalno širenje
        scroll_window.set_hexpand(True)  # Omogućava horizontalno širenje
        main_page.append(scroll_window)

        # Glavni sadržaj
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        content_box.set_margin_top(0)  # Bez margine na vrhu
        content_box.set_margin_bottom(20)
        content_box.set_margin_start(20)
        content_box.set_margin_end(20)
        scroll_window.set_child(content_box)

        # Dodajemo ikonu baterije iznad Battery Health labela
        battery_icon = Gtk.Image()
        battery_icon.set_from_icon_name("battery")
        battery_icon.set_icon_size(Gtk.IconSize.LARGE)
        battery_icon.set_vexpand(False)
        content_box.append(battery_icon)

        # Naslov za Battery Health
        battery_health_title = Gtk.Label(label="Battery Health")
        battery_health_title.set_css_classes(["title-label"])
        battery_health_title.set_halign(Gtk.Align.CENTER)
        content_box.append(battery_health_title)

        # Kreiranje BatteryHealthWidget i dodajemo ga u content_box
        self.battery_health_widget = BatteryHealthWidget()
        content_box.append(self.battery_health_widget)

        # Inicijalizuj labels i kreiraj vrednosne okvire
        self.labels = {
            "Manufacturer": Gtk.Label(label="Manufacturer"),
            "Percentage": Gtk.Label(label="Percentage"),
            "Status": Gtk.Label(label="Status"),
            "Time to Full/Empty": Gtk.Label(label="Time to Full/Empty"),
            "Temperature": Gtk.Label(label="Temperature"),
            "Voltage": Gtk.Label(label="Voltage"),
            "Current": Gtk.Label(label="Current")
        }
        self.create_value_boxes(content_box)

        graph_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        graph_page.set_margin_top(10)  # Bez margine na vrhu
        graph_page.set_margin_bottom(0)
        graph_page.set_margin_start(10)
        graph_page.set_margin_end(10)

        # Dodavanje VoltageChartWidget u content_box
        self.voltage_chart_widget.set_voltage_data([0])  # Inicijalizuj sa nekim podacima
        voltage_graph_label = Gtk.Label(label="Voltage")
        voltage_graph_label.set_css_classes(["title-label"])
        graph_page.append(voltage_graph_label)
        graph_page.append(self.voltage_chart_widget)

        # Dodavanje VoltageChartWidget u content_box
        self.current_chart_widget.set_current_data([0])  # Inicijalizuj sa nekim podacima
        current_graph_label = Gtk.Label(label="Current")
        current_graph_label.set_css_classes(["title-label"])
        graph_page.append(current_graph_label)
        graph_page.append(self.current_chart_widget)

        self.temperature_chart_widget.set_temperature_data([0])  # Inicijalizuj sa nekim podacima
        temperature_graph_label = Gtk.Label(label="Temperature")
        temperature_graph_label.set_css_classes(["title-label"])
        graph_page.append(temperature_graph_label)
        graph_page.append(self.temperature_chart_widget)

        self.apply_styles()

        notebook.append_page(main_page, Gtk.Label(label="Main"))
        notebook.append_page(graph_page, Gtk.Label(label="Graphs"))


        window.present()

        # Start updating battery data
        GLib.timeout_add_seconds(5, self.update_battery_data)

    def create_value_boxes(self, box):
        for title, label in self.labels.items():
            title_label = Gtk.Label(label=title)
            title_label.set_css_classes(["title-label"])
            box.append(title_label)

            if title == "Manufacturer":
                label.set_css_classes(["manufacturer-label"])
            else:
                label.set_css_classes(["value-label"])
            box.append(label)

    def apply_styles(self):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
        .title-label {
            font-size: 20px;
            text-align: center; 
        }
        .manufacturer-label {
            font-size: 24px;
            text-align: center;
            font-weight: bold;
        }
        .value-label {
            font-size: 26px;
            font-weight: bold;
            text-align: center;
        }
        .title {
            font-size: 24px;
            font-weight: bold;
        }
        """)

        display = Gdk.Display.get_default()
        Gtk.StyleContext.add_provider_for_display(
            display, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

    def update_battery_data(self):
        # Čitanje podataka iz sistema (primer kako bi moglo izgledati)
        manufacturer = self.read_battery_status("/sys/class/power_supply/bq27411-0/manufacturer")
        technology = self.read_battery_status("/sys/class/power_supply/bq27411-0/technology")
        charge_now = self.read_battery_value("/sys/class/power_supply/bq27411-0/charge_now")
        charge_full = self.read_battery_value("/sys/class/power_supply/bq27411-0/charge_full")
        charge_full_design = self.read_battery_value("/sys/class/power_supply/bq27411-0/charge_full_design")
        voltage = self.read_battery_value("/sys/class/power_supply/bq27411-0/voltage_now") / 1000000
        current_now = self.read_battery_value("/sys/class/power_supply/bq27411-0/current_now")

        temp = self.read_battery_value("/sys/class/power_supply/bq27411-0/temp") / 10.0
        status = self.read_battery_status("/sys/class/power_supply/bq27411-0/status")

        # Pretpostavimo da je maksimalni kapacitet baterije 3000 mAh
        max_capacity = 3000

        # Ažuriraj vrednosti na ekranu
        percentage = (charge_now / max_capacity) / 10

        # if percentage <= 20:
        #     self.send_notification("Battery to low", f"Battery is on {int(percentage)}%.")
        self.labels["Manufacturer"].set_text(f"{manufacturer} ({technology})")
        self.labels["Percentage"].set_text(f"{percentage:.1f}%")
        self.labels["Status"].set_text(status)

        # Provera da li se baterija puni
        if status == "Charging" and current_now != 0:
            time_to_full = abs((charge_full - charge_now) / current_now)
            hours = int(time_to_full)
            minutes = int((time_to_full * 60) % 60)
            self.labels["Time to Full/Empty"].set_text(f"{hours}h {minutes}m to full")
        elif current_now != 0:
            time_to_empty = abs(charge_now / current_now)
            hours = int(time_to_empty)
            minutes = int((time_to_empty * 60) % 60)
            self.labels["Time to Full/Empty"].set_text(f"{hours}h {minutes}m to empty")
        else:
            self.labels["Time to Full/Empty"].set_text("Calculating...")

        self.labels["Temperature"].set_text(f"{temp:.1f}°C")
        self.labels["Voltage"].set_text(f"{voltage:.2f}V")
        self.labels["Current"].set_text(f"{current_now / 1000:.2f}mA")

        # Izračunavanje zdravlja baterije
        health_percentage = (charge_full / charge_full_design) * 100
        self.battery_health_widget.set_health_percentage(health_percentage)

        # Dodajte nove podatke u grafikon
        self.voltage_chart_widget.set_voltage_data([voltage])
        self.current_chart_widget.set_current_data([current_now / 1000]) 
        self.temperature_chart_widget.set_temperature_data([temp]) 

        return True

    def read_battery_status(self, path):
        try:
            with open(path, 'r') as file:
                return file.read().strip()
        except FileNotFoundError:
            return "Unknown"

    def read_battery_value(self, path):
        try:    
            with open(path, 'r') as file:
                return int(file.read().strip())
        except FileNotFoundError:
            return 0

    def do_about(self, action, param):
        about_dialog = Gtk.AboutDialog()
        about_dialog.set_program_name("Battery Monitor")
        about_dialog.set_version("1.0")
        # about_dialog.set_license_type(Gtk.License.MIT)
        about_dialog.set_comments("A simple battery monitoring application.")
        
        # Dodavanje ikone baterije u About dijalog
        # icon = Gtk.Image()
        # icon.new_from_icon_name("battery")
        # icon.set_icon_size(Gtk.IconSize.LARGE)
        about_dialog.set_logo_icon_name("battery")
        
        about_dialog.show()

if __name__ == "__main__":
    app = BatteryMonitorApp()
    app.run()