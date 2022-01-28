from tkinter import Frame, Label, Entry


def create_label(frame: Frame, text: str, row: int, col: int) -> Label:
    lbl = Label(frame, text=text)
    lbl.grid(row=row, column=col)
    return lbl


def create_entry(frame: Frame, text: str, row: int, col: int, value: any, index: int = 0) -> Entry:
    entry = Entry(frame, text=text)
    entry.insert(index=index, string=value)
    entry.grid(row=row, column=col)
    return entry
