import tkinter as tk
from tkinter import scrolledtext
import shlex

class ShellEmulator:
    def __init__(self, root, script_path=None):# конструктор
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

        # Приветствие
        self.print_output("You are using emulator of the Unix-system-v1\n")
        self.print_output("Enter command: ls, cd, exit\n\n")
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

    def _execute_command(self, command_line): #2 этап
        try:
            tokens = shlex.split(command_line)
            cmd = tokens[0]
            args = tokens[1:]

            if cmd == "exit":
                self.root.quit()
            elif cmd == "ls":
                self.stub_ls(args)
            elif cmd == "cd":
                self.stub_cd(args)
            else:
                self.print_output(f"Unknown command: {cmd}\n")

        except ValueError as e:
            self.print_output(f"Value error: {e}\n")
        except Exception as e:
            self.print_output(f"Unknown error: {e}\n")

    def stub_ls(self, args):
        self.print_output(f"[ЗАГЛУШКА] ls {args}\n")

    def stub_cd(self, args):
        self.print_output(f"[ЗАГЛУШКА] cd {args}\n")

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