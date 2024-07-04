import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import requests
import os
import threading
import time

class DownloadManager:
    def __init__(self, master):
        self.master = master
        self.current_index = 0
        self.selected_options = []
        self.save_path = ""
        self.downloaded_files = []
        self.urls = {
            "Google Chrome": ("https://dl.google.com/chrome/install/375.126/chrome_installer.exe", "chrome_installer.exe"),
            "Mozilla Firefox": ("https://download.mozilla.org/?product=firefox-stub&os=win&lang=ru", "firefox_installer.exe"),
            "Yandex": ("https://browser.yandex.ru/download/?noredirect=1&banerid=1110000", "yandex_installer.exe"),
            "Opera": ("https://download1.operacdn.com/pub/opera/desktop/99.0.4788.31/win/Opera_99.0.4788.31_Setup.exe", "opera_installer.exe"),
            "Discord": ("https://discord.com/api/download?platform=win", "discord_installer.exe"),
            "Skype": ("https://go.skype.com/windows.desktop.download", "skype_installer.exe"),
            "Telegram Desktop": ("https://updates.tdesktop.com/tsetup/tsetup.4.8.3.exe", "telegram_installer.exe"),
            "Zoom": ("https://zoom.us/client/latest/ZoomInstaller.exe", "zoom_installer.exe"),
            "WhatsApp Desktop": ("https://get.microsoft.com/installer/download/9NKSQGP7F2NH?cid=website_cta_psi", "whatsapp_installer.exe"),
            "Steam": ("https://cdn.cloudflare.steamstatic.com/client/installer/SteamSetup.exe", "steam_installer.exe"),
            "Epic Games Launcher": ("https://launcher-public-service-prod06.ol.epicgames.com/launcher/api/installer/download/EpicGamesLauncherInstaller.msi", "epic_games_installer.msi"),
            "EA Play": ("https://origin-a.akamaihd.net/Origin-Client-Download/origin/live/OriginSetup.exe", "ea_play_installer.exe"),
            "Ubisoft Connect": ("https://ubistatic3-a.akamaihd.net/orbit/launcher_installer/UplayInstaller.exe", "ubisoft_connect_installer.exe"),
            "Battle.net": ("https://www.battle.net/download/getInstallerForGame?os=win&version=Live&gameProgram=BATTLENET_APP", "battlenet_installer.exe"),
            "Visual Studio Code": ("https://update.code.visualstudio.com/latest/win32-x64-user/stable", "vscode_installer.exe"),
            "JetBrains IntelliJ IDEA": ("https://download.jetbrains.com/idea/ideaIU-2023.1.exe", "intellij_idea_installer.exe"),
            "PyCharm": ("https://download.jetbrains.com/python/pycharm-professional-2023.1.exe", "pycharm_installer.exe"),
            "Atom": ("https://github.com/atom/atom/releases/download/v1.58.0/AtomSetup-x64.exe", "atom_installer.exe"),
            "Sublime Text": ("https://download.sublimetext.com/Sublime%20Text%20Build%203211%20x64%20Setup.exe", "sublime_text_installer.exe"),
            "OBS Studio": ("https://cdn-fastly.obsproject.com/downloads/OBS-Studio-27.1.3-Full-Installer-x64.exe", "obs_studio_installer.exe"),
            "7-Zip": ("https://www.7-zip.org/a/7z2201-x64.exe", "7zip_installer.exe"),
            "Logitech G Hub": ("https://download01.logi.com/web/ftp/pub/techsupport/gaming/lghub_installer.exe", "logitech_g_hub_installer.exe"),
            "Razer Synapse": ("https://rzr.to/synapse-3-pc-download", "razer_synapse_installer.exe"),
            "MSI Dragon Center": ("https://download.msi.com/uti_exe/common/Dragon-Center.zip", "msi_dragon_center_installer.zip"),
            "Corsair iCUE": ("https://downloads.corsair.com/Files/CUE/iCUESetup_4.33.138_release.msi", "corsair_icue_installer.msi"),
            "SteelSeries Engine": ("https://engine.steelseriescdn.com/SteelSeriesGG44.0.0Setup.exe", "steelseries_engine_installer.exe")
        }

    def start_download(self):
        self.selected_options = [var.get() for var in all_vars if var.get()]
        if not self.selected_options:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите хотя бы один элемент для загрузки.")
            return

        folder_selected = filedialog.askdirectory()
        if not folder_selected:
            return  # Если папка не выбрана, выйти из функции

        self.save_path = os.path.join(folder_selected, "offach installer Загрузки")
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

        for widget in download_listbox.winfo_children():
            widget.destroy()
        for option in self.selected_options:
            add_to_download_list(option)

        self.current_index = 0
        self.downloaded_files = []
        self.download_next_file()

    def download_next_file(self):
        if self.current_index >= len(self.selected_options):
            messagebox.showinfo("Загрузка завершена",
                                f"Все файлы были успешно загружены:\n" + "\n".join(self.downloaded_files))
            os.startfile(self.save_path)
            return

        option = self.selected_options[self.current_index]
        if option in self.urls:
            url, filename = self.urls[option]
            threading.Thread(target=self.download_browser, args=(url, filename, option)).start()

    def download_browser(self, url, filename, option):
        file_path = os.path.join(self.save_path, filename)
        try:
            with requests.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                downloaded_size = 0
                start_time = time.time()

                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            downloaded_size += len(chunk)
                            progress_var.set(downloaded_size / total_size * 100)
                            current_status_var.set(
                                f"Загружается: {filename} ({self.current_index + 1}/{len(self.selected_options)})")
                            self.master.update_idletasks()

                            elapsed_time = time.time() - start_time
                            if elapsed_time > 60 and downloaded_size < total_size * 0.05:
                                raise Exception("Превышено время ожидания для загрузки")

                self.downloaded_files.append(filename)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при загрузке {filename}: {e}")

        self.current_index += 1
        self.download_next_file()


def add_to_download_list(item):
    frame = tk.Frame(download_listbox, bg="white")
    frame.pack(fill=tk.X)
    label = tk.Label(frame, text=item, anchor="w", bg="white")
    label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    button = tk.Button(frame, text="Удалить", command=lambda: remove_from_download_list(frame, item))
    button.pack(side=tk.RIGHT)


def remove_from_download_list(frame, item):
    frame.destroy()
    software_vars[item].set("")


def show_info():
    info_window = tk.Toplevel(root)
    info_window.title("Справка")

    info_label = tk.Label(info_window, text="Создатель: offach\nКонтакт: me@offach.ru\n\nСписок ссылок:")
    info_label.pack(padx=10, pady=10)

    links_text = "\n".join([f"{name}: {url[0]}" for name, url in download_manager.urls.items()])
    links_label = tk.Label(info_window, text=links_text, justify=tk.LEFT, anchor="w")
    links_label.pack(padx=10, pady=10)

    info_window.transient(root)
    info_window.grab_set()
    root.wait_window(info_window)


def create_gui():
    global root, progress_var, current_status_var, all_vars, download_listbox, search_entry, software_vars, all_checkbuttons, download_manager

    root = tk.Tk()
    root.title("offach's installer")
    root.geometry("550x650")  # Задаем фиксированный размер окна
    root.configure(bg="white")

    def on_start():
        messagebox.showinfo("Внимание", "Ответственности создатель не несет, используйте на свой риск.")

    root.after(100, on_start)

    main_frame = tk.Frame(root, bg="white")
    main_frame.pack(fill=tk.BOTH, expand=True)

    canvas = tk.Canvas(main_frame, bg="white")
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Прокрутка колесиком мыши
    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Creating a search bar
    search_frame = tk.Frame(scrollable_frame, padx=20, pady=10, bg="white")
    search_frame.pack(fill=tk.X)
    search_label = tk.Label(search_frame, text="Поиск", bg="white")
    search_label.pack(side=tk.LEFT)
    search_entry = tk.Entry(search_frame)
    search_entry.pack(fill=tk.X, expand=True)
    search_entry.bind("<KeyRelease>", search_program)

    # Info button
    info_button = tk.Button(scrollable_frame, text="Информация", command=show_info)
    info_button.pack(anchor="ne", padx=10, pady=5)

    categories = {
        "Браузеры": ["Google Chrome", "Mozilla Firefox", "Yandex", "Opera"],
        "СоцСети": ["Discord", "Skype", "Telegram Desktop", "Zoom", "WhatsApp Desktop"],
        "Лаунчеры игр и т.д.": ["Steam", "Epic Games Launcher", "EA Play", "Ubisoft Connect", "Battle.net"],
        "Софт для разработки": ["Visual Studio Code", "JetBrains IntelliJ IDEA", "PyCharm", "Atom", "Sublime Text"],
        "Полезные утилиты": ["OBS Studio", "7-Zip"],
        "Приложения для гаджетов": ["Logitech G Hub", "Razer Synapse", "MSI Dragon Center", "Corsair iCUE", "SteelSeries Engine"]
    }

    all_vars = []
    all_checkbuttons = []
    software_vars = {}

    cat_frame = tk.Frame(scrollable_frame, padx=10, pady=10, bg="white")
    cat_frame.pack(fill=tk.BOTH, expand=True)

    row = 0
    col = 0
    for category, items in categories.items():
        if col >= 3:
            col = 0
            row += 1
        frame = tk.LabelFrame(cat_frame, text=category, padx=10, pady=10, bg="white")
        frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        for item in items:
            var = tk.StringVar(value="")
            chk = tk.Checkbutton(frame, text=item, variable=var, onvalue=item, offvalue="",
                                 command=update_download_list, bg="white")
            chk.pack(anchor=tk.W)
            all_vars.append(var)
            all_checkbuttons.append(chk)
            software_vars[item] = var

        col += 1

    # Listbox to show selected programs for download
    download_listbox_frame = tk.LabelFrame(scrollable_frame, text="Список загрузок", padx=10, pady=10, bg="white")
    download_listbox_frame.pack(fill=tk.X, pady=5)
    download_listbox = tk.Frame(download_listbox_frame, bg="white")
    download_listbox.pack(fill=tk.X, pady=5)

    current_status_var = tk.StringVar()
    current_status_label = tk.Label(scrollable_frame, textvariable=current_status_var, bg="white")
    current_status_label.pack(pady=5)

    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(scrollable_frame, variable=progress_var, maximum=100)
    progress_bar.pack(fill=tk.X, pady=10)

    download_manager = DownloadManager(root)
    download_button = tk.Button(scrollable_frame, text="Загрузить", command=download_manager.start_download)
    download_button.pack(pady=10)

    root.mainloop()


def update_download_list():
    # Clear the download list frame
    for widget in download_listbox.winfo_children():
        widget.destroy()

    for var in all_vars:
        if var.get():
            add_to_download_list(var.get())


def search_program(event):
    search_text = search_entry.get().lower()
    for chk in all_checkbuttons:
        if search_text in chk.cget("text").lower():
            chk.config(fg="red")
        else:
            chk.config(fg="black")

    if search_text == "":
        for chk in all_checkbuttons:
            chk.config(fg="black")


if __name__ == "__main__":
    create_gui()
