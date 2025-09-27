import tkinter as tk
from tkinter import scrolledtext
import shlex

class ShellEmulator:
    def __init__(self, root):# конструктор
        self.root = root
        self.root.title("UnixEmulatorV1 — -zsh 800x500 — [cheese_cheddar@Noutbuk-Maksim-2]")
        self.root.geometry("800x500")
        # GUI:
        # поле вывода
        self.output = scrolledtext.ScrolledText(
            root,
            wrap=tk.WORD,
            state='disabled',
            font=("Menlo", 10),
            bg="#000" # чёрный фон
        )
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

    def print_output(self, text):
        self.output.config(state='normal') # разрешаем изменение для добавления текста
        self.output.insert(tk.END, text)
        self.output.config(state='disabled')
        self.output.see(tk.END) # прокрутка

    def execute_command(self, event=None):
        command_line = self.entry.get().strip() # получаем ввод
        if not command_line: # ничего не делаем если пусто
            return

        self.print_output(f"(base) cheese_makso@Noutbuk-testEmulator $ {command_line}\n")
        self.entry.delete(0, tk.END) # отчистка поля ввода

        try:
            tokens = shlex.split(command_line) # разбиваем по токенам
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
            self.print_output(f"Error: {e}\n")
        except Exception as e:
            self.print_output(f"Unknown error: {e}\n")

    def stub_ls(self, args):
        self.print_output(f"[ЗАГЛУШКА] ls {args}\n")

    def stub_cd(self, args):
        self.print_output(f"[ЗАГЛУШКА] cd {args}\n")


if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ShellEmulator(root)
        root.mainloop()
    except Exception as err:
        print(f"Error: {err}")
        input("Press Enter ...")