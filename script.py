#!/usr/bin/python3
import shutil
import subprocess

from gi import require_version

require_version("Nautilus", "4.0")

from gi.repository import GObject, Gio, Nautilus

class Terminal:
    def __init__(self, name: str):
        self._cmd = []
        self._name = name
        self._args = []
        
    def is_valid(self) -> bool:
        return len(self._cmd) > 0
        
    def exec(self, exec: str):
        if self.is_valid() and shutil.which(exec) is not None:
            self._cmd = [exec]
        return self
        
    def flatpak(self, id: str):
        proc = subprocess.Popen(["flatpak", "info", id], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        if proc.returncode == 0:
            self._cmd = ["flatpak", "run", id]
        return self
        
    def args(self, args: list[str]):
        self._args = args
        return self
        
    def command(self) -> str:
        return self._cmd + self._args
    
    def app_info(self) -> Gio.AppInfo:
        command_str = " ".join(self.command())
        print(command_str, self._name)
        return Gio.AppInfo.create_from_commandline(command_str, self._name, Gio.AppInfoCreateFlags.NONE)

class OepnWithRecommended(GObject.GObject, Nautilus.MenuProvider):
    def __init__(self):
        super().__init__()
        self.terminal = self._get_terminal()
    
    def _get_terminal(self) -> Gio.AppInfo | None:
        settings = Gio.Settings.new("org.gnome.desktop.default-applications.terminal") 
        terminals = [
            Terminal("Terminal").exec(settings.get_string("exec") or ""),
            Terminal("Alacritty").exec("alacritty"),
            Terminal("Ptyxis").exec("ptyxis").flatpak("app.devsuite.Ptyxis").args(["--new-window", "-d"]),
            Terminal("Gnome Terminal").exec("gnome-terminal"),
            Terminal("Konsole").exec("konsole"),
            Terminal("Xfce4 Terminal").exec("xfce4-terminal"),
            Terminal("Terminator").exec("terminator"),
            Terminal("Tilix").exec("tilix"),
            Terminal("Kitty").exec("kitty"),
            Terminal("Xterm").exec("xterm"),
        ]

        for terminal in terminals:
            if terminal.is_valid():
                return terminal.app_info()

        return None
    
    def _launch(self, app: Gio.AppInfo, file: Nautilus.FileInfo) -> None:
        uris = [file.get_uri()]
        app.launch_uris_async(uris, None, None, None)
        
    def _get_label(self, name: str) -> str:
        MAXIMUM_LABEL_LENGTH = 10
        words = ""
        for index, part in enumerate(name.lower().split(" ")):
            if len(part) == 0: continue
            words += " " + part
            if index > 0 and len(words) > MAXIMUM_LABEL_LENGTH:
                words += "..."
                break
        return words
    
    def _create_menu_item(self, app: Gio.AppInfo, file: Nautilus.FileInfo) -> Nautilus.MenuItem:
        if app.get_commandline() is None:
            return None
        
        item = Nautilus.MenuItem(
            name="open-with::" + (app.get_id() or app.get_name()),
            label="Open with " + self._get_label(app.get_display_name()),
            tip=app.get_description(),
        )

        item.connect("activate", lambda _, __: self._launch(app, file), None)
        return item
    
    def _create_menu(self, file: Nautilus.FileInfo, mime: str) -> list[Nautilus.MenuItem]:
        apps = Gio.AppInfo.get_recommended_for_type(mime)
        items = []
        if self.terminal and mime == "inode/directory":
            menu_item = self._create_menu_item(self.terminal, file)
            items.append(menu_item)
        
        for app in apps:
            if len(items) > 4: break
            menu_item = self._create_menu_item(app, file)
            if menu_item is None: continue
            items.append(menu_item)
            
        return items

    def get_file_items(self, files: list[Nautilus.FileInfo]):
        if len(files) != 1:
            return []
        file = files[0]
        return self._create_menu(file, file.get_mime_type())

    def get_background_items(self, directory: Nautilus.FileInfo):
        return self._create_menu(directory, "inode/directory")