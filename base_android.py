# main.py
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.toast import toast
import json, os, math
from datetime import datetime
import webbrowser

# Set mobile preview size (optional)
Window.size = (360, 640)

KV = '''
BoxLayout:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)

    MDDataTable:
        id: overall_table
        size_hint: None, None
        size: dp(340), dp(40)
        column_data: [
            ("Attended", dp(100)),
            ("Total", dp(100)),
            ("%", dp(100))
        ]
        row_data: []
        use_pagination: False
        elevation: 2

    MDTextField:
        id: entry_total
        hint_text: "Today's Lectures"
        input_filter: 'int'
        size_hint_x: None
        width: dp(150)
    MDTextField:
        id: entry_attended
        hint_text: "Attended"
        input_filter: 'int'
        size_hint_x: None
        width: dp(150)
    MDTextField:
        id: entry_future
        hint_text: "Next Day Lectures"
        input_filter: 'int'
        size_hint_x: None
        width: dp(150)

    BoxLayout:
        size_hint_y: None
        height: dp(40)
        spacing: dp(10)
        MDFlatButton:
            text: "Calculate"
            on_release: app.calculate()
        MDFlatButton:
            text: "Save Record"
            on_release: app.add_record()

    MDLabel:
        id: label_today
        text: "Today: --%"
        halign: 'center'
        theme_text_color: 'Primary'
    MDLabel:
        id: label_bunks
        text: "Bunks Possible: --"
        halign: 'center'

    MDDataTable:
        id: history_table
        size_hint: None, None
        size: dp(340), dp(300)
        column_data: [
            ("Date", dp(60)),
            ("Attended", dp(70)),
            ("Total", dp(70)),
            ("%", dp(70))
        ]
        row_data: []
        elevation: 2

    BoxLayout:
        size_hint_y: None
        height: dp(30)
        MDLabel:
            text: "Made by Swaraj - "
            font_style: 'Caption'
            halign: 'right'
        MDLabel:
            text: "GitHub"
            theme_text_color: 'Custom'
            text_color: app.link_color
            font_style: 'Caption'
            on_touch_down: app.open_link()
'''

class AttendanceApp(MDApp):
    link_color = (0,0,1,1)
    DATA_FILE = 'attendance_data.json'

    def build(self):
        self.history = []
        if os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE) as f:
                self.history = json.load(f)
        return Builder.load_string(KV)

    def get_cumulative(self):
        s = sum(item['total'] for item in self.history)
        a = sum(item['attended'] for item in self.history)
        p = (a/s)*100 if s>0 else 0
        return a, s, p

    def save_data(self):
        with open(self.DATA_FILE, 'w') as f:
            json.dump(self.history, f)

    def refresh_tables(self):
        a, s, p = self.get_cumulative()
        self.root.ids.overall_table.row_data = [(str(a), str(s), f"{p:.2f}%")]

        rows = []
        for itm in self.history:
            d = datetime.strptime(itm['date'], '%Y-%m-%d').strftime('%d%m%Y')
            t = itm['total']; at = itm['attended']
            pct = (at/t)*100
            rows.append((d, str(at), str(t), f"{pct:.2f}%"))
        self.root.ids.history_table.row_data = rows

    def calculate(self):
        try:
            total = int(self.root.ids.entry_total.text)
            attended = int(self.root.ids.entry_attended.text)
        except:
            toast("Enter valid integers!")
            return
        pct = (attended/total)*100
        self.root.ids.label_today.text = f"Today: {pct:.2f}%"
        N = int(self.root.ids.entry_future.text or 0)
        a,s,_ = self.get_cumulative()
        req = 0.75*(s+total+N)
        mf = math.ceil(req-(a+attended))
        bunk = max(0, N-mf)
        self.root.ids.label_bunks.text = f"Bunks Possible: {bunk}/{N}"

    def add_record(self):
        try:
            total = int(self.root.ids.entry_total.text)
            attended = int(self.root.ids.entry_attended.text)
        except:
            toast("Calculate first!")
            return
        self.history.append({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'total': total, 'attended': attended
        })
        self.save_data()
        self.refresh_tables()
        toast("Record added!")

    def open_link(self):
        webbrowser.open("https://github.com/Swaraj-SG")

if __name__ == '__main__':
    AttendanceApp().run()

