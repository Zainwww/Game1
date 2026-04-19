import random
import tkinter
import customtkinter as ctk
from PIL import Image
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="kata_baku"
)
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM kata_baku")
myresult = mycursor.fetchall()
nomer_soal = random.randint(1, len(myresult))
print(myresult[nomer_soal-1])


root = ctk.CTk()
root.geometry("1365x768")
root.title("Quiz Minigame")

class AnimatedImage:
    """Simple animated sprite that can load sprite-sheets or multi-frame images,
    place itself at absolute coordinates, and switch animation sources.
    """
    def __init__(self, parent, image_paths, x=0, y=0, delay=120, frame_count=1, scale=1.0):
        self.parent = parent
        self.paths = image_paths if isinstance(image_paths, (list, tuple)) else [image_paths]
        self.delay = delay
        self.frame_count = frame_count
        self.scale = scale
        self.frames = []
        self.sizes = []
        self.x = x
        self.y = y

        self._load_frames(self.paths)

        if not self.frames:
            raise RuntimeError("No frames loaded for animation")

        self.label = ctk.CTkLabel(self.parent, image=self.frames[0], text="")
        # place using bottom-center anchor so y is the ground/top-of-foot coordinate
        self.label.place(x=self.x, y=self.y, anchor='s')
        self._index = 0
        self._running = False

    def _load_frames(self, paths):
        self.frames = []
        self.sizes = []
        for p in paths:
            try:
                img = Image.open(p)
            except Exception as e:
                print(f"Could not open {p}: {e}")
                continue

            n_frames = getattr(img, "n_frames", 1)
            if n_frames > 1:
                try:
                    for i in range(n_frames):
                        img.seek(i)
                        frame = img.copy().convert("RGBA")
                        display_w = int(frame.width * self.scale)
                        display_h = int(frame.height * self.scale)
                        self.frames.append(ctk.CTkImage(light_image=frame, size=(display_w, display_h)))
                        self.sizes.append((display_w, display_h))
                except Exception:
                    pass
            elif self.frame_count and self.frame_count > 1:
                w, h = img.size
                fw = w // self.frame_count
                for i in range(self.frame_count):
                    box = (i * fw, 0, (i + 1) * fw, h)
                    frame = img.crop(box).convert("RGBA")
                    display_w = int(frame.width * self.scale)
                    display_h = int(frame.height * self.scale)
                    self.frames.append(ctk.CTkImage(light_image=frame, size=(display_w, display_h)))
                    self.sizes.append((display_w, display_h))
            else:
                frame = img.copy().convert("RGBA")
                display_w = int(frame.width * self.scale)
                display_h = int(frame.height * self.scale)
                self.frames.append(ctk.CTkImage(light_image=frame, size=(display_w, display_h)))
                self.sizes.append((display_w, display_h))

        # store first-frame size for placement calculations
        if self.sizes:
            self.img_width, self.img_height = self.sizes[0]
        else:
            self.img_width = self.img_height = 0

    def start(self):
        if not self._running:
            self._running = True
            self._animate()

    def stop(self):
        self._running = False

    def _animate(self):
        if not self._running:
            return
        self._index = (self._index + 1) % len(self.frames)
        self.label.configure(image=self.frames[self._index])
        self.parent.after(self.delay, self._animate)

    def set_images(self, image_paths, frame_count=1):
        self.frame_count = frame_count
        self._load_frames(image_paths if isinstance(image_paths, (list, tuple)) else [image_paths])
        self._index = 0
        if self.frames:
            self.label.configure(image=self.frames[0])

# --- Build UI similar to screenshot ---
WIDTH, HEIGHT = 1365, 768

# Colors
SKY_COLOR = "#E9E9E9"
CARD_COLOR = SKY_COLOR  # match boys background / sky tone

canvas = tkinter.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
canvas.configure(bg=SKY_COLOR)
canvas.pack(fill="both", expand=True)

# top-right counter
counter_text = canvas.create_text(WIDTH - 40, 30, text="12/50", anchor="ne", font=("Courier", 20), fill="black")

# central question card (rounded-ish look using CTkFrame)
card_w, card_h = 820, 360
card_x = (WIDTH - card_w) // 2
card_y = 110
card = ctk.CTkFrame(root, width=card_w, height=card_h, fg_color=CARD_COLOR, corner_radius=16, border_width=2, border_color="#746a6a")
card.place(x=card_x, y=card_y)
question_label = ctk.CTkLabel(card, text="Your Question !?", font=("Courier", 36), text_color="black")
question_label.place(relx=0.5, rely=0.32, anchor='center')

# Buttons at bottom of card
def on_wrong():
    options = [1,2]
    handle_wrong()


def on_correct():
    options = [1,2]
    print("Correct pressed")

# default options placeholder (will be replaced per question)
options = [1, 2]

def shuffle_options(opts):
  """Return a new list with the items of `opts` shuffled (non-destructive)."""
  shuffled = list(opts)
  random.shuffle(shuffled)
  return shuffled


def prepare_question():
    """Prepare the current question and shuffled options from `myresult` and
    `nomer_soal`. Returns (question_text, btn1_text, btn2_text, on_select).
    The code assumes that the DB row format places the question at index 1 and
    the correct answer at index 2 (with an optional second option at index 3).
    """
    row = myresult[nomer_soal - 1]

    # try to extract sensible fields from DB row
    if isinstance(row, (list, tuple)) and len(row) >= 4:
        question_text = "mana yang baku?"
        opts = [str(row[1]), str(row[2])]
    elif isinstance(row, (list, tuple)) and len(row) == 3:
        question_text = "mana yang baku?"
        opts = [str(row[1]), str(row[2])]
    else:
        # fallback when row is a single string or unexpected format
        question_text = str(row)
        opts = [str(row), ""]

    # assume opts[0] is the correct answer
    correct = opts[0]
    shuffled = shuffle_options(opts)
    btn_1_text = shuffled[0] if len(shuffled) > 0 else ""
    btn_2_text = shuffled[1] if len(shuffled) > 1 else ""

    def on_select(choice_text):
        if choice_text == correct:
            print("Correct")
            return True
        else:
            print("Wrong")
            return False

    # quick console display for demo / debugging
    print(f"Question #{nomer_soal}: {question_text}")
    print("Button 1 label:", btn_1_text)
    print("Button 2 label:", btn_2_text)

    return question_text, btn_1_text, btn_2_text, on_select


# current on_select callback (updated each question)
current_on_select = None


def load_question():
    """Randomize `nomer_soal`, prepare the question, and update UI widgets."""
    global nomer_soal, current_on_select
    nomer_soal = random.randint(1, len(myresult))
    question, btn1_label, btn2_label, on_select = prepare_question()
    current_on_select = on_select
    # update UI
    try:
        question_label.configure(text=question)
    except Exception:
        pass
    try:
        btn_1.configure(text=btn1_label)
        btn_2.configure(text=btn2_label)
    except Exception:
        pass


def handle_selection(choice_text):
    """Call current question callback; if wrong, run handle_wrong(); then load next question."""
    global current_on_select
    if current_on_select is None:
        return
    ok = current_on_select(choice_text)
    if not ok:
        handle_wrong()
    load_question()


# create buttons (commands read current text from the button when clicked)
btn_1 = ctk.CTkButton(card, text="", fg_color="#F4A6A6", hover_color="#f2a3a3", command=lambda: handle_selection(btn_1.cget('text')), width=160, height=48, corner_radius=12)
btn_1.place(relx=0.35, rely=0.78, anchor='center')
btn_2 = ctk.CTkButton(card, text="", fg_color="#B9E39A", hover_color="#A8D785", command=lambda: handle_selection(btn_2.cget('text')), width=160, height=48, corner_radius=12)
btn_2.place(relx=0.65, rely=0.78, anchor='center')

# load the first question into the UI
load_question()

# ground strip
GROUND_H = 96
ground = canvas.create_rectangle(0, HEIGHT - GROUND_H, WIDTH, HEIGHT, fill="#5D8931", outline="")

# Create and position multiple boys along the ground
NUM_BOYS = 4
boy_sprites = []
boy_states = []  # 'alive' or 'dead'

# approximate x positions (left -> right)
start_x = 80
spacing = 100
# place bottom of sprite exactly at top of ground so they stand on the green
base_y = HEIGHT - GROUND_H

for i in range(NUM_BOYS):
    x = start_x + i * spacing
    # start all with attack animation
    try:
        # use a slightly larger delay for smoother, slower animation
        sprite = AnimatedImage(root, ["5 Boy/Boy_attack.png"], x=x, y=base_y, delay=220, frame_count=4, scale=1.5)
    except Exception as e:
        print("Error creating sprite:", e)
        sprite = None
    boy_sprites.append(sprite)
    boy_states.append('alive')

# start all sprites together for more consistent timing
for s in boy_sprites:
    try:
        if s is not None:
            s.start()
    except Exception:
        pass

# wrong-answer handling: kill the right-most alive boy
def handle_wrong():
    # find rightmost alive index
    for idx in range(len(boy_sprites) - 1, -1, -1):
        if boy_states[idx] == 'alive' and boy_sprites[idx] is not None:
            # switch to death sprite
            try:
                boy_sprites[idx].stop()
                boy_sprites[idx].set_images(["5 Boy/Boy_death.png"], frame_count=4)
                # if death has animations, start them
                boy_sprites[idx].start()
            except Exception as e:
                print("Could not set death image:", e)
            boy_states[idx] = 'dead'
            break
    check_defeat()

def check_defeat():
    if all(s == 'dead' for s in boy_states):
        show_defeat()

def show_defeat():
    # Full-screen defeat box with black border
    box = ctk.CTkFrame(root, width=WIDTH, height=HEIGHT, fg_color="#111111", corner_radius=0, border_width=6, border_color="#000000")
    box.place(x=0, y=0)

    defeat_label = ctk.CTkLabel(box, text="DEFEAT", font=("Courier", 72), text_color="white")
    defeat_label.place(relx=0.5, rely=0.4, anchor='center')

    # Replay: reset game state and continue; Exit: close app
    def replay():
        for i in range(len(boy_sprites)):
            boy_states[i] = 'alive'
            try:
                boy_sprites[i].set_images(["5 Boy/Boy_attack.png"], frame_count=4)
                boy_sprites[i].start()
            except Exception:
                pass
        try:
            box.destroy()
        except Exception:
            pass
        load_question()

    def exit_game():
        try:
            box.destroy()
        except Exception:
            pass
        root.destroy()

    replay_btn = ctk.CTkButton(box, text="Replay", command=replay)
    replay_btn.place(relx=0.42, rely=0.6, anchor='center')
    restart_btn = ctk.CTkButton(box, text="Exit", command=exit_game)
    restart_btn.place(relx=0.58, rely=0.6, anchor='center')

root.mainloop()
