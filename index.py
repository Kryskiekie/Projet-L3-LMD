#*******************************************************************************
#----------------------------------LANDA YE------------------------------------*
#                                                                              *
#                           par KIEKIE YEDIDIA Chris                           *
#                                                                              *
#                                 2023-2024                                    *
#*******************************************************************************
import tkinter as tk
from PIL import Image, ImageTk
import subprocess
from time import sleep

def lancer_autre_programme():
    subprocess.Popen(["python", "main.py"])
    sleep(5)
    root.destroy()

# Créer une fenêtre tkinter
root = tk.Tk()
root.title("LANDA YE")
largeur:int = 728
hauteur:int = 473

# Récupérer la résolution de l'écran
largeur_ecran:int = root.winfo_screenwidth()
hauteur_ecran:int = root.winfo_screenheight()

# Calculer les coordonnées pour centrer la fenêtre
x:int = (largeur_ecran - largeur) // 2
y:int = (hauteur_ecran - hauteur) // 2

root.geometry(f"{largeur}x{hauteur}+{x}+{y}")

# Charger l'image
image = Image.open("background.png")
photo = ImageTk.PhotoImage(image)

# Créer un label pour afficher l'image de fond
background_label = tk.Label(root, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Créer un lbutton!
button = tk.Button(root, width=15, height=2, text="Begin Tracking", bd=0, bg="#B97A57", fg="white", font=("Calibri", 12, "bold"))
button.place(x=300, y=hauteur//2)
button.config(command=lancer_autre_programme)

# Lancer la boucle principale de l'interface graphique
root.mainloop()