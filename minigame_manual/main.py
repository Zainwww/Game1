import customtkinter as ctk
import os
from PIL import Image
import time 
import json
import random

monster_x = 0
monster_spawned=True
time = 0
score = 0
with open('kata_baku.json','r') as file:
    data = json.load(file)
nomor = random.randint(0,len(data)-1)
undi = ["kata_baku","kata_tidak_baku"]
random.shuffle(undi)
jawaban_benar = data[nomor]['kata_baku']

class Frame_top(ctk.CTkFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)



class Frame_rear_mid(ctk.CTkFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)


class Frame_mid(ctk.CTkFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        self.grid_rowconfigure((0,1),weight=2)
        self.grid_columnconfigure((0,1,2),weight = 2)

        # soal = ctk.CTkFrame(self,fg_color="#FFFFFF")
        # soal.place(relx=0.5, rely=0.3, anchor=ctk.CENTER)
        # pil_1 = ctk.CTkFrame(self,fg_color="#FFA4A4",width = 200,height= 60)
        # pil_1.place(relx=0.1,rely=0.9, anchor=ctk.SW)
        # pil_2 = ctk.CTkFrame(self,fg_color="#B9DB9B",width = 200,height= 60)
        # pil_2.place(relx=0.9,rely=0.9, anchor=ctk.SE)

        
        # self.jawaban_1 = data[nomor][undi.pop()]
        # self.button_1 = ctk.CTkButton(pil_1,text=self.jawaban_1,font=('Courier Prime',32),fg_color="#FFA4A4",text_color="#000000",command=lambda :self.check_jawaban(self.jawaban_1,self.button_1) )
        # self.button_1.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)
        # self.jawaban_2 = data[nomor][undi.pop()]
        # self.button_2 = ctk.CTkButton(pil_2,text= self.jawaban_2,font=('Courier Prime',32),fg_color="#B9DB9B",text_color="#000000",command=lambda :self.check_jawaban(self.jawaban_2,self.button_2) )
        # self.button_2.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)

    def check_jawaban(self,jawaban,button):
        global score
        if jawaban ==jawaban_benar:
            score+=10
        print(score)
        self.update_jawaban()
    
    def update_jawaban(self):
        global nomor,undi,jawaban_benar
        if len(undi)==0:
            nomor = random.randint(0,len(data)-1)
            undi = ["kata_baku","kata_tidak_baku"]
            random.shuffle(undi)
        jawaban_benar = data[nomor]["kata_baku"]
        self.jawaban_1 = data[nomor][undi.pop()]
        self.jawaban_2 = data[nomor][undi.pop()]
        self.button_1.configure(text= self.jawaban_1)
        self.button_2.configure(text = self.jawaban_2)

        
class Frame_ground(ctk.CTkFrame):
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        self.grid_rowconfigure((0,1), weight=2)
        self.grid_columnconfigure((0,1) ,weight=2)
        ground = ctk.CTkFrame(self,fg_color="#5D8931",height=100)
        ground.grid(row=1,column=0,columnspan = 2, sticky="nsew")
        human = ctk.CTkFrame(self,fg_color="#E2E2E2",height=100,width=300)
        human.grid(row=0,column=0, columnspan = 2,sticky="nsew")
        chara1 = character(human, start=100)
        chara2 = character(human, start=200)
        chara3 = character(human, start=300)
        chara4 = character(human, start=400)
        monster1 = monster(human)
        self.kotak = ctk.CTkFrame(self,width=200,height=125)
        self.kotak.place(x = monster_x+25,y=139)
       
        # character handles its own animation scheduling
        

class character(ctk.CTkLabel):
    
    def __init__(self,master,start,**kwargs):
        super().__init__(master,**kwargs)
        self.animation = 1
        self.ind = 0
        self.x = start
        self.master_frame = master
        dir_path_attack = os.path.join(os.path.dirname(os.path.realpath(__file__)), "5 Boy", "Boy_attack")
        dir_path_walk = os.path.join(os.path.dirname(os.path.realpath(__file__)), "5 Boy", "Boy_walk")
        dir_path_idle = os.path.join(os.path.dirname(os.path.realpath(__file__)), "5 Boy", "Boy_idle")
        self.list_image_attack = [os.path.join(dir_path_attack, x) for x in os.listdir(dir_path_attack)]
        self.list_image = [os.path.join(dir_path_walk, x) for x in os.listdir(dir_path_walk)]
        self.list_image_idle = [os.path.join(dir_path_idle, x) for x in os.listdir(dir_path_idle)]
        my_image = ctk.CTkImage(light_image=Image.open(self.list_image[self.ind]),
                                dark_image=Image.open(self.list_image[self.ind]),
                                size=(46,52))
        self.my_label = ctk.CTkLabel(master, text="", image=my_image)
        self.my_label.place(x=self.x,relx =0,anchor = "s")
        
        self.my_label.after(100, self._animate)
    def _Frame(self):
        self.ind = (self.ind + 1) % len(self.list_image)
        self.idle = ctk.CTkImage(light_image=Image.open(self.list_image_idle[self.ind]),
                           dark_image=Image.open(self.list_image_idle[self.ind]),
                           size=(46,52))
        self.idle_rot = ctk.CTkImage(light_image=Image.open(self.list_image_idle[self.ind]).transpose(Image.FLIP_LEFT_RIGHT),
                           dark_image=Image.open(self.list_image_idle[self.ind]).transpose(Image.FLIP_LEFT_RIGHT),
                           size=(46,52))
        self.raw = ctk.CTkImage(light_image=Image.open(self.list_image[self.ind]).transpose(Image.FLIP_LEFT_RIGHT),
                           dark_image=Image.open(self.list_image[self.ind]).transpose(Image.FLIP_LEFT_RIGHT),
                           size=(46,52))
        self.img = ctk.CTkImage(light_image=Image.open(self.list_image[self.ind]),
                           dark_image=Image.open(self.list_image[self.ind]),
                           size=(46,52))
        self.gacha = [self.raw,self.img,self.idle,self.idle_rot]

    def _animate(self):
        global time
        time+=1
        self._Frame()
        if monster_spawned:
            self._go_to_enemies()
        else:
            if self.x >50 and self.x<(self.master_frame.winfo_width()-50) and time%50==0:
                self.animation =random.randint(0,3)
                self.my_label.configure(image = self.gacha[self.animation])
            if self.x<50:
                self.animation = 1
                self.my_label.configure(image = self.gacha[self.animation])
            elif self.x>(self.master_frame.winfo_width()-50):
                self.animation = 0
                self.my_label.configure(image = self.gacha[self.animation])
            else:
                self.my_label.configure(image=self.gacha[self.animation])
            animate = self.my_label.cget("image")

            if animate==self.img:
                self._move_right()
            if animate==self.raw:
                self._move_left()
            self.my_label.after(50, self._animate)


    def _move_right(self):
        self.x += random.randint(7,14)
        self.my_label.place(x=self.x, rely=1.0, anchor="s")
    
    def _move_left(self):
        self.x -= random.randint(7,14)
        self.my_label.place(x=self.x, rely=1.0, anchor="s")

    def _attack_enemies(self,direction):
        self.attack = ctk.CTkImage(light_image=Image.open(self.list_image_attack[self.ind]),
                           dark_image=Image.open(self.list_image_attack[self.ind]),
                           size=(46,52))
        self.attack_rot = ctk.CTkImage(light_image=Image.open(self.list_image_attack[self.ind]).transpose(Image.FLIP_LEFT_RIGHT),
                           dark_image=Image.open(self.list_image_attack[self.ind]).transpose(Image.FLIP_LEFT_RIGHT),
                           size=(46,52))
        if direction == "R":
            self.my_label.configure(image = self.attack)
        elif direction=="L":
            self.my_label.configure(image = self.attack_rot)
        else:
            pass

    def _go_to_enemies(self):
        global monster_x
        self._Frame()
        if abs(self.x-monster_x)<50:
            self._attack_enemies("R")
        elif abs(self.x-(monster_x+288))<50:
            self._attack_enemies("L")
        elif self.x<monster_x:
            self.animation = 1
            self.my_label.configure(image = self.gacha[self.animation])
            self._move_right()
        elif self.x>monster_x:
            self.animation = 0
            self.my_label.configure(image = self.gacha[self.animation])
            self._move_left()
        self.my_label.after(50, self._animate)

class monster(ctk.CTkLabel):
    
    def __init__(self,master,**kwargs):
        super().__init__(master,**kwargs)
        global monster_x
        monster_x =random.randint(50,1800)
        self.health = 100
        
        self.ind = 0
        dir_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "monster")
        self.list_image = [os.path.join(dir_path, x) for x in os.listdir(dir_path)]
        my_image = ctk.CTkImage(light_image=Image.open(self.list_image[self.ind]),
                                dark_image=Image.open(self.list_image[self.ind]),
                                size=(288,288))
        self.my_label = ctk.CTkLabel(master, text="", image=my_image)
        self.my_label.place(x = monster_x)
        self.progressbar = ctk.CTkProgressBar(master, orientation="horizontal",width=200,height=12,corner_radius=0,determinate_speed=5,progress_color="Blue")
        self.progressbar.set(0)
        self.progressbar.place(x=monster_x,y= 0)
        self.my_label.after(300, self._animate)
        
        # soal = ctk.CTkFrame(self.my_label,fg_color="#FFFFFF")
        # soal.place(relx=0.5, y=100, anchor=ctk.CENTER)
        # pil_1 = ctk.CTkFrame(self.my_label,fg_color="#FFA4A4",width = 200,height= 60)
        # pil_1.place(relx=0.1,y=100, anchor=ctk.SW)
        # pil_2 = ctk.CTkFrame(self.my_label,fg_color="#B9DB9B",width = 200,height= 60)
        # pil_2.place(relx=0.9,y=100, anchor=ctk.SE)

        
        # self.jawaban_1 = data[nomor][undi.pop()]
        # self.button_1 = ctk.CTkButton(pil_1,text=self.jawaban_1,font=('Courier Prime',32),fg_color="#FFA4A4",text_color="#000000",command=lambda :self.check_jawaban(self.jawaban_1,self.button_1) )
        # self.button_1.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)
        # self.jawaban_2 = data[nomor][undi.pop()]
        # self.button_2 = ctk.CTkButton(pil_2,text= self.jawaban_2,font=('Courier Prime',32),fg_color="#B9DB9B",text_color="#000000",command=lambda :self.check_jawaban(self.jawaban_2,self.button_2) )
        # self.button_2.place(relx=0.5,rely=0.5,anchor=ctk.CENTER)

    def check_jawaban(self,jawaban,button):
        global score
        if jawaban ==jawaban_benar:
            score+=10
        print(score)
        self.update_jawaban()
    
    def update_jawaban(self):
        global nomor,undi,jawaban_benar
        if len(undi)==0:
            nomor = random.randint(0,len(data)-1)
            undi = ["kata_baku","kata_tidak_baku"]
            random.shuffle(undi)
        jawaban_benar = data[nomor]["kata_baku"]
        self.jawaban_1 = data[nomor][undi.pop()]
        self.jawaban_2 = data[nomor][undi.pop()]
        self.button_1.configure(text= self.jawaban_1)
        self.button_2.configure(text = self.jawaban_2)

    def _animate(self):
        global time
        self.ind = (self.ind + 1) % len(self.list_image)
        img = ctk.CTkImage(light_image=Image.open(self.list_image[self.ind]),
                           dark_image=Image.open(self.list_image[self.ind]),
                           size=(288,288))
        self.my_label.configure(image=img)
        self.progressbar.step()
        print(self.progressbar.get())
        self.my_label.after(300, self._animate)
        if time%200==0:
            self.respawn()
    
    def respawn(self):
         global monster_x
         monster_x =random.randint(50,1800)
         self.progressbar.set(0)
         self.progressbar.place(x=monster_x,y= 0)
         self.my_label.place(x = monster_x)

    # def health_bar(self):

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self._fg_color = "#E2E2E2"
        self.geometry("1920x1080")
        self.grid_rowconfigure((0,1,2), weight=2)# configure grid system
        self.grid_columnconfigure((0,1,2), weight=2)

        self.my_frame = Frame_top(master=self,corner_radius = 0,fg_color = "#E2E2E2")
        self.my_frame.grid(row=0, column=0, columnspan = 3, sticky="nsew")
        self.my_frame = Frame_rear_mid(master=self,corner_radius = 0,fg_color = "#E2E2E2")
        self.my_frame.grid(row=1, column=0, sticky="nsew")
        self.my_frame = Frame_mid(master=self,corner_radius = 66,height = 400,fg_color = "#FFFFFF")
        self.my_frame.grid(row=1, column=1, sticky="nsew")
        self.my_frame.pack_propagate(False)
        self.my_frame = Frame_rear_mid(master=self,corner_radius = 0,fg_color = "#E2E2E2")
        self.my_frame.grid(row=1, column=2, sticky="nsew")
        self.my_frame = Frame_ground(master=self,corner_radius = 0)
        self.my_frame.grid(row=2, column=0, columnspan = 3, sticky="nsew")
    
app = App()
app.mainloop()



