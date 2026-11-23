#!/usr/bin/env python3
"""Generate and display a one-task password for the user to enter manually.

This tool never fills or submits a browser form and never writes the generated
value to stdout, the clipboard, files, or logs.
"""

from __future__ import annotations

import argparse
import secrets
import string
import tkinter as tk
from tkinter import ttk


def generate_password(length: int = 24) -> str:
    if length < 16 or length > 128:
        raise ValueError("password length must be between 16 and 128")
    groups = (string.ascii_lowercase, string.ascii_uppercase, string.digits, "!@#$%^&*()-_=+")
    chars = [secrets.choice(group) for group in groups]
    alphabet = "".join(groups)
    chars.extend(secrets.choice(alphabet) for _ in range(length - len(chars)))
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


class PasswordHandoff:
    def __init__(self, length: int, timeout: int) -> None:
        self.root = tk.Tk()
        self.root.title("Одноразовый пароль MyMeet")
        self.root.resizable(False, False)
        self.secret = generate_password(length)
        self.timeout = timeout

        frame = ttk.Frame(self.root, padding=16)
        frame.grid(sticky="nsew")
        ttk.Label(frame, text="Перепишите пароль в форму MyMeet самостоятельно:").grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        self.value = tk.StringVar(value=self.secret)
        entry = ttk.Entry(frame, textvariable=self.value, width=44, state="readonly", font=("Menlo", 13))
        entry.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        entry.selection_range(0, tk.END)

        ttk.Button(frame, text="Сгенерировать новый", command=self.regenerate).grid(row=2, column=0, sticky="w")
        ttk.Button(frame, text="Закрыть", command=self.close).grid(row=2, column=1, sticky="e")
        ttk.Label(frame, text=f"Окно закроется через {timeout} секунд. Пароль нигде не сохраняется.").grid(row=3, column=0, columnspan=2, sticky="w", pady=(10, 0))

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.after(timeout * 1000, self.close)

    def regenerate(self) -> None:
        self.secret = generate_password(len(self.secret))
        self.value.set(self.secret)

    def close(self) -> None:
        self.value.set("")
        self.secret = ""
        self.root.destroy()

    def run(self) -> None:
        self.root.mainloop()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--length", type=int, default=24, help="password length, 16–128 characters (default: 24)")
    parser.add_argument("--timeout", type=int, default=300, help="close the display after this many seconds (default: 300)")
    args = parser.parse_args()
    if args.timeout < 30 or args.timeout > 1800:
        parser.error("timeout must be between 30 and 1800 seconds")
    if not 16 <= args.length <= 128:
        parser.error("password length must be between 16 and 128")
    PasswordHandoff(args.length, args.timeout).run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
