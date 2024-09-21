import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno
from tkinterPdfViewer import tkinterPdfViewer as pdf
from tkinter.messagebox import showerror
import os
from PyPDF2 import PdfReader
from gtts import gTTS
import threading
import playsound

import time


# Créer la fenêtre principale
window = tk.Tk()
window.title("INTERACTION - LECTURE PDF")
window.geometry("1360x680")
window.minsize(600, 350)

# Changer la couleur de fond
window.configure(bg='lightblue')


# Fonction pour quitter l'application
def quit_app():
    if askyesno('Message', 'Êtes-vous sûr de vouloir quitter le programme?'):
        window.destroy()


# Variable globale pour stocker le chemin du fichier PDF et le texte extrait
pdf_file_path = None
text_content = ""
is_paused = False
is_stopped = False

# Définir text_widget comme une variable globale
text_widget = None


# Fonction pour ouvrir un fichier PDF
def open_file():
    global pdf_file_path
    pdf_file_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_file_path:
        display_pdf(pdf_file_path)
        read_pdf()


# Fonction pour afficher le PDF
def display_pdf(file_path):
    v1 = pdf.ShowPdf()
    v2 = v1.pdf_view(canvas, pdf_location=file_path, width=canvas.winfo_width(), height=canvas.winfo_height())
    v2.pack(side="left", fill="both", expand=True)


# Fonction pour lire le contenu du PDF
def read_pdf():
    global text_content
    if pdf_file_path:
        with open(pdf_file_path, 'rb') as file:
            reader = PdfReader(file)
            text_content = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text_content += page.extract_text()
            display_text(text_content)


# Fonction pour afficher le texte extrait
def display_text(text):
    global text_widget
    if text_widget:
        text_widget.delete(1.0, tk.END)
        text_widget.insert(tk.END, text)
    else:
        showerror("Erreur", "Le widget de texte n'est pas initialisé.")


# Fonction pour vider le canvas
def clear_canvas():
    if hasattr(canvas, 'pdf_widget'):
        canvas.pdf_widget.destroy()
        del canvas.pdf_widget
    canvas.delete("all")


# Fonction pour démarrer la lecture
def start_reading():
    global is_paused, is_stopped
    if not text_content:
        showerror("Erreur", "Aucun texte à lire. Veuillez ouvrir un fichier PDF valide.")
        return
    is_paused = False
    is_stopped = False
    threading.Thread(target=read_aloud).start()


# Fonction pour lire le texte à haute voix
"""def read_aloud():
    global is_paused, is_stopped
    tts = gTTS(text_content, lang='fr')
    tts.save("temp_audio.mp3")
    playsound.playsound("temp_audio.mp3", block=False)
    while not is_stopped:
        if is_paused:
            playsound.playsound("temp_audio.mp3", block=True)"""


def read_aloud():
    global is_paused, is_stopped
    backoff_time = 1  # Temps initial d'attente en secondes
    max_backoff_time = 60  # Temps maximum d'attente en secondes
    while True:
        try:
            tts = gTTS(text_content, lang='fr')
            tts.save("temp_audio.mp3")
            playsound.playsound("temp_audio.mp3", block=False)
            break  # Sortir de la boucle si la requête réussit
        except gTTS.tts.gTTSError as e:
            if "429" in str(e):
                print(f"Erreur 429: Trop de requêtes. Réessayer dans {backoff_time} secondes.")
                time.sleep(backoff_time)
                backoff_time = min(backoff_time * 2, max_backoff_time)  # Augmenter le temps d'attente
            else:
                raise e  # Réélever l'exception si ce n'est pas une erreur 429

    while not is_stopped:
        if is_paused:
            playsound.playsound("temp_audio.mp3", block=True)


# Fonction pour mettre en pause la lecture
def pause_reading():
    global is_paused
    is_paused = not is_paused


# Fonction pour arrêter la lecture
def stop_reading():
    global is_stopped
    is_stopped = True
    playsound.playsound("temp_audio.mp3", block=False)


# Fonction pour vider le canvas
"""def clear_canvas():
    if hasattr(canvas, 'pdf_widget'):
        canvas.pdf_widget.destroy()
        del canvas.pdf_widget
    canvas.delete("all")"""

frame_PL = tk.Frame(window, bg='lightblue', relief='sunken', width=1000, height=50)
frame_PL.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')

frame_titre = tk.Frame(frame_PL, bg='lightblue', relief='sunken', width=50, height=50)
frame_titre.grid(row=0, column=0, padx=10, pady=0, sticky='nsew')

frame_zoom = tk.Frame(frame_PL, bg='lightblue', relief='sunken', width=20, height=50)
frame_zoom.grid(row=0, column=1, padx=20, pady=0, sticky='nsew')

# Ajouter le grand titre
title_label = tk.Label(frame_titre, text="APPLICATION INTERACTION - Lecture PDF",
                       font=("Berlin sans FB", 18, "bold"), fg='blue', bg='lightblue')
title_label.grid(row=0, column=0, columnspan=3, pady=5, padx=10)

button_plus = tk.Button(frame_zoom, text="Plus", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                        width=10, height=1)
button_plus.grid(row=0, column=0, padx=5, pady=5)

button_moin = tk.Button(frame_zoom, text="Moin", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                        width=10, height=1)
button_moin.grid(row=0, column=1, padx=5, pady=5)

# Créer un frame pour contenir le canvas et la scrollbar
frame_canvas = tk.Frame(window, bg='lightblue', width=600)
frame_canvas.grid(row=1, column=0, padx=5, pady=6, sticky='nsew')

canvas = tk.Canvas(frame_canvas, bg='white', width=600)
scrollbar = tk.Scrollbar(frame_canvas, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)
canvas.pack(side="left", fill="both", expand=True)


def resize_canvas(event):
    canvas.config(width=event.width, height=event.height)
    if hasattr(canvas, 'pdf_widget'):
        canvas.pdf_widget.pack(side="left", fill="both", expand=True)


canvas.bind("<Configure>", resize_canvas)

window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)

frame_btn = tk.Frame(window, bg='lightblue', relief='sunken', width=1000, height=50)
frame_btn.grid(row=1, column=1, padx=30, pady=5, columnspan=2, sticky='nsew')

# Créer des boutons
button1 = tk.Button(frame_btn, text="Ouvrir un fichier", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    width=25, height=1, command=open_file)
button1.grid(row=0, column=0, padx=20, pady=10)

button2 = tk.Button(frame_btn, text="Démarrer la lecture", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    width=25, height=1, command=start_reading)
button2.grid(row=1, column=0, padx=20, pady=10)

button3 = tk.Button(frame_btn, text="Pause", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    width=25, height=1, command=pause_reading)
button3.grid(row=2, column=0, padx=20, pady=10)

button3 = tk.Button(frame_btn, text="Play", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    width=25, height=1)
button3.grid(row=3, column=0, padx=20, pady=10)

button3 = tk.Button(frame_btn, text="Stop la lecture", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    width=25, height=1, command=stop_reading)
button3.grid(row=4, column=0, padx=20, pady=10)

button3 = tk.Button(frame_btn, text="Vider la case", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    width=25, height=1, command=clear_canvas)
button3.grid(row=5, column=0, padx=20, pady=10)

button4 = tk.Button(frame_btn, text="Quitter l'application", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    width=25, height=1, command=quit_app)
button4.grid(row=6, column=0, padx=20, pady=10)

frame_bas = tk.Frame(window, bg='lightblue', relief='sunken', width=1000, height=20)
frame_bas.grid(row=2, column=0, padx=0, pady=0, columnspan=2, sticky='nsew')

bas_label = tk.Label(frame_bas, text="***************************",
                     font=("Berlin sans FB", 12, "bold"), fg='blue', bg='lightblue')
bas_label.grid(row=0, column=0, columnspan=3, pady=0, padx=400)

# Créer un menu
menu = tk.Menu(window, bg="lightblue", fg="black", font=("Berlin sans FB", 14))
window.config(menu=menu)

# Ajouter des éléments au menu
file_menu = tk.Menu(menu, tearoff=0, bg="lightblue", fg="black", font=("Berlin sans FB", 14))
menu.add_cascade(label="Fichier", menu=file_menu, font=("Berlin sans FB", 14))
file_menu.add_command(label="Ouvrir PDF", command=open_file)
file_menu.add_command(label="Quitter", command=quit_app)

# Lancer la boucle principale de l'interface graphique
window.mainloop()

"""import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno
from tkinterPdfViewer import tkinterPdfViewer as pdf
import os

largeur = 1320
hauteur = 530

# Créer la fenêtre principale
window = tk.Tk()
window.title("Segmentation Image - CROISSANCE D'UNE REGION")
window.geometry("1360x680")
window.minsize(600, 350)

# Changer la couleur de fond
window.configure(bg='lightblue')


# Fonction pour quitter l'application
def quit_app():
    if askyesno('Message', 'Êtes-vous sûr de vouloir quitter le programme?'):
        window.destroy()


# Fonction pour ouvrir un fichier PDF
def open_file():
    file_path = askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        display_pdf(file_path)


# Fonction pour afficher le PDF
def display_pdf(file_path):
    v1 = pdf.ShowPdf()
    v2 = v1.pdf_view(canvas, pdf_location=file_path, width=largeur, height=hauteur)
    v2.pack(side="left", fill="both", expand=True)


frame_PL = tk.Frame(window, bg='lightblue', relief='sunken', width=1000, height=50)
frame_PL.grid(row=0, column=0, padx=0, pady=0)

frame_titre = tk.Frame(frame_PL, bg='lightblue', relief='sunken', width=50, height=50)
frame_titre.grid(row=0, column=0, padx=150, pady=0)

frame_zoom = tk.Frame(frame_PL, bg='white', relief='sunken', width=20, height=50)
frame_zoom.grid(row=0, column=1, padx=150, pady=0)

# Ajouter le grand titre
title_label = tk.Label(frame_titre, text="APPLICATION INTERACTION - Lecture PDF",
                       font=("Berlin sans FB", 18, "bold"), fg='blue', bg='lightblue')
title_label.grid(row=0, column=0, columnspan=3, pady=5, padx=10)

button_plus = tk.Button(frame_zoom, text="Plus", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                        width=10, height=1)
button_plus.grid(row=0, column=0, padx=5, pady=0)

button_moin = tk.Button(frame_zoom, text="Moin", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                        width=10, height=1)
button_moin.grid(row=0, column=1, padx=5, pady=0)

# Créer un canvas pour le PDF avec une barre de défilement
canvas = tk.Canvas(window, bg='white', width=largeur, height=hauteur)
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollbar.grid(row=1, column=1, sticky='ns')
canvas.configure(yscrollcommand=scrollbar.set)
canvas.grid(row=1, column=0, padx=20, pady=6)
canvas.grid_propagate(False)

frame_PDF = tk.Frame(canvas, bg='white', bd=2, relief='sunken', width=largeur, height=hauteur)
canvas.create_window((0, 0), window=frame_PDF, anchor='nw')
frame_PDF.grid_propagate(False)  # Empêcher le cadre de se redimensionner

frame_btn = tk.Frame(window, bg='lightblue', relief='sunken', width=1000, height=50)
frame_btn.grid(row=3, column=0, padx=0, pady=5, columnspan=2)

# Créer des boutons
button1 = tk.Button(frame_btn, text="Ouvrir un fichier", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    width=30, height=1, command=open_file)
button1.grid(row=2, column=0, padx=20, pady=3)

button2 = tk.Button(frame_btn, text="Démarrer la lecture", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    width=30, height=1)
button2.grid(row=2, column=1, padx=20, pady=3)

button3 = tk.Button(frame_btn, text="Quitter l'application", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    width=30, height=1, command=quit_app)
button3.grid(row=2, column=2, padx=20, pady=3)"""

"""import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import askyesno
import os
from tkinter import messagebox
import numpy as np
import cv2

largeur = 1320
hauteur = 530

# Créer la fenêtre principale
window = tk.Tk()
window.title("Segmentation Image - CROISSANCE D'UNE REGION")
window.geometry("1360x680")
window.minsize(600, 350)

# Changer la couleur de fond
window.configure(bg='lightblue')


# Fonction pour quitter l'application
def quit_app():
    if askyesno('Message', 'Êtes-vous sûr de vouloir quitter le programme?'):
        window.destroy()


frame_titre = tk.Frame(window, bg='lightblue', relief='sunken', width=1000, height=50)
frame_titre.grid(row=0, column=0, padx=0, pady=5)

# Ajouter le grand titre
title_label = tk.Label(frame_titre, text="APPLICATION INTERACTION - Lecture PDF",
                       font=("Berlin sans FB", 18, "bold"), fg='blue', bg='lightblue')
title_label.grid(row=0, column=0, columnspan=3, pady=5, padx=10)


# Boucle pour les frames
frame_PDF = tk.Frame(window, bg='white', bd=2, relief='sunken', width=largeur, height=hauteur)
frame_PDF.grid(row=1, column=0, padx=20, pady=6)
frame_PDF.grid_propagate(False)  # Empêcher le cadre de se redimensionner

frame_btn = tk.Frame(window, bg='lightblue', relief='sunken', width=1000, height=50)
frame_btn.grid(row=3, column=0, padx=0, pady=5)

# Créer des boutons
button1 = tk.Button(frame_btn, text="Ouvrir un fichier", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    width=30, height=1)
button1.grid(row=2, column=0, padx=20, pady=3)

button2 = tk.Button(frame_btn, text="Démarrer la lecture", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    width=30, height=1)
button2.grid(row=2, column=1, padx=20, pady=3)

button3 = tk.Button(frame_btn, text="Quitter l'application", font=("Berlin sans FB", 14), bg='#5187ec', fg="white",
                    width=30, height=1, command=quit_app)
button3.grid(row=2, column=2, padx=20, pady=3)


# Créer un menu
menu = tk.Menu(window, bg="lightblue", fg="black", font=("Berlin sans FB", 14))
window.config(menu=menu)

# Ajouter des éléments au menu
file_menu = tk.Menu(menu, tearoff=0, bg="lightblue", fg="black", font=("Berlin sans FB", 14))
menu.add_cascade(label="Fichier", menu=file_menu, font=("Berlin sans FB", 14))
file_menu.add_command(label="Ouvrir PDF")
file_menu.add_command(label="Quitter", command=quit_app)

# Lancer la boucle principale de l'interface graphique
window.mainloop()"""
