import random
import tkinter as tk
from tkinter import ttk, messagebox
import time
from PIL import Image, ImageTk
import json
from i18n import i18n, I18N
from database_scores import (
    initialize_database,
    store_player_time,
    update_global_top,
    get_player_times,
    get_global_top,
)
from add_images import add_image


key_window_instance = None
player_name = i18n.translations.get("Anonymous", "Anonymous")

class LanguageSelectorWindow:
    def __init__(self, parent):
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self.window.title(i18n.translations.get("Select Language", "Select Language"))
        self.window.geometry("300x200")

        tk.Label(self.window, text=i18n.translations.get("Choose Language:", "Choose Language:"), font=("Times New Roman", 12)).pack(pady=10)

        self.language_var = tk.StringVar(value=i18n.translations.get('current_language', 'en'))

        languages = I18N.get_available_languages()
        current_language = i18n.translations.get('current_language', 'en')

        for lang in languages:
            lang_button = ttk.Radiobutton(
                self.window,
                text=lang.upper(),
                variable=self.language_var,
                value=lang
            )
            lang_button.pack(pady=5)

            if lang == current_language:
                lang_button.config(state="disabled")

        ttk.Button(self.window, text=i18n.translations.get("Apply", "Apply"), command=self.apply_language).pack(pady=10)

    def apply_language(self):
        global i18n
        selected_lang = self.language_var.get()
        try:
            i18n = I18N(selected_lang)
            messagebox.showinfo(
                i18n.translations.get("Success", "Success"),
                i18n.translations.get("Language changed successfully!", "Language changed successfully!")
            )
            self.window.destroy()
            self.parent.destroy()

            self.restart_main_menu()
        except Exception as e:
            messagebox.showerror(i18n.translations.get("Error", "Error"), str(e))

    def restart_main_menu(self):
        global win, main_menu, control

        win.destroy()
        win = tk.Tk()
        main_menu = MainMenuWindow(win)
        win.mainloop()
        control.set = tk.IntVar(win, 0)
class CongratulationsWindow:
    def __init__(self, root):
        self.root = root
        self.new_window = tk.Toplevel(root)
        self.new_window.title(i18n.translations.get("Congratulations!", "Congratulations!"))
        self.new_window.geometry("400x400+150+250")

        global timer_instance
        if timer_instance and timer_instance.running:
            elapsed_time = timer_instance.stop_timer()
            store_player_time(player_name, elapsed_time)
            update_global_top(player_name, elapsed_time)
        else:
            elapsed_time = 0

        tk.Label(
            self.new_window,
            text=i18n.translations.get("Congratulations!", "Congratulations!"),
            font=("Times New Roman", 24, "bold")
        ).pack(pady=20)

        tk.Label(
            self.new_window,
            text=f"{i18n.translations.get('Time Taken:', 'Time Taken:')} {elapsed_time:.2f} {i18n.translations.get('seconds', 'seconds')}",
            font=("Times New Roman", 18)
        ).pack(pady=20)
class GameWindow:
    def open_congratulations_window(self):
        if control.get() == 4:
            self.new_window.destroy()
            global game_instance
            game_instance = CongratulationsWindow(self.root)
            game_instance.new_window.lift()
            game_instance.new_window.focus_force()


            global timer_instance
            if timer_instance:
                timer_instance.new_window.destroy()
                timer_instance = None
        else:
            messagebox.showwarning(i18n.translations.get("Not Enough Keys", "Not Enough Keys"),
                                   i18n.translations.get("You need more keys to open this door!", "You need more keys to open this door!")
            )
    def open_room4_window(self):
        self.new_window.destroy()
        game_instance = room4Window(self.root)
        game_instance.new_window.lift()
        game_instance.new_window.focus_force()

    def open_room3_window(self):
        self.new_window.destroy()
        game_instance = room3Window(self.root)
        game_instance.new_window.lift()
        game_instance.new_window.focus_force()

    def open_room2_window(self):
        self.new_window.destroy()
        game_instance = room2Window(self.root)
        game_instance.new_window.lift()
        game_instance.new_window.focus_force()

    def open_room1_window(self):
        self.new_window.destroy()
        game_instance = room1Window(self.root)
        game_instance.new_window.lift()
        game_instance.new_window.focus_force()

    def __init__(self, root):
        self.root = root
        self.new_window = tk.Toplevel(root)
        self.new_window.title(i18n.translations.get("Game Window", "Game Window"))
        self.new_window.geometry("700x550+350+200")
        self.new_window.focus_force()
        self.canvas = tk.Canvas(self.new_window, width=500, height=400, bg="lightblue")
        self.canvas.pack(fill="both", expand=True)
        self.new_window.iconbitmap("game_icon.ico")
        room0_config = "json/room0_config.json"
        with open(room0_config, 'r') as file:
            config = json.load(file)

        self.images = {}
        for image in config["images"]:
            add_image(self.canvas, self.images, image)

        kapı = Image.open("assets/kapi.png")
        kapı = kapı.resize((100, 200))
        kapıtk = ImageTk.PhotoImage(kapı)
        self.canvas.kapıtk = kapıtk
        kapıid = self.canvas.create_image((350, 50), anchor="center", image=kapıtk)
        self.canvas.kapı = kapıtk
        self.canvas.tag_bind(kapıid, "<Button-1>", lambda e: self.open_congratulations_window())

        ok1 = Image.open("assets/oksol.png")
        ok1 = ok1.resize((100, 100))
        ok1tk = ImageTk.PhotoImage(ok1)
        self.canvas.ok1tk = ok1tk
        ok1id = self.canvas.create_image((75, 250), anchor="center", image=ok1tk)
        self.canvas.ok1 = ok1tk
        self.canvas.tag_bind(ok1id, "<Button-1>", lambda e: self.open_room1_window())

        ok2 = Image.open("assets/oksag.png")
        ok2 = ok2.resize((100, 100))
        ok2tk = ImageTk.PhotoImage(ok2)
        self.canvas.ok2tk = ok2tk
        ok2id = self.canvas.create_image((630, 250), anchor="center", image=ok2tk)
        self.canvas.ok2 = ok2tk
        self.canvas.tag_bind(ok2id, "<Button-1>", lambda e: self.open_room2_window())

        ok3 = Image.open("assets/oksag.png")
        ok3 = ok3.resize((100, 100))
        ok3tk = ImageTk.PhotoImage(ok3)
        self.canvas.ok3tk = ok3tk
        ok3id = self.canvas.create_image((630, 450), anchor="center", image=ok3tk)
        self.canvas.ok3 = ok3tk
        self.canvas.tag_bind(ok3id, "<Button-1>", lambda e: self.open_room3_window())

        ok4 = Image.open("assets/oksol.png")
        ok4 = ok4.resize((100, 100))
        ok4tk = ImageTk.PhotoImage(ok4)
        self.canvas.ok4tk = ok4tk
        ok4id = self.canvas.create_image((75, 450), anchor="center", image=ok4tk)
        self.canvas.ok4 = ok4tk
        self.canvas.tag_bind(ok4id, "<Button-1>", lambda e: self.open_room4_window())
        self.new_window.resizable(False, False)
class KeyWindow:
    def __init__(self, root):
        self.root = root
        self.new_window = tk.Toplevel(root)
        self.new_window.title(i18n.translations.get("Keys", "Keys"))
        self.new_window.geometry("200x100+1075+325")


        self.control_text = tk.StringVar()
        self.update_control_text()

        self.keyCountLabel = ttk.Label(self.new_window, textvariable=self.control_text)
        self.keyCountLabel.pack(expand=True)

    def update_control_text(self):
        self.control_text.set(f"{i18n.translations.get('Keys', 'Keys')}: {control.get()}")


class room1Window:
    def open_cardgame_window(self):
        game_instance = CardGameWindow(self.root)
        game_instance.new_window.lift()
        game_instance.new_window.focus_force()

    def open_game_window(self):
        self.new_window.destroy()
        game_instance = GameWindow(self.root)
        game_instance.new_window.lift()
        game_instance.new_window.focus_force()

    def __init__(self, root):
        self.root = root
        self.new_window = tk.Toplevel(root)
        self.new_window.title(i18n.translations.get("Room 1 Window", "Room 1 Window"))  
        self.new_window.geometry("700x550+200+200")

        self.canvas = tk.Canvas(self.new_window, width=500, height=400, bg="lightblue")
        self.canvas.pack(fill="both", expand=True)

        room1_config = "json/room1_config.json"
        with open(room1_config, 'r') as file:
            config = json.load(file)

        self.images = {}
        for image in config["images"]:
            add_image(self.canvas, self.images, image)

        ok = Image.open("assets/oksag.png")
        ok = ok.resize((100, 100))
        oktk = ImageTk.PhotoImage(ok)
        self.canvas.oktk = oktk
        okid = self.canvas.create_image((600, 350), anchor="center", image=oktk)
        self.canvas.ok = oktk
        self.canvas.tag_bind(okid, "<Button-1>", lambda e: self.open_game_window())

        kitap = Image.open("assets/kitap.png")
        kitap = kitap.resize((50, 35))
        kitaptk = ImageTk.PhotoImage(kitap)
        self.canvas.kitaptk = kitaptk
        kitapid = self.canvas.create_image((350, 225), anchor="center", image=kitaptk)
        self.canvas.kitap = kitaptk
        self.canvas.tag_bind(kitapid, "<Button-1>", lambda e: self.open_cardgame_window())
        self.new_window.resizable(False, False)
class room2Window:
    def open_cooking_game(self):
        game_instance = FoodChemistryLab(self.root)
        game_instance.new_window.lift()
        game_instance.new_window.focus_force()

    def open_game_window(self):
        self.new_window.destroy()
        game_instance = GameWindow(self.root)
        game_instance.new_window.lift()
        game_instance.new_window.focus_force()
    def __init__(self, root):
        self.root = root
        self.new_window = tk.Toplevel(root)
        self.new_window.title(i18n.translations.get("Room 2 Window", "Room 2 Window"))  
        self.new_window.geometry("700x550+200+200")

        self.canvas = tk.Canvas(self.new_window, width=500, height=400, bg="lightblue")
        self.canvas.pack(fill="both", expand=True)

        room2_config = "json/room2_config.json"
        with open(room2_config, 'r') as file:
            config = json.load(file)

        self.images = {}
        for image in config["images"]:
            add_image(self.canvas, self.images, image)

        ok = Image.open("assets/oksol.png")
        ok = ok.resize((100, 100))
        oktk = ImageTk.PhotoImage(ok)
        self.canvas.oktk = oktk
        okid = self.canvas.create_image((65, 300), anchor="center", image=oktk)
        self.canvas.ok = oktk
        self.canvas.tag_bind(okid, "<Button-1>", lambda e: self.open_game_window())

        tezgah = Image.open("assets/tezgah.png")
        tezgah = tezgah.resize((350, 140))
        tezgahtk = ImageTk.PhotoImage(tezgah)
        self.canvas.oktk = tezgahtk
        tezgahid = self.canvas.create_image((460, 135), anchor="center", image=tezgahtk)
        self.canvas.tezgah = tezgahtk
        self.canvas.tag_bind(tezgahid, "<Button-1>", lambda e: self.open_cooking_game())
        self.new_window.resizable(False, False)
class room3Window:
    def open_mastermind_game(self):
        game_instance = MastermindGame(self.root)
        game_instance.new_window.lift()
        game_instance.new_window.focus_force()

    def open_game_window(self):
        self.new_window.destroy()
        game_instance = GameWindow(self.root)
        game_instance.new_window.lift()
        game_instance.new_window.focus_force()

    def __init__(self, root):
        self.root = root
        self.new_window = tk.Toplevel(root)
        self.new_window.title(i18n.translations.get("Room 3 Window", "Room 3 Window"))  
        self.new_window.geometry("700x550+200+200")

        self.canvas = tk.Canvas(self.new_window, width=500, height=400, bg="lightblue")
        self.canvas.pack(fill="both", expand=True)

        room3_config = "json/room3_config.json"
        with open(room3_config, 'r') as file:
            config = json.load(file)

        self.images = {}
        for image in config["images"]:
            add_image(self.canvas, self.images, image)

        ok = Image.open("assets/oksol.png")
        ok = ok.resize((100, 100))
        oktk = ImageTk.PhotoImage(ok)
        self.canvas.oktk = oktk
        okid = self.canvas.create_image((75, 350), anchor="center", image=oktk)
        self.canvas.ok = oktk
        self.canvas.tag_bind(okid, "<Button-1>", lambda e: self.open_game_window())

        kasa = Image.open("assets/kasa.png")
        kasa = kasa.resize((110, 110))
        kasatk = ImageTk.PhotoImage(kasa)
        self.canvas.kasatk = kasatk
        kasaid = self.canvas.create_image((500, 150), anchor="center", image=kasatk)
        self.canvas.kasa = kasatk
        self.canvas.tag_bind(kasaid, "<Button-1>", lambda e: self.open_mastermind_game())
        self.new_window.resizable(False, False)
class room4Window:
    def open_pathfinding_game(self):
        game_instance = PathfindingGameWindow(self.root)
        game_instance.new_window.lift()
        game_instance.new_window.focus_force()

    def open_game_window(self):
        self.new_window.destroy()
        game_instance = GameWindow(self.root)
        game_instance.new_window.lift()
        game_instance.new_window.focus_force()

    def __init__(self, root):
        self.root = root
        self.new_window = tk.Toplevel(root)
        self.new_window.title(i18n.translations.get("Room 4 Window", "Room 4 Window"))  
        self.new_window.geometry("700x550+200+200")

        self.canvas = tk.Canvas(self.new_window, width=700, height=550, bg="lightblue")
        self.canvas.pack(fill="both", expand=True)

        room4_config = "json/room4_config.json"
        with open(room4_config, 'r') as file:
            config = json.load(file)

        self.images = {}
        for image in config["images"]:
            add_image(self.canvas, self.images, image)

        ok = Image.open("assets/oksag.png")
        ok = ok.resize((100, 100))
        oktk = ImageTk.PhotoImage(ok)
        self.canvas.oktk = oktk
        okid = self.canvas.create_image((625, 350), anchor="center", image=oktk)
        self.canvas.ok = oktk
        self.canvas.tag_bind(okid, "<Button-1>", lambda e: self.open_game_window())

        gider = Image.open("assets/gider.png")
        gider = gider.resize((50, 50))
        gidertk = ImageTk.PhotoImage(gider)
        self.canvas.gidertk = gidertk
        giderid = self.canvas.create_image((650, 515), anchor="center", image=gidertk)
        self.canvas.gider = gidertk
        self.canvas.tag_bind(giderid, "<Button-1>", lambda e: self.open_pathfinding_game())
        self.new_window.resizable(False, False)

class TimerWindow:
    def __init__(self, root):
        self.root = root
        self.new_window = tk.Toplevel(root)
        self.new_window.title(i18n.translations.get("In-Game Timer", "In-Game Timer"))
        self.new_window.geometry("200x100+1075+200")
        self.running = True
        self.start_time = time.time()
        self.pause_time = None
        self.time_label = ttk.Label(self.new_window, text="00:00:00", font=("Times New Roman", 24))
        self.time_label.pack(pady=20)
        self.new_window.protocol("WM_DELETE_WINDOW", self.prevent_close)
        self.update_timer()

    def stop_timer(self):
        if self.running:
            self.running = False
            elapsed_time = time.time() - self.start_time
            return elapsed_time
        return 0

    def update_timer(self):
        if self.running:
            elapsed_time = int(time.time() - self.start_time)
            formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
            self.time_label.config(text=formatted_time)
            self.new_window.after(1000, self.update_timer)


    def prevent_close(self):

        self.running = False
        self.pause_time = time.time()

        messagebox.showinfo(
            i18n.translations.get("Action Not Allowed", "Action Not Allowed"),
            i18n.translations.get("You cannot close the timer window.", "You cannot close the timer window.")
        )

        if self.pause_time:
            pause_duration = time.time() - self.pause_time
            self.start_time += pause_duration

        self.running = True
        self.update_timer()

class MainMenuWindow:
    def __init__(self, root):
        self.root = root
        self.game_instance = None
        self.root.title(i18n.translations.get("Main Menu", "Main Menu"))
        self.root.geometry("400x400+550+250")
        self.root.iconbitmap("game_icon.ico")
        self.Frame1 = tk.LabelFrame(
            self.root, text=i18n.translations.get("W E L C O M E", "W E L C O M E"), labelanchor="n", width=300,
            height=300,
            bg="lightblue", font=("Times New Roman", 25)
        )
        self.Frame1.pack(expand=True, fill='both', padx=10, pady=10)
        self.label_name_of_the_game = ttk.Label(self.Frame1, text=i18n.translations.get("ESCAPE THE HOUSE", "ESCAPE THE HOUSE"), font=("Times New Roman", 20))
        self.label_name_of_the_game.pack(side="top", pady=5)
        self.button_play = ttk.Button(self.Frame1, text=i18n.translations.get("Play", "Play"), command=self.play_game)
        self.button_play.place(relx=0.5, rely=0.3, anchor="center")
        self.button_options = ttk.Button(self.Frame1, text=i18n.translations.get("Options", "Options"), command=self.open_options_window)
        self.button_options.place(relx=0.5, rely=0.4, anchor="center")
        self.button_quit = ttk.Button(self.Frame1, text=i18n.translations.get("Exit Game", "Exit Game"), command=self.exit_handler)
        self.button_quit.place(relx=0.5, rely=0.7, anchor="center")
        self.button_leaderboard = ttk.Button(self.Frame1, text=i18n.translations.get("View Leaderboard", "View Leaderboard"), command=self.open_leaderboard_window)
        self.button_leaderboard.place(relx=0.5, rely=0.6, anchor="center")

    def play_game(self):
        global player_name, game_window_instance
        player_name = None
        self.button_play.config(state="disabled")
        game_window = GameWindow(self.root)
        game_window.new_window.protocol("WM_DELETE_WINDOW", lambda: self.restore_main_menu())

        if not player_name:
            name_input = PlayerNameInput(self.root)
            self.root.wait_window(name_input.name_window)
            player_name = name_input.player_name
            self.open_timer_window()
            self.open_key_window()
            return
        if not player_name:
            return

    def restore_main_menu(self):
        self.root.deiconify()

    def open_timer_window(self):
        global timer_instance
        timer_instance = TimerWindow(self.root)
        timer_instance.new_window.lift()
        timer_instance.new_window.focus_force()

    def open_pathfinding_game(self):
        PathfindingGameWindow(self.root)
        
    def open_mastermind_game(self):
        MastermindGame(self.root)
        
    def open_foodchem_game(self):
        FoodChemistryLab(self.root)
        
    def exit_handler(self):
        on_exit()
        win.protocol("WM_DELETE_WINDOW", on_exit)


    def open_game_window(self):

        game_instance = GameWindow(self.root)
        game_instance.new_window.lift()
        game_instance.new_window.focus_force()

        if self.game_instance and self.game_instance.new_window.winfo_exists():
            messagebox.showinfo("Game Already Running", "A game is already running.")
        else:
            self.game_instance = GameWindow(self.root)

    def open_key_window(self):
        global key_window_instance
        if key_window_instance is None or not key_window_instance.new_window.winfo_exists():
            key_window_instance = KeyWindow(self.root)
        else:
            key_window_instance.new_window.lift()

    def open_options_window(self):
        new_window = OptionsWindow(self.root)
        new_window.new_window.lift()
        new_window.new_window.focus_force()

    def open_card_game_window(self):
        CardGameWindow(self.root)

    def open_leaderboard_window(self):
        global player_name
        if not player_name:
            messagebox.showwarning("Player Name Missing", "Please enter your name before viewing the leaderboard.")
            return
        LocalLeaderboardWindow(self.root, player_name)
        GlobalLeaderboardWindow(self.root)

class OptionsWindow:
    def __init__(self, root):
        self.new_window = tk.Toplevel(root)
        self.new_window.title(i18n.translations.get("Options Window", "Options Window"))
        self.new_window.geometry("300x200+950+250")
        self.new_window.iconbitmap("settings_icon.ico")
        self.Frame1 = tk.LabelFrame(
            self.new_window, text=i18n.translations.get("OPTIONS", "OPTIONS"), labelanchor="n", width=300, height=300,
            bg="lightblue", font=("Times New Roman", 15)
        )
        self.Frame1.pack(expand=True, fill='both', padx=10, pady=10)
        self.button_change_language = ttk.Button(
            self.Frame1, text=i18n.translations.get("Change Language", "Change Language"), width=15,
            command=self.open_language_selector
        )
        self.button_change_language.place(relx=0.5, rely=0.2, anchor="n")

    def open_language_selector(self):
        LanguageSelectorWindow(self.new_window)

class PlayerNameInput:
        def __init__(self, root):
            self.root = root
            self.player_name = None
            self.name_window = tk.Toplevel(root)
            self.name_window.title(i18n.translations.get("Enter Your Name:", "Enter Your Name:"))
            self.name_window.geometry("300x200+500+300")
            self.name_window.grab_set()
            self.name_window.iconbitmap("game_icon.ico")
            tk.Label(self.name_window, text=i18n.translations.get("Enter Your Name:", "Enter Your Name:"),
                     font=("Times New Roman", 14)).pack(pady=10)

            self.name_entry = ttk.Entry(self.name_window, font=("Times New Roman", 12))
            self.name_entry.pack(pady=10)

            ttk.Button(self.name_window, text=i18n.translations.get("Submit", "Submit"), command=self.save_name).pack(
                pady=10)

        def save_name(self):
            entered_name = self.name_entry.get().strip()
            if entered_name:
                self.player_name = entered_name
                self.name_window.destroy()
            else:
                messagebox.showwarning(
                    i18n.translations.get("Invalid Input", "Invalid Input"),
                    i18n.translations.get("Name cannot be empty!", "Name cannot be empty!")
                )

def sort_leaderboard(times):
    return sorted(times, key=lambda x: x[1])

class GlobalLeaderboardWindow:
    def __init__(self, root):
        self.root = root
        self.new_window = tk.Toplevel(root)
        self.new_window.title(i18n.translations.get("Global Leaderboard", "Global Leaderboard"))
        self.new_window.geometry("400x350+100+475")
        self.new_window.iconbitmap("game_icon.ico")

        tk.Label(self.new_window, text=i18n.translations.get("Global Top 10 Times", "Global Top 10 Times"),
                 font=("Times New Roman", 16, "bold")).pack(pady=10)

        self.frame = tk.Frame(self.new_window)
        self.frame.pack(pady=10)


        self.display_global_times()

    def display_global_times(self):
        global_top = get_global_top()

        if not global_top:
            tk.Label(
                self.frame,
                text=i18n.translations.get("No Records Found", "No Records Found"),
                font=("Times New Roman", 12),
                fg="red"
            ).pack(anchor="w")
        else:
            for idx, (name, time) in enumerate(global_top, 1):
                formatted_time = f"{time:.2f}"
                label_text = f"{idx}. {name} - {formatted_time} {i18n.translations.get('seconds', 'seconds')}"
                tk.Label(self.frame, text=label_text, font=("Times New Roman", 12)).pack(anchor="w")

class LocalLeaderboardWindow:
    def __init__(self, root, player_name):

        self.root = root
        self.player_name = player_name
        self.new_window = tk.Toplevel(root)
        title_text = i18n.translations.get("player_times", "%s's Times") % player_name
        self.new_window.title(title_text)
        self.new_window.geometry("400x350+100+75")
        self.new_window.iconbitmap("game_icon.ico")
        tk.Label(self.new_window, text=title_text, font=("Times New Roman", 16, "bold")).pack(pady=10)

        self.frame = tk.Frame(self.new_window)
        self.frame.pack(pady=10)


        self.display_local_times()

    def display_local_times(self):

        player_times = get_player_times(self.player_name)

        if not player_times:
            tk.Label(self.frame, text=i18n.translations.get("No Records Found", "No Records Found"), font=("Times New Roman", 12), fg="red").pack(anchor="w")
        else:
            for idx, (time,) in enumerate(player_times, 1):
                formatted_time = f"{time:.2f}"
                tk.Label(self.frame, text=f"{idx}. {formatted_time} {i18n.translations.get('seconds', 'seconds')}", font=("Times New Roman", 12)).pack(anchor="w")

class CardGameWindow:
    def __init__(self, root):
        self.new_window = tk.Toplevel(root)
        self.new_window.title(i18n.translations.get("Card Matching Game", "Card Matching Game"))
        self.new_window.geometry("500x475+200+200")
        self.new_window.iconbitmap("game_icon.ico")
        self.cards = list(range(1, 9)) * 2
        random.shuffle(self.cards)

        self.card_images = {
            i: ImageTk.PhotoImage(
                Image.open(f"images/card_{i}.png").resize((80, 80), Image.Resampling.LANCZOS)
            )
            for i in range(1, 9)
        }
        self.back_image = ImageTk.PhotoImage(
            Image.open("images/back.png").resize((80, 80), Image.Resampling.LANCZOS)
        )

        self.buttons = []
        self.first_card = None
        self.second_card = None
        self.matched_pairs = 0

        self.create_game_grid()

    def create_game_grid(self):
        frame = ttk.Frame(self.new_window)
        frame.pack(pady=20)

        for row in range(4):
            for col in range(4):
                card_value = self.cards.pop()
                button = ttk.Button(frame, image=self.back_image, width=80)
                button.grid(row=row, column=col, padx=5, pady=5)
                button.config(command=lambda b=button, v=card_value: self.reveal_card(b, v))
                self.buttons.append((button, card_value))

    def reveal_card(self, button, card_value):
        if self.first_card and self.second_card:
            return

        button.config(image=self.card_images[card_value], state="disabled")

        if not self.first_card:
            self.first_card = (button, card_value)
        else:
            self.second_card = (button, card_value)
            self.check_match()

    def check_match(self):
        first_button, first_value = self.first_card
        second_button, second_value = self.second_card

        if first_value == second_value:
            self.first_card = None
            self.second_card = None
            self.matched_pairs += 1

            if self.matched_pairs == len(self.buttons) // 2:
                messagebox.showinfo(
                    i18n.translations.get("Congratulations!", "Congratulations!"),
                    i18n.translations.get("You revealed all cards!", "You revealed all cards!")
                )
                global control
                control.set(control.get() + 1)
                if key_window_instance:
                    key_window_instance.update_control_text()
        else:
            self.new_window.after(1000, self.reset_cards)

    def reset_cards(self):
        first_button, _ = self.first_card
        second_button, _ = self.second_card

        first_button.config(image=self.back_image, state="normal")
        second_button.config(image=self.back_image, state="normal")

        self.first_card = None
        self.second_card = None

class PathfindingGameWindow:
    def __init__(self, root):
        self.new_window = tk.Toplevel(root)
        self.new_window.title(i18n.translations.get("Pathfinding Puzzle", "Pathfinding Puzzle"))
        self.new_window.geometry("600x750+200+50")
        self.new_window.configure(bg="white")


        self.grid_size = 10
        self.cell_size = 50
        self.level = 1
        self.max_level = 3
        self.obstacles = set()
        self.traps = set()
        self.player_position = [0, 0]
        self.goal_position = [self.grid_size - 1, self.grid_size - 1]
        self.steps = 0


        self.time_remaining = 60
        self.running = True

        self.timer_label = tk.Label(self.new_window,text=f"{i18n.translations.get('Time Left:', 'Time Left:')} {self.time_remaining}s", font=("Arial", 14))
        self.timer_label.pack(pady=5)

        self.level_label = tk.Label(self.new_window, text=f"{i18n.translations.get('Level:', 'Level:')} {self.level}", font=("Arial", 14))
        self.level_label.pack(pady=5)


        self.progress_var = tk.IntVar()
        self.progress_bar = ttk.Progressbar(self.new_window, orient="horizontal", length=400, mode="determinate",
                                            variable=self.progress_var, maximum=100)
        self.progress_bar.pack(pady=10)


        self.canvas = tk.Canvas(self.new_window, width=self.grid_size * self.cell_size,
                                height=self.grid_size * self.cell_size, bg="lightgray")
        self.canvas.pack(pady=20)

        self.start_level()


        self.new_window.bind("<Up>", lambda event: self.move_player(0, -1))
        self.new_window.bind("<Down>", lambda event: self.move_player(0, 1))
        self.new_window.bind("<Left>", lambda event: self.move_player(-1, 0))
        self.new_window.bind("<Right>", lambda event: self.move_player(1, 0))

    def start_level(self):
        self.steps = 0
        self.obstacles.clear()
        self.traps.clear()
        self.player_position = [0, 0]
        self.generate_obstacles()
        self.draw_grid()
        self.running = True
        self.update_level_label()
        self.update_timer()


        if self.level == 3:
            self.move_dynamic_goal()

    def move_dynamic_goal(self):

        if self.running and self.level == 3:

            while True:
                x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
                if (x, y) not in self.obstacles and (x, y) not in self.traps and (x, y) != tuple(self.player_position):
                    self.goal_position = [x, y]
                    break
            self.draw_grid()


            self.new_window.after(5000, self.move_dynamic_goal)

    def update_progress_bar(self):
        distance_to_goal = abs(self.goal_position[0] - self.player_position[0]) + abs(
            self.goal_position[1] - self.player_position[1])
        max_distance = self.grid_size * 2 - 2
        progress = (max_distance - distance_to_goal) / max_distance * 100
        self.progress_var.set(progress)


    def generate_obstacles(self):
        total_cells = self.grid_size ** 2
        num_obstacles = total_cells // 3
        num_traps = total_cells // 10
        max_attempts = 100

        for attempt in range(max_attempts):
            self.obstacles.clear()
            self.traps.clear()


            while len(self.obstacles) < num_obstacles:
                x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
                if (x, y) != tuple(self.player_position) and (x, y) != tuple(self.goal_position):
                    self.obstacles.add((x, y))


            if self.is_path_solvable():
                break


        while len(self.traps) < num_traps:
            x, y = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
            if (x, y) not in self.obstacles and (x, y) != tuple(self.player_position) and (x, y) != tuple(
                    self.goal_position):
                if abs(x - self.player_position[0]) > 1 or abs(y - self.player_position[1]) > 1:
                    self.traps.add((x, y))

    def is_path_solvable(self):
        from collections import deque

        visited = set()
        queue = deque([tuple(self.player_position)])
        goal = tuple(self.goal_position)

        while queue:
            current = queue.popleft()
            if current == goal:
                return True
            if current in visited:
                continue

            visited.add(current)

            x, y = current
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and (nx, ny) not in self.obstacles:
                    queue.append((nx, ny))

        return False

    def draw_grid(self):

        self.canvas.delete("all")
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="black")

        for (x, y) in self.obstacles:
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                         (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                         fill="red", tag="obstacle")

        for (x, y) in self.traps:
            self.canvas.create_rectangle(x * self.cell_size, y * self.cell_size,
                                         (x + 1) * self.cell_size, (y + 1) * self.cell_size,
                                         fill="yellow", tag="trap")

        px, py = self.player_position
        self.canvas.create_oval(px * self.cell_size + 5, py * self.cell_size + 5,
                                (px + 1) * self.cell_size - 5, (py + 1) * self.cell_size - 5,
                                fill="blue", tag="player")


        gx, gy = self.goal_position
        self.canvas.create_rectangle(gx * self.cell_size + 5, gy * self.cell_size + 5,
                                     (gx + 1) * self.cell_size - 5, (gy + 1) * self.cell_size - 5,
                                     fill="green", tag="goal")

    def move_player(self, dx, dy):
        new_x = self.player_position[0] + dx
        new_y = self.player_position[1] + dy

        if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
            if (new_x, new_y) not in self.obstacles:
                self.player_position = [new_x, new_y]
                self.steps += 1

                if (new_x, new_y) in self.traps:
                    self.time_remaining -= 5
                    self.traps.remove((new_x, new_y))

                if self.steps % 5 == 0:
                    self.generate_obstacles()

                self.check_goal()
                self.update_progress_bar()
                self.draw_grid()

    def check_goal(self):
        if self.player_position == self.goal_position:
            if self.level < self.max_level:
                self.display_transition_message(
                    i18n.translations.get('Level {level} Complete!', 'Level {level} Complete!').format(
                        level=self.level))
                self.level += 1
                self.update_level_label()
                self.new_window.after(1000, self.start_level)
            else:
                self.running = False
                self.display_message(
                    i18n.translations.get('You Win!', 'You Win!'),
                    i18n.translations.get('Congratulations, you completed all levels!',
                                          'Congratulations, you completed all levels!')
                )

                global control
                control.set(control.get() + 1)
                if key_window_instance:
                    key_window_instance.update_control_text()

    def update_level_label(self):
        self.level_label.config(text=f"{i18n.translations.get('Level:', 'Level:')} {self.level}")

    def display_transition_message(self, message):
        transition_label = tk.Label(self.new_window, text=message, font=("Arial", 18), fg="blue", bg="white")
        transition_label.pack(pady=10)
        self.new_window.after(1000, transition_label.destroy)

    def update_timer(self):
        if self.running:
            self.time_remaining -= 1
            self.timer_label.config(text=f"{i18n.translations.get('Time Left:', 'Time Left:')} {self.time_remaining}{i18n.translations.get('s', 's')}")
            if self.time_remaining <= 0:
                self.running = False
                self.freeze_game()
                self.display_message(
                    i18n.translations.get('Time Out!', 'Time Out!'),
                    i18n.translations.get('You ran out of time!', 'You ran out of time!')
                )
            else:
                self.new_window.after(1000, self.update_timer)

    def freeze_game(self):
        self.running = False

        self.new_window.unbind("<Up>")
        self.new_window.unbind("<Down>")
        self.new_window.unbind("<Left>")
        self.new_window.unbind("<Right>")

        self.canvas.create_rectangle(0, 0, self.grid_size * self.cell_size,
                                     self.grid_size * self.cell_size,
                                     fill="black", stipple="gray50", tags="freeze")

    def display_message(self, title, message):

        msg_window = tk.Toplevel(self.new_window)
        msg_window.title(title)
        msg_window.geometry("500x200+250+250")
        msg_window.transient(self.new_window)
        msg_window.grab_set()
        msg_window.focus_force()


        tk.Label(msg_window, text=message, font=("Arial", 16)).pack(pady=20)

        tk.Button(msg_window, text=i18n.translations.get('Quit', 'Quit'), command=self.new_window.destroy).pack(pady=10)

class MastermindGame:
    def __init__(self, root):

        self.new_window = tk.Toplevel(root)
        self.new_window.title(i18n.translations.get('Mastermind Game', 'Mastermind Game'))
        self.new_window.geometry("600x700+400+75")
        self.new_window.configure(bg="lightgray")
        self.new_window.iconbitmap("game_icon.ico")

        self.code_length = 4
        self.max_attempts = 10
        self.colors = [
            i18n.translations.get("Red", "Red"),
            i18n.translations.get("Blue", "Blue"),
            i18n.translations.get("Green", "Green"),
            i18n.translations.get("Yellow", "Yellow"),
            i18n.translations.get("Purple", "Purple"),
            i18n.translations.get("Orange", "Orange")
        ]
        self.secret_code = random.sample(self.colors, k=self.code_length)
        self.attempts = 0


        self.create_widgets()

        self.color_to_tk_color = {
            i18n.translations.get("Red", "Red"): "red",
            i18n.translations.get("Blue", "Blue"): "blue",
            i18n.translations.get("Green", "Green"): "green",
            i18n.translations.get("Yellow", "Yellow"): "yellow",
            i18n.translations.get("Purple", "Purple"): "purple",
            i18n.translations.get("Orange", "Orange"): "orange"
        }

    def create_widgets(self):

        tk.Label(self.new_window, text=i18n.translations.get('Mastermind Game', 'Mastermind Game'),
                 font=("Times New Roman", 24, "bold"), bg="lightgray").pack(pady=20)


        self.secret_label = tk.Label(self.new_window,
                                     text=i18n.translations.get('Secret Code: ???', 'Secret Code: ???'),
                                     font=("Times New Roman", 14), bg="lightgray")
        self.secret_label.pack(pady=10)


        feedback_frame = tk.Frame(self.new_window, bg="lightgray")
        feedback_frame.pack(fill="both", expand=True, pady=10)

        self.feedback_canvas = tk.Canvas(feedback_frame, bg="lightgray")
        self.feedback_canvas.pack(side="left", fill="both", expand=True)

        feedback_scrollbar = ttk.Scrollbar(feedback_frame, orient="vertical", command=self.feedback_canvas.yview)
        feedback_scrollbar.pack(side="right", fill="y")

        self.feedback_inner_frame = tk.Frame(self.feedback_canvas, bg="lightgray")
        self.feedback_canvas.create_window((0, 0), window=self.feedback_inner_frame, anchor="nw")
        self.feedback_canvas.configure(yscrollcommand=feedback_scrollbar.set)


        tk.Label(self.new_window, text=i18n.translations.get('Make Your Guess:', 'Make Your Guess:'),
                 font=("Times New Roman", 16), bg="lightgray").pack(pady=10)
        self.guess_buttons = []
        self.guess_colors = [None] * self.code_length
        guess_frame = tk.Frame(self.new_window, bg="lightgray")
        guess_frame.pack(pady=10)
        for i in range(self.code_length):
            button = tk.Button(guess_frame, text=i18n.translations.get('Select', 'Select'), width=10, height=2,
                               command=lambda idx=i: self.select_color(idx))
            button.grid(row=0, column=i, padx=10)
            self.guess_buttons.append(button)

        self.submit_button = ttk.Button(self.new_window, text=i18n.translations.get('Submit Guess', 'Submit Guess'),
                                        command=self.submit_guess, state="disabled")
        self.submit_button.pack(pady=20)


        self.status_label = tk.Label(self.new_window, text="", font=("Times New Roman", 14), fg="blue", bg="lightgray")
        self.status_label.pack(pady=10)

    def select_color(self, index):

        color_menu = tk.Toplevel(self.new_window)
        color_menu.title(i18n.translations.get('Select Color', 'Select Color'))
        color_menu.geometry("200x275+500+200")

        for color in self.colors:
            button = ttk.Button(color_menu, text=color, command=lambda c=color: self.set_color(index, c, color_menu))
            button.pack(pady=5)

    def set_color(self, index, color, menu):

        self.guess_colors[index] = color
        tk_color = self.color_to_tk_color.get(color, "white")
        self.guess_buttons[index].config(text=color, bg=tk_color)
        menu.destroy()


        if all(self.guess_colors):
            self.submit_button.config(state="normal")

    def submit_guess(self):
        self.attempts += 1
        guess = self.guess_colors[:]
        feedback_row = tk.Frame(self.feedback_inner_frame, bg="lightgray")
        feedback_row.pack(pady=5, fill="x", padx=5)


        feedback = [None] * self.code_length
        unmatched_code = []
        unmatched_guess = []


        for i in range(self.code_length):
            if guess[i] == self.secret_code[i]:
                feedback[i] = "green"
            else:
                unmatched_code.append(self.secret_code[i])
                unmatched_guess.append(guess[i])


        for i, color in enumerate(guess):
            if feedback[i] is None and color in unmatched_code:
                feedback[i] = "yellow"
                unmatched_code.remove(color)


        for i in range(self.code_length):
            if feedback[i] is None:
                feedback[i] = "white"


        for color in feedback:
            tk.Label(feedback_row, bg=color, width=2, height=1, relief="solid").pack(side="left", padx=2)


        tk.Label(feedback_row, text=" | ".join(guess), font=("Times New Roman", 12), bg="lightgray").pack(side="right", padx=10)


        self.guess_colors = [None] * self.code_length
        for button in self.guess_buttons:
            button.config(text=i18n.translations.get("Select", "Select"), bg="SystemButtonFace")
        self.submit_button.config(state="disabled")

        if feedback.count("green") == self.code_length:
            self.status_label.config(text=i18n.translations.get('Congratulations! You cracked the code!',
                                                                'Congratulations! You cracked the code!'), fg="green")
            self.end_game()


            global control
            control.set(control.get() + 1)
            if key_window_instance:
                key_window_instance.update_control_text()

        elif self.attempts == self.max_attempts:
            self.status_label.config(text=i18n.translations.get("Game Over!", "Game Over!"), fg="red")
            self.secret_label.config(
                text=f"{i18n.translations.get('Secret Code', 'Secret Code')}: {', '.join(self.secret_code)}")

            self.end_game()


        self.feedback_canvas.config(scrollregion=self.feedback_canvas.bbox("all"))

    def end_game(self):
        for button in self.guess_buttons:
            button.config(state="disabled")
        self.submit_button.config(state="disabled")

class FoodChemistryLab:
    def __init__(self, root):
        self.new_window = tk.Toplevel(root)
        self.new_window.title(i18n.translations.get("food_lab.title", "Food Chemistry Lab"))
        self.new_window.geometry("900x850+300+100")
        self.new_window.configure(bg="lightblue")

        self.ingredients = {
            i18n.translations.get("ingredients.milk", "Milk"): [
                i18n.translations.get("properties.sweet", "Sweet"),
                i18n.translations.get("properties.neutral", "Neutral"),
            ],
            i18n.translations.get("ingredients.lemon", "Lemon"): [
                i18n.translations.get("properties.sour", "Sour"),
                i18n.translations.get("properties.acidic", "Acidic"),
            ],
            i18n.translations.get("ingredients.spice", "Spice"): [
                i18n.translations.get("properties.hot", "Hot"),
            ],
            i18n.translations.get("ingredients.meat", "Meat"): [
                i18n.translations.get("properties.savory", "Savory"),
            ],
            i18n.translations.get("ingredients.baking_soda", "Baking Soda"): [
                i18n.translations.get("properties.neutral", "Neutral"),
                i18n.translations.get("properties.explosive", "Explosive"),
            ],
            i18n.translations.get("ingredients.honey", "Honey"): [
                i18n.translations.get("properties.sweet", "Sweet"),
                i18n.translations.get("properties.sticky", "Sticky"),
            ],
            i18n.translations.get("ingredients.vinegar", "Vinegar"): [
                i18n.translations.get("properties.sour", "Sour"),
                i18n.translations.get("properties.acidic", "Acidic"),
            ],
        }

        self.reactions = {
            (
                i18n.translations.get("properties.explosive", "Explosive"),
                i18n.translations.get("properties.acidic", "Acidic"),
            ): (
                i18n.translations.get("recipes.fizzy_bomb", "Fizzy Bomb"),
                i18n.translations.get("titles.basic", "Basic"),
            ),
            (
                i18n.translations.get("properties.sweet", "Sweet"),
                i18n.translations.get("properties.sour", "Sour"),
            ): (
                i18n.translations.get("recipes.candied_lemon", "Candied Lemon"),
                i18n.translations.get("titles.basic", "Basic"),
            ),
            (
                i18n.translations.get("properties.hot", "Hot"),
                i18n.translations.get("properties.neutral", "Neutral"),
            ): (
                i18n.translations.get("recipes.spicy_milk", "Spicy Milk"),
                i18n.translations.get("titles.basic", "Basic"),
            ),
            (
                i18n.translations.get("properties.sweet", "Sweet"),
                i18n.translations.get("properties.sticky", "Sticky"),
            ): (
                i18n.translations.get("recipes.honey_candy", "Honey Candy"),
                i18n.translations.get("titles.basic", "Basic"),
            ),
            (
                i18n.translations.get("properties.savory", "Savory"),
                i18n.translations.get("properties.hot", "Hot"),
            ): (
                i18n.translations.get("recipes.spicy_meat", "Spicy Meat"),
                i18n.translations.get("titles.basic", "Basic"),
            ),
        }

        self.intermediate_products = {}
        self.selected_ingredients = []
        self.score = 0
        self.discovered_recipes = set()

        self.create_widgets()

    def mix_ingredients(self):

        if not self.new_window.winfo_exists():
            return

        properties = []
        for ingredient in self.selected_ingredients:
            if ingredient in self.intermediate_products:
                properties.extend(self.intermediate_products[ingredient])
            else:
                properties.extend(self.ingredients.get(ingredient, []))

        properties = tuple(sorted(properties))

        found_recipe = None
        for reaction_key, (recipe, complexity) in self.reactions.items():
            if all(prop in properties for prop in reaction_key):
                found_recipe = (recipe, complexity)
                break

        if found_recipe:
            recipe_name, complexity = found_recipe
            if recipe_name not in self.discovered_recipes:
                self.reaction_label.config(
                    text=f"{i18n.translations.get('result.label', 'Result')}: {recipe_name}",
                    fg="green"
                )
                self.update_score(self.get_points_for_complexity(complexity))
                self.discovered_recipes.add(recipe_name)
                self.update_recipes(recipe_name, complexity)

                if " " in recipe_name:
                    self.intermediate_products[recipe_name] = list(properties)

                self.flash_reaction(self.reaction_label, "green")
                self.check_completion()
            else:
                self.reaction_label.config(
                    text=f"{i18n.translations.get('result.label', 'Result')}: {recipe_name} "
                         f"({i18n.translations.get('already_discovered', 'Already Discovered')})",
                    fg="blue"
                )
                self.flash_reaction(self.reaction_label, "blue")
        else:
            self.reaction_label.config(
                text=i18n.translations.get('result.failed', "Result: Failed Experiment!"), fg="red"
            )
            self.flash_reaction(self.reaction_label, "red")

        if self.new_window.winfo_exists():
            self.reset_selection()

    def check_completion(self):

        if len(self.discovered_recipes) == len(self.reactions):
            messagebox.showinfo(
                i18n.translations.get('congratulations.title', "Congratulations!"),
                i18n.translations.get('congratulations.message', "You discovered all recipes!")
            )
            global control
            control.set(control.get() + 1)
            if key_window_instance:
                key_window_instance.update_control_text()

            self.new_window.destroy()

    def create_widgets(self):

        tk.Label(self.new_window, text=i18n.translations.get('food_lab.title', "Food Chemistry Lab"),
                   font=("Times New Roman", 24, "bold"), bg="lightblue").pack(pady=20)

        ingredient_frame = tk.Frame(self.new_window, bg="lightblue")
        ingredient_frame.pack(pady=10)
        tk.Label(ingredient_frame, text=i18n.translations.get('ingredients.title', "Ingredients:"),
                 font=("Times New Roman", 16), bg="lightblue").pack(anchor="w")

        for ingredient in self.ingredients.keys():
            btn = ttk.Button(ingredient_frame, text=ingredient,
                             command=lambda ing=ingredient: self.add_ingredient(ing))
            btn.pack(side="left", padx=10, pady=5)


        selection_frame = tk.Frame(self.new_window, bg="lightblue")
        selection_frame.pack(pady=10)
        self.selected_label = tk.Label(selection_frame,
                                       text=i18n.translations.get('selection.label', "Selected: None"),
                                       font=("Times New Roman", 14), bg="lightblue")
        self.selected_label.pack(side="left", padx=5)
        ttk.Button(selection_frame, text=i18n.translations.get('reset.selection', "Reset Selection"),
                   command=self.reset_selection).pack(side="left", padx=5)


        button_frame = tk.Frame(self.new_window, bg="lightblue")
        button_frame.pack(pady=10)
        self.mix_button = ttk.Button(button_frame, text=i18n.translations.get('mix.button', "Mix Ingredients"),
                                     command=self.mix_ingredients, state="disabled")
        self.mix_button.pack(side="left", padx=5)


        self.reaction_label = tk.Label(self.new_window, text="", font=("Times New Roman", 16), bg="lightblue")
        self.reaction_label.pack(pady=10)


        self.score_label = tk.Label(self.new_window,
                                    text=f"{i18n.translations.get('score.label', 'Score')}: 0",
                                    font=("Times New Roman", 14), bg="lightblue")
        self.score_label.pack(pady=10)

        recipe_frame = tk.Frame(self.new_window, bg="lightblue")
        recipe_frame.pack(pady=10, fill="x")
        tk.Label(recipe_frame, text=i18n.translations.get('recipes.title', "Discovered Recipes:"),
                 font=("Times New Roman", 16), bg="lightblue").pack(anchor="w")
        self.recipe_list = tk.Text(recipe_frame, height=10, width=50, state="disabled", wrap="word")
        self.recipe_list.pack(padx=10, pady=5)


        self.create_info_table()

    def create_info_table(self):
        info_frame = tk.Frame(self.new_window, bg="white", bd=2, relief="solid")
        info_frame.pack(pady=10, padx=20, fill="x")

        tk.Label(
            info_frame,
            text=i18n.translations.get("Combinable Property Pairs", "Combinable Property Pairs"),
            font=("Times New Roman", 16, "bold"),
            bg="lightgray"
        ).pack(fill="x")

        table_frame = tk.Frame(info_frame)
        table_frame.pack(fill="x", padx=10, pady=5)


        scrollbar = ttk.Scrollbar(table_frame, orient="vertical")
        table = ttk.Treeview(
            table_frame,
            columns=("property_pair",),
            show="headings",
            height=8,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=table.yview)
        scrollbar.pack(side="right", fill="y")
        table.pack(side="left", fill="x", expand=True)


        table.heading(
            "property_pair",
            text=i18n.translations.get("Property Pair", "Property Pair")
        )
        table.column("property_pair", anchor="center")


        for reaction_key in self.reactions.keys():
            property_pair = " + ".join(reaction_key)
            table.insert("", "end", values=(property_pair,))

        self.info_table = table

    def add_ingredient(self, ingredient):

        if len(self.selected_ingredients) < 2:
            self.selected_ingredients.append(ingredient)
            selected_text = i18n.translations.get("Selected", "Selected")
            ingredients = ', '.join(self.selected_ingredients)
            self.selected_label.config(text=f"{selected_text}: {ingredients}")
            if len(self.selected_ingredients) > 1:
                self.mix_button.config(state="normal")

            self.flash_reaction(self.selected_label, "yellow")

    def reset_selection(self):

        if self.new_window.winfo_exists():
            self.selected_ingredients = []
            reset_text = i18n.translations.get("Selected: None", "Selected: None")
            self.selected_label.config(text=reset_text)
            self.mix_button.config(state="disabled")

    def get_points_for_complexity(self, complexity):
        points = {"Basic": 5, "Intermediate": 10, "Advanced": 15}
        return points.get(complexity, 5)

    def flash_reaction(self, widget, color):

        original_color = widget.cget("bg")
        widget.config(bg=color)
        for i in range(3):
            self.new_window.after(100 * i, lambda: widget.config(bg="white" if i % 2 == 0 else color))
        self.new_window.after(300, lambda: widget.config(bg=original_color))

    def update_score(self, points):
        self.score += points
        score_text = i18n.translations.get("Score", "Score")
        self.score_label.config(text=f"{score_text}: {self.score}")

    def update_recipes(self, recipe, complexity):
        self.recipe_list.config(state="normal")
        recipe_entry = f"{recipe} ({complexity})\n"
        self.recipe_list.insert("end", recipe_entry)
        self.recipe_list.config(state="disabled")
        self.update_info_table()

    def update_info_table(self):
        for recipe, properties in self.intermediate_products.items():
            if not any(self.info_table.item(item)["values"][0] == recipe for item in self.info_table.get_children()):
                property_text = i18n.translations.get("Property Pair", "Property Pair")
                self.info_table.insert("", "end", values=(recipe, ", ".join(properties)))

def on_exit():
    if messagebox.askokcancel(
            i18n.translations.get("Quit", "Quit"),
            i18n.translations.get("Do you want to quit?", "Do you want to quit?")
    ):

        for window in win.winfo_children():
            try:
                window.destroy()
            except tk.TclError:
                pass
        try:
            win.destroy()
        except tk.TclError:
            pass

if __name__ == "__main__":
    initialize_database()
    win = tk.Tk()
    control = tk.IntVar(win, 0)
    main_menu = MainMenuWindow(win)
    win.protocol("WM_DELETE_WINDOW", on_exit)
    win.mainloop()



