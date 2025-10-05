from emulator_shell import ShellEmulator
import tkinter as tk
import argparse # 2 этап

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--vfs", help="Path to VFS XML ")
    parser.add_argument("--script", help="Path to startup script ")
    args = parser.parse_args()

    try:
        root = tk.Tk()
        app = ShellEmulator(root, vfs_path=args.vfs, script_path=args.script)
        root.mainloop()
    except Exception as err:
        print(f"Error: {err}")
        input("Press Enter ...")