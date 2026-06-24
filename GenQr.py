from tkinter import *
from tkinter import messagebox
import os
from PIL import Image, ImageTk, ImageDraw
import qrcode

#img = Image.open("GenQr.png")
#img.save("GenQr.ico")
#root.iconbitmap("GenQr.ico")
qr_image = None
generated_img = None

# ---------- THEME / TYPOGRAPHY ----------
PRIMARY_FG = "#f8fafc"
ACCENT = "#60a5fa"
TEXT_FG = "#e2e8f0"
PLACEHOLDER_FG = "#94a3b8"
PANEL_BG = "#111827"
ENTRY_BG = "#0f172a"
ENTRY_HIGHLIGHT_BG = "#1e293b"

HEADING_FONT = ("Segoe UI", 26, "bold")
LABEL_FONT = ("Segoe UI", 14)
ENTRY_FONT = ("Segoe UI", 14)
BTN_FONT = ("Segoe UI", 12, "bold")
RESULT_FONT = ("Segoe UI", 12, "bold")
FOOTER_FONT = ("Segoe UI", 10)

# ---------------- WINDOW ----------------
root = Tk()
root.title("GENERATE YOUR QR")
root.geometry("500x550")
root.configure(bg=ENTRY_BG)

# ---------------- PLACEHOLDER FUNCTION ----------------
def add_placeholder(entry, text):
    entry.insert(0, text)
    entry.config(fg=PLACEHOLDER_FG)

    def on_focus_in(event):
        if entry.get() == text:
            entry.delete(0, END)
            entry.config(fg=TEXT_FG)

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg=PLACEHOLDER_FG)

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# ---------------- GENERATE QR ----------------
def generate_qr():
    global qr_image, generated_img

    data = txt.get().strip()

    if data == "" or data == "Enter URL here":
        messagebox.showerror(
            "Error",
            "Please enter text or URL."
        )
        return

    try:
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )

        qr.add_data(data)
        qr.make(fit=True)

        generated_img = qr.make_image(
            fill_color="black",
            back_color="white"
        ).convert("RGB")

        display_img = generated_img.resize((200, 200))

        qr_image = ImageTk.PhotoImage(display_img)

        qr_label.config(image=qr_image)
        qr_label.image = qr_image

        result.config(
            text="✅ QR Code Generated Successfully"
        )

    except Exception as e:
        messagebox.showerror(
            "Error",
            str(e)
        )

# ---------------- SAVE QR ----------------
def save_qr():
    global generated_img

    if generated_img is None:
        messagebox.showwarning(
            "Warning",
            "Generate a QR code first."
        )
        return

    filename = "my_qrcode.png"

    generated_img.save(filename)

    messagebox.showinfo(
        "Saved",
        f"QR Code saved as:\n{os.path.abspath(filename)}"
    )

# ---------------- CLEAR ----------------
def clear_fields():
    global generated_img

    txt.delete(0, END)
    add_placeholder(txt, "Enter URL here")

    qr_label.config(image="")
    qr_label.image = None

    generated_img = None

    result.config(
        text="Your QR code information will appear here."
    )

# ---------------- HEADING ----------------
heading = Label(
    root,
    text="GenQr",
    font=HEADING_FONT,
    bg=ENTRY_BG,
    fg=PRIMARY_FG
)

heading.pack(pady=(18, 10))

# ---------------- NOTE ----------------
# Removed the enclosing gray Frame so the background image fills the app.
# Widgets below are parented to `root` so the image shows across the window.

# ---------------- BACKGROUND & ICON SETUP ----------------
def setup_background_and_icon():
    import os
    base = os.path.dirname(__file__)
    # Prefer files named 'background*' then fall back to 'genqr*'
    candidates = [f for f in os.listdir(base) if f.lower().startswith("background") and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico'))]
    if not candidates:
        candidates = [f for f in os.listdir(base) if f.lower().startswith("genqr") and f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.ico'))]
    if not candidates:
        return

    img_path = os.path.join(base, candidates[0])
    try:
        pil_img = Image.open(img_path).convert("RGBA")
    except Exception:
        return

    # set window icon (small square)
    try:
        icon_img = pil_img.resize((64, 64), Image.LANCZOS)
        icon = ImageTk.PhotoImage(icon_img)
        root.iconphoto(False, icon)
        root._icon_img = icon
    except Exception:
        pass

    # background label on root and dynamic resize handler
    bg_label = Label(root)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    root._bg_label = bg_label
    root._bg_pil = pil_img

    def _resize_bg(event=None):
        try:
            w = root.winfo_width()
            h = root.winfo_height()
            if w <= 1 or h <= 1:
                return
            resized = root._bg_pil.resize((w, h), Image.LANCZOS)
            bg_photo = ImageTk.PhotoImage(resized)
            bg_label.config(image=bg_photo)
            bg_label.image = bg_photo
            bg_label.lower()
        except Exception:
            pass

    root.bind("<Configure>", _resize_bg)
    root.after(50, _resize_bg)

# setup_background_and_icon()  # Disabled: using solid background color instead

# ---------------- LIGHT CENTER PANEL ----------------
def setup_light_panel():
    panel_label = Label(root)
    root._panel_label = panel_label

    def _resize_panel(event=None):
        try:
            w = root.winfo_width()
            h = root.winfo_height()
            if w <= 1 or h <= 1:
                return
            panel_w = min(460, int(w * 0.94))
            panel_h = 320
            x = (w - panel_w) // 2
            y = 80
            # dark translucent panel for the dark theme
            panel_img = Image.new("RGBA", (panel_w, panel_h), (15, 23, 42, 220))
            mask = Image.new("L", (panel_w, panel_h), 0)
            draw = ImageDraw.Draw(mask)
            r = 20
            draw.rounded_rectangle((0, 0, panel_w, panel_h), radius=r, fill=255)
            panel_img.putalpha(mask)
            panel_photo = ImageTk.PhotoImage(panel_img)
            panel_label.config(image=panel_photo)
            panel_label.image = panel_photo
            panel_label.place(x=x, y=y)
            # ensure panel is above background and below widgets
            try:
                panel_label.lift(root._bg_label)
                for wgt in (heading, subtitle_label, txt, button_frame, qr_label, result, footer):
                    try:
                        wgt.lift(panel_label)
                    except Exception:
                        pass
            except Exception:
                pass
        except Exception:
            pass

    root.bind("<Configure>", _resize_panel)
    root.after(50, _resize_panel)

# setup_light_panel()  # Disabled: using solid background color instead

# ---------------- LABEL ----------------
subtitle_label = Label(
    root,
    text="Enter text or url to generate code",
    font=LABEL_FONT,
    bg=ENTRY_BG,
    fg=PRIMARY_FG
)
subtitle_label.pack(pady=(8, 12))

# ---------------- ENTRY ----------------
txt = Entry(
    root,
    font=ENTRY_FONT,
    justify="center",
    width=34,
    bg=ENTRY_BG,
    fg=TEXT_FG,
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=ENTRY_HIGHLIGHT_BG,
    highlightcolor=ACCENT,
    insertbackground=TEXT_FG
)

add_placeholder(txt, "Enter URL here")

txt.pack(
    ipady=6,
    pady=(6, 14)
)

# ---------------- BUTTON FRAME ----------------
button_frame = Frame(
    root,
    bg=ENTRY_BG,
)
button_frame.pack(pady=12)

# Common button style
btn_width = 140
btn_height = 40
btn_radius = 20

# Rounded button helper

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb


def darken_color(hex_color, factor=0.09):
    r, g, b = hex_to_rgb(hex_color)
    return rgb_to_hex(
        (max(0, int(r * (1 - factor))),
         max(0, int(g * (1 - factor))),
         max(0, int(b * (1 - factor))))
    )


class RoundedButton(Canvas):
    def __init__(self, master, text, command=None, bg=ACCENT, fg="white", width=140, height=44, radius=18, font=None, **kwargs):
        super().__init__(master, width=width, height=height, bg=master.cget("bg"), highlightthickness=0, bd=0, **kwargs)
        self.command = command
        self.normal_bg = bg
        self.hover_bg = darken_color(bg)
        self.radius = radius
        self.fg = fg
        self.text = text
        self.font = font
        self.configure(cursor="hand2")

        self.round_rect = self.create_round_rect(2, 2, width - 2, height - 2, radius, fill=bg, outline="")
        self.text_id = self.create_text(width // 2, height // 2, text=text, fill=fg, font=font)

        # raise main rect and text
        self.tag_raise(self.round_rect)
        self.tag_raise(self.text_id)

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.tag_bind(self.round_rect, "<Enter>", self.on_enter)
        self.tag_bind(self.round_rect, "<Leave>", self.on_leave)
        self.tag_bind(self.text_id, "<Enter>", self.on_enter)
        self.tag_bind(self.text_id, "<Leave>", self.on_leave)
        self.tag_bind(self.round_rect, "<Button-1>", self.on_click)
        self.tag_bind(self.text_id, "<Button-1>", self.on_click)

    def create_round_rect(self, x1, y1, x2, y2, r, **kwargs):
        points = [
            x1 + r, y1,
            x2 - r, y1,
            x2, y1,
            x2, y1 + r,
            x2, y2 - r,
            x2, y2,
            x2 - r, y2,
            x1 + r, y2,
            x1, y2,
            x1, y2 - r,
            x1, y1 + r,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, splinesteps=36, **kwargs)

    def on_enter(self, event=None):
        # animated transition to hover color
        try:
            self._animate_fill(self.normal_bg, self.hover_bg)
        except Exception:
            self.itemconfig(self.round_rect, fill=self.hover_bg)

    def on_leave(self, event=None):
        try:
            self._animate_fill(self.hover_bg, self.normal_bg)
        except Exception:
            self.itemconfig(self.round_rect, fill=self.normal_bg)

    def on_click(self, event=None):
        if self.command:
            self.command()

    def set_colors(self, bg, fg):
        self.normal_bg = bg
        self.hover_bg = darken_color(bg)
        self.fg = fg
        self.itemconfig(self.round_rect, fill=self.normal_bg)
        self.itemconfig(self.text_id, fill=self.fg)

    def _animate_fill(self, start_hex, end_hex, steps=6, delay=20):
        # interpolate RGB values
        start_rgb = hex_to_rgb(start_hex)
        end_rgb = hex_to_rgb(end_hex)
        dr = (end_rgb[0] - start_rgb[0]) / steps
        dg = (end_rgb[1] - start_rgb[1]) / steps
        db = (end_rgb[2] - start_rgb[2]) / steps

        def step(i, r, g, b):
            if i > steps:
                return
            nr = int(start_rgb[0] + dr * i)
            ng = int(start_rgb[1] + dg * i)
            nb = int(start_rgb[2] + db * i)
            self.itemconfig(self.round_rect, fill=rgb_to_hex((nr, ng, nb)))
            self.after(delay, lambda: step(i + 1, nr, ng, nb))

        step(1, *start_rgb)


# ---------------- GENERATE BUTTON ----------------
generate_btn = RoundedButton(
    button_frame,
    text="⚡ Generate QR",
    command=generate_qr,
    bg=ACCENT,
    fg="white",
    width=btn_width,
    height=btn_height,
    radius=btn_radius,
    font=BTN_FONT
)
generate_btn.grid(row=0, column=0, padx=8)

# ---------------- CLEAR BUTTON ----------------
clear_btn = RoundedButton(
    button_frame,
    text="🗑 Clear",
    command=clear_fields,
    bg=ACCENT,
    fg="white",
    width=btn_width,
    height=btn_height,
    radius=btn_radius,
    font=BTN_FONT
)
clear_btn.grid(row=0, column=1, padx=8)

# ---------------- SAVE BUTTON ----------------
save_btn = RoundedButton(
    button_frame,
    text="💾 Save QR",
    command=save_qr,
    bg=ACCENT,
    fg="white",
    width=btn_width,
    height=btn_height,
    radius=btn_radius,
    font=BTN_FONT
)
save_btn.grid(row=0, column=2, padx=8)
# ---------------- RESULT ----------------
qr_label = Label(
    root,
    bg=ENTRY_BG
)

qr_label.pack(pady=10)

result = Label(
    root,
    text="Your QR code information will appear here.",
    font=RESULT_FONT,
    bg=ENTRY_BG,
    fg=ACCENT,
    wraplength=400,
    justify="center"
)

result.pack(pady=20)

# ---------------- FOOTER ----------------
footer = Label(
    root,
    text="TriGen product",
    font=FOOTER_FONT,
    bg=ENTRY_BG,
    fg=PLACEHOLDER_FG
)

footer.pack(
    side=BOTTOM,
    pady=10
)

# ---------------- MAIN LOOP ----------------
root.mainloop()