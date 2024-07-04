import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import requests
import os


def download_browser(url, save_path, filename):
    file_path = os.path.join(save_path, filename)

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = int(r.headers.get('content-length', 0))
            downloaded_size = 0

            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        progress_var.set(downloaded_size / total_size * 100)
                        root.update_idletasks()

        messagebox.showinfo("Загрузка завершена", f"Файл {filename} был успешно загружен в {save_path}.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка при загрузке: {e}")


def start_download():
    browser = browser_var.get()
    folder_selected = filedialog.askdirectory()
    if not folder_selected:
        return  # Если папка не выбрана, выйти из функции

    urls = {
        "Chrome": ("https://dl.google.com/chrome/install/standalonesetup64.exe", "chrome_installer.exe"),
        "Mozilla Firefox": (
        "https://download.mozilla.org/?product=firefox-latest-ssl&os=win&lang=ru", "firefox_installer.exe"),
        "Opera": ("https://download3.operacdn.com/pub/opera/desktop/79.0.4143.22/win/Opera_79.0.4143.22_Setup_x64.exe",
                  "opera_installer.exe")
    }

    if browser in urls:
        url, filename = urls[browser]
        download_browser(url, folder_selected, filename)


def create_gui():
    global root, browser_var, progress_var

    root = tk.Tk()
    root.title("offach's installer")

    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(padx=10, pady=10)

    label = tk.Label(frame, text="Выберите браузер для загрузки", pady=10)
    label.pack()

    browser_var = tk.StringVar(value="Chrome")
    browsers = ["Chrome", "Mozilla Firefox", "Opera"]

    for browser in browsers:
        rb = tk.Radiobutton(frame, text=browser, variable=browser_var, value=browser)
        rb.pack(anchor=tk.W)

    download_button = tk.Button(frame, text="Скачать выбранный браузер", command=start_download)
    download_button.pack(pady=10)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(frame, variable=progress_var, maximum=100)
    progress_bar.pack(fill=tk.X, pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
