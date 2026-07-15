import tkinter as tk
from tkinter import filedialog, messagebox
from rembg import remove
from PIL import Image, ImageTk

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Suppression fond blanc")
        self.root.geometry("400x450")

        self.image_path = None
        self.image_preview = None

        # Bouton pour choisir l'image
        self.btn_choisir = tk.Button(root, text="Choisir une image", command=self.choisir_image)
        self.btn_choisir.pack(pady=10)

        # Zone d'aperçu
        self.label_apercu = tk.Label(root, text="Aucune image sélectionnée")
        self.label_apercu.pack(pady=10)

        # Bouton OK
        self.btn_ok = tk.Button(root, text="OK - Enlever le fond", command=self.traiter_image, state="disabled")
        self.btn_ok.pack(pady=10)

    def choisir_image(self):
        chemin = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")]
        )
        if chemin:
            self.image_path = chemin
            img = Image.open(chemin)
            img.thumbnail((300, 300))
            self.image_preview = ImageTk.PhotoImage(img)
            self.label_apercu.config(image=self.image_preview, text="Image sélectionnée")
            self.btn_ok.config(state="normal")

    def traiter_image(self):
        if not self.image_path:
            return
        img = remove(Image.open(self.image_path))
        data = img.getdata()

        nouvelles_donnees = []
        for pixel in data:
            if pixel[0] > 235 and pixel[1] > 235 and pixel[2] > 235:
                nouvelles_donnees.append((255, 255, 255, 0))
            else:
                nouvelles_donnees.append(pixel)

        img.putdata(nouvelles_donnees)

        chemin_sortie = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png")]
        )
        if chemin_sortie:
            img.save(chemin_sortie)
            messagebox.showinfo("Terminé", f"Image sauvegardée :\n{chemin_sortie}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()