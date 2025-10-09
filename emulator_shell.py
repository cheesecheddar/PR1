import tkinter as tk
from tkinter import scrolledtext
import shlex
from vfs import create_default_vfs, load_vfs_from_xml, normalize_path, is_dir, list_dir, get_node
import getpass
import calendar
from datetime import datetime

class ShellEmulator:
    def __init__(self, root,vfs_path=None, script_path=None):# конструктор
        self.root = root
        self.root.title("UnixEmulatorV1 — -zsh 800x500 — [cheese_cheddar@Noutbuk-Maksim-2]")
        self.root.geometry("800x500")
        # GUI:
        # поле вывода
        self.output = scrolledtext.ScrolledText(root,wrap=tk.WORD,state='disabled',font=("Menlo", 10),bg="#000")# чёрный фон
        self.output.pack(expand=True, fill='both', padx=5, pady=5)

        # поле ввода
        self.input_frame = tk.Frame(root, bg="#000")
        self.input_frame.pack(fill='x', padx=5, pady=(0, 5))

        self.prompt_label = tk.Label(self.input_frame, text="(base) cheese_makso@Noutbuk-testEmulator $ ", font=("Menlo", 10))
        self.prompt_label.pack(side='left')

        self.entry = tk.Entry(self.input_frame, font=("Menlo", 10), bg="#000")
        self.entry.pack(side='left')
        self.entry.pack(side='left', fill='x', expand=True)
        self.entry.bind("<Return>", self.execute_command) # при нажатии Enter вызывается обработчик команды
        self.entry.focus()
        # загрузка VFS
        if vfs_path:
            try:
                self.vfs = load_vfs_from_xml(vfs_path)
            except Exception as e:
                self.print_output(f"VFS error: {e}. Using default VFS.\n")
                self.vfs = create_default_vfs()
        else:
            self.vfs = create_default_vfs()
        self.current_dir = "/"
        # приветствие
        self.print_output("You are using emulator of the Unix-system-v1\n")
        self.print_output("Enter command: ls, cd, exit\n\n")
        # скрипт
        if script_path:
            self.run_script(script_path)

    def print_output(self, text):
        self.output.config(state='normal') # разрешаем изменение для добавления текста
        self.output.insert(tk.END, text)
        self.output.config(state='disabled')
        self.output.see(tk.END) # прокрутка

    def execute_command(self, event=None):
        command_line = self.entry.get().strip()
        if not command_line:
            return
        self.print_output(f"(base) cheese_makso@Noutbuk-testEmulator $ {command_line}\n")
        self.entry.delete(0, tk.END)
        self._execute_command(command_line)

    def _execute_command(self, cmd_line): #2 этап
        try:
            tokens = shlex.split(cmd_line)
            cmd = tokens[0]
            args = tokens[1:]

            if cmd == "exit":
                self.root.quit()
            elif cmd == "ls":
                self.cmd_ls(args)
            elif cmd == "cd":
                self.cmd_cd(args)
            elif cmd == "whoami":
                self.cmd_whoami()
            elif cmd == "cal":
                self.cmd_cal()
            elif cmd == "rmdir":
                self.cmd_rmdir(args)
            elif cmd == "vfs-load":
                self.cmd_vfs_load(args)
            else:
                self.print_output(f"Unknown command: {cmd}\n")
        except Exception as e:
            self.print_output(f"Error: {e}\n")

    def cmd_ls(self, args):
        path = args[0] if args else self.current_dir
        try:
            path_parts = normalize_path(self.current_dir, path)
            files = list_dir(self.vfs, path_parts)
            self.print_output("  ".join(files) + "\n")
        except Exception as e:
            self.print_output(f"ls: cannot access '{path}': {e}\n")

    def cmd_cd(self, args):
        if not args:
            self.current_dir = "/"
            return
        target = args[0]
        try:
            path_parts = normalize_path(self.current_dir, target)
            # Собираем путь для отображения
            new_path = "/" + "/".join(path_parts) if path_parts else "/"
            if is_dir(self.vfs, path_parts):
                self.current_dir = new_path
            else:
                self.print_output(f"cd: not a directory: {new_path}\n")
        except Exception as e:
            self.print_output(f"cd: {e}\n")

    def cmd_whoami(self):
        self.print_output(f"{getpass.getuser()}\n")

    def cmd_cal(self):
        now = datetime.now()
        cal_text = calendar.TextCalendar().formatmonth(now.year, now.month)
        self.print_output(cal_text + "\n")

    def cmd_rmdir(self, args):
        if not args:
            self.print_output("rmdir: missing operand\n")
            return
        target = args[0]
        try:
            path_parts = normalize_path(self.current_dir, target)
            if not path_parts:
                self.print_output("rmdir: cannot remove '/': Is a directory\n")
                return

            # Получаем родителя
            parent_parts = path_parts[:-1]
            dir_name = path_parts[-1]

            parent = get_node(self.vfs, parent_parts)
            if dir_name not in parent:
                raise FileNotFoundError(f"No such file or directory")

            target_node = parent[dir_name]
            if isinstance(target_node, dict) and len(target_node) == 0:
                del parent[dir_name]
                self.print_output("")
            else:
                self.print_output(f"rmdir: failed to remove '{target}': Directory not empty\n")
        except Exception as e:
            self.print_output(f"Error: {e}\n")

    def cmd_vfs_load(self, args):
        if not args:
            self.print_output("vfs-load: missing file path\n")
            return
        try:
            self.vfs = load_vfs_from_xml(args[0])
            self.current_dir = "/"
            self.print_output(f"VFS reloaded from {args[0]}\n")
        except Exception as e:
            self.print_output(f"vfs-load error: {e}\n")

    def run_script(self, script_path):# 2 этап
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    # Имитируем ввод от пользователя
                    self.print_output(f"(base) cheese_makso@Noutbuk-testEmulator $ {line}\n")
                    # Выполняем через тот же механизм, что и GUI
                    self._execute_command(line)
        except Exception as e:
            self.print_output(f"Script error (ignored): {e}\n")