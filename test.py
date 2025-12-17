import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

# ================= COLORS =================
CITI_BLUE = "#003B70"
CITI_BLUE_DARK = "#002A4E"
CITI_RED = "#EE1C25"
WHITE = "#FFFFFF"
BG = "#F8FAFC"
TEXT = "#0F172A"
MUTED = "#475569"

SUBMIT_BG = "#0B5ED7"
SUBMIT_HOVER = "#0A58CA"

GREEN_BG = "#5FB878"
GREEN_HOVER = "#4FA96A"

SECONDARY_HOVER_BG = "#EEF2F7"

# ================= COLOR ANIMATION HELPERS =================
def hex_to_rgb(h):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

def rgb_to_hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def lerp(a, b, t):
    return int(a + (b - a) * t)

def lerp_color(c1, c2, t):
    r1, g1, b1 = hex_to_rgb(c1)
    r2, g2, b2 = hex_to_rgb(c2)
    return rgb_to_hex((lerp(r1, r2, t), lerp(g1, g2, t), lerp(b1, b2, t)))

# ================= ANIMATED BUTTON =================
class AnimatedButton(tk.Button):
    def __init__(self, master, normal_bg, hover_bg, **kwargs):
        super().__init__(
            master,
            bg=normal_bg,
            fg=WHITE,
            activebackground=hover_bg,
            activeforeground=WHITE,
            bd=0,
            **kwargs
        )
        self.normal_bg = normal_bg
        self.hover_bg = hover_bg
        self.t = 0
        self.after_id = None
        self.bind("<Enter>", lambda e: self.animate(1))
        self.bind("<Leave>", lambda e: self.animate(0))

    def animate(self, target):
        if self.after_id:
            self.after_cancel(self.after_id)
        self.step(target)

    def step(self, target):
        if abs(self.t - target) < 0.01:
            self.t = target
            self.configure(bg=lerp_color(self.normal_bg, self.hover_bg, self.t))
            return
        self.t += 0.1 if self.t < target else -0.1
        self.configure(bg=lerp_color(self.normal_bg, self.hover_bg, self.t))
        self.after_id = self.after(15, lambda: self.step(target))

# ================= SECONDARY BUTTON WRAPPER =================
class HoverFrameButton(tk.Frame):
    def __init__(self, master, text, command):
        super().__init__(master, bg=WHITE)
        self.btn = ttk.Button(self, text=text, command=command)
        self.btn.pack(ipadx=6, ipady=2)
        self.bind("<Enter>", lambda e: self.config(bg=SECONDARY_HOVER_BG))
        self.bind("<Leave>", lambda e: self.config(bg=WHITE))
        self.btn.bind("<Enter>", lambda e: self.config(bg=SECONDARY_HOVER_BG))
        self.btn.bind("<Leave>", lambda e: self.config(bg=WHITE))

# ================= MAIN APP =================
class ScenarioManagerTool(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Scenario Manager Tool")
        self.geometry("780x500")
        self.configure(bg=BG)
        self.attributes("-alpha", 1.0)

        self._style()
        self._ui()

    def _style(self):
        style = ttk.Style(self)
        style.theme_use("vista" if "vista" in style.theme_names() else "clam")
        style.configure("TLabel", font=("Segoe UI", 11))
        style.configure("Citi.TEntry", padding=7)

    def _ui(self):
        # ===== HEADER =====
        header = tk.Frame(self, bg=CITI_BLUE, height=90)
        header.pack(fill="x")
        header.pack_propagate(False)

        self.logo_img = tk.PhotoImage(file="citi_logo.png")
        tk.Label(header, image=self.logo_img, bg=CITI_BLUE)\
            .place(x=12, rely=0.35, anchor="w")

        tk.Label(
            header,
            text="Scenario Manager Tool",
            bg=CITI_BLUE,
            fg=WHITE,
            font=("Segoe UI", 13, "bold"),
        ).place(x=12, rely=0.72, anchor="w")

        tk.Frame(self, bg=CITI_RED, height=3).pack(fill="x")

        # ===== CARD =====
        card = tk.Frame(self, bg=WHITE)
        card.pack(fill="both", expand=True, padx=26, pady=20)

        tk.Label(card, text="User Details", bg=WHITE, fg=CITI_BLUE,
                 font=("Segoe UI", 22, "bold"))\
            .grid(row=0, column=0, columnspan=2, sticky="w", padx=22)

        tk.Label(card, text="Please complete the fields below.",
                 bg=WHITE, fg=MUTED, font=("Segoe UI", 12))\
            .grid(row=1, column=0, columnspan=2, sticky="w", padx=22, pady=(0, 16))

        ttk.Separator(card).grid(row=2, column=0, columnspan=2, sticky="ew", padx=22)

        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.email = tk.StringVar()

        fields = [
            ("First name", self.first_name),
            ("Last name", self.last_name),
            ("Email", self.email),
        ]

        for i, (label, var) in enumerate(fields, start=3):
            tk.Label(card, text=label, bg=WHITE, fg=CITI_BLUE_DARK,
                     font=("Segoe UI", 12))\
                .grid(row=i, column=0, sticky="w", padx=22, pady=10)

            ttk.Entry(card, textvariable=var, style="Citi.TEntry")\
                .grid(row=i, column=1, sticky="ew", padx=(10, 22), pady=10)

        card.columnconfigure(1, weight=1)

        ttk.Separator(card).grid(row=6, column=0, columnspan=2, sticky="ew", padx=22, pady=18)

        contact = tk.Label(
            card, text="Contact us", bg=WHITE, fg="#0B5ED7",
            cursor="hand2", font=("Segoe UI", 11, "underline")
        )
        contact.grid(row=7, column=0, sticky="w", padx=22)
        contact.bind("<Button-1>", lambda e: webbrowser.open("mailto:tv@citi.com"))

        # ===== BUTTONS =====
        btns = tk.Frame(card, bg=WHITE)
        btns.grid(row=8, column=0, columnspan=2, sticky="e", padx=22, pady=20)

        AnimatedButton(
            btns, GREEN_BG, GREEN_HOVER,
            text="Example", font=("Segoe UI", 12, "bold"),
            padx=26, pady=10, command=self.fill_example
        ).grid(row=0, column=0, padx=8)

        AnimatedButton(
            btns, SUBMIT_BG, SUBMIT_HOVER,
            text="Submit", font=("Segoe UI", 12, "bold"),
            padx=26, pady=10, command=self.submit
        ).grid(row=0, column=1, padx=8)

        HoverFrameButton(btns, "Clear", self.clear)\
            .grid(row=0, column=2, padx=8)

        HoverFrameButton(btns, "Exit", self.destroy)\
            .grid(row=0, column=3, padx=8)

    # ===== ACTIONS =====
    def fill_example(self):
        self.first_name.set("Test")
        self.last_name.set("User")
        self.email.set("test.user@citi.com")

    def submit(self):
        if not all([self.first_name.get(), self.last_name.get(), self.email.get()]):
            messagebox.showwarning("Missing data", "Please fill in all fields.")
            return
        messagebox.showinfo("Submitted", "Scenario data submitted successfully.")

    def clear(self):
        self.first_name.set("")
        self.last_name.set("")
        self.email.set("")


if __name__ == "__main__":
    ScenarioManagerTool().mainloop()
