from tkinter import *
from gui import run_gui, pop_up
from file_managers import file_manager


class MasterGUI:
    def __init__(self, root):
        self.root = root

        self.root.title("Digit Classifier")
        # setup menu bar
        self.menu_bar = Menu(root)

        self.file_menu = self._setup_file_menu()
        self.view_menu = self._setup_view_menu()
        self.run_menu = self._setup_run_menu()

        root.config(menu=self.menu_bar)

        # setup frame structure
        self.train_UI_frame = Frame(root, width=600, height=600)
        self.train_UI_frame.grid(column=0, row=0)

        # setup modules

        self.file_handler = file_manager.FileManager()

    # Menu bar methods
    def _setup_file_menu(self):
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self._file_new)
        file_menu.add_command(label="Load", command=self._file_load)
        file_menu.add_command(label="Save", command=self._file_save)
        file_menu.add_command(label="Save As", command=self._file_save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        return file_menu

    def _setup_view_menu(self):
        view_menu = Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Coming Soon!")
        self.menu_bar.add_cascade(label="View", menu=view_menu)
        return view_menu

    def _setup_run_menu(self):
        run_menu = Menu(self.menu_bar, tearoff=0)
        run_menu.add_command(label="Run", command=self._run_run)
        run_menu.add_command(label="Debug", command=self.to_do)
        run_menu.add_command(label="Train", command=self.to_do)
        self.menu_bar.add_cascade(label="Run", menu=run_menu)
        return run_menu

    def _file_new(self):
        pop_up.NewNetwork(self.root, self.file_handler)

    def _file_load(self):
        pop_up.LoadNetwork(self.root, self.file_handler)

    def _file_save(self):
        self.file_handler.save()

    def _file_save_as(self):
        pop_up.SaveByName(self.root, self.file_handler)

    def _run_run(self):
        run_gui.RunGUI(self.root, self.file_handler.loaded_object, title=self.file_handler.current_file_name)

    @staticmethod
    def to_do():
        print("TODO")


root = Tk()

ui = MasterGUI(root)

root.mainloop()
