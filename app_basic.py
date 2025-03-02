import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import skin_cancer_detection as SCD
import logging
import cv2

logging.basicConfig(level=logging.INFO)

class_info = {
    0: ("Actinic Keratosis", "Actinic keratosis also known as solar keratosis or senile keratosis are names given to intraepithelial keratinocyte dysplasia. As such they are a pre-malignant lesion or in situ squamous cell carcinomas and thus a malignant lesion."),
    1: ("Basal Cell Carcinoma", "Basal cell carcinoma is a type of skin cancer. Basal cell carcinoma begins in the basal cells — a type of cell within the skin that produces new skin cells as old ones die off.Basal cell carcinoma often appears as a slightly transparent bump on the skin, though it can take other forms. Basal cell carcinoma occurs most often on areas of the skin that are exposed to the sun, such as your head and neck"),
    2: ("Benign Lichenoid Keratosis", "Benign lichenoid keratosis (BLK) usually presents as a solitary lesion that occurs predominantly on the trunk and upper extremities in middle-aged women. The pathogenesis of BLK is unclear; however, it has been suggested that BLK may be associated with the inflammatory stage of regressing solar lentigo (SL)1"),
    3: ("Dermatofibroma", "Dermatofibromas are small, noncancerous (benign) skin growths that can develop anywhere on the body but most often appear on the lower legs, upper arms or upper back. These nodules are common in adults but are rare in children. They can be pink, gray, red or brown in color and may change color over the years. They are firm and often feel like a stone under the skin. "),
    4: ("Melanocytic Nevus", "A melanocytic nevus (also known as nevocytic nevus, nevus-cell nevus and commonly as a mole) is a type of melanocytic tumor that contains nevus cells. Some sources equate the term mole with ‘melanocytic nevus’, but there are also sources that equate the term mole with any nevus form."),
    5: ("Pyogenic Granuloma", "Pyogenic granulomas are skin growths that are small, round, and usually bloody red in color. They tend to bleed because they contain a large number of blood vessels. They’re also known as lobular capillary hemangioma or granuloma telangiectaticum."),
    6: ("Melanoma", "Melanoma, the most serious type of skin cancer, develops in the cells (melanocytes) that produce melanin — the pigment that gives your skin its color. Melanoma can also form in your eyes and, rarely, inside your body, such as in your nose or throat. The exact cause of all melanomas isn't clear, but exposure to ultraviolet (UV) radiation from sunlight or tanning lamps and beds increases your risk of developing melanoma."),
}


def upload_image():
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not filepath:
        return

    try:
        inputimg = Image.open(filepath).convert("RGB")
        inputimg = inputimg.resize((28, 28))
        img = np.array(inputimg).reshape(-1, 28, 28, 3)

        result = SCD.model.predict(img)
        result = result.tolist()
        max_prob = max(result[0])
        class_ind = result[0].index(max_prob)
        logging.info(f"Prediction: {SCD.classes[class_ind]} with probability {max_prob:.2f}")

        class_label, info = class_info.get(class_ind, ("Unknown", "Information not available."))

        show_results(class_label, info)

    except Exception as e:
        logging.error(f"Error in prediction: {str(e)}")
        messagebox.showerror("Error", "Error processing the image.")

def capture_image():
    """Open the webcam, capture an image, and process it."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Error", "Could not access the webcam.")
        return

    messagebox.showinfo("Webcam", "Press SPACEBAR to capture an image.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture image.")
            cap.release()
            return

        cv2.imshow("Capture Image - Press SPACEBAR to Save", frame)
        key = cv2.waitKey(1)

        if key == 32:  # Spacebar to capture
            cv2.imwrite("captured_image.jpg", frame)
            cap.release()
            cv2.destroyAllWindows()
            try:
                inputimg = Image.open("captured_image.jpg").convert("RGB")
                inputimg = inputimg.resize((28, 28))
                img = np.array(inputimg).reshape(-1, 28, 28, 3)

                result = SCD.model.predict(img)
                result = result.tolist()
                max_prob = max(result[0])
                class_ind = result[0].index(max_prob)
                logging.info(f"Prediction: {SCD.classes[class_ind]} with probability {max_prob:.2f}")

                class_label, info = class_info.get(class_ind, ("Unknown", "Information not available."))

                show_results(class_label, info)

            except Exception as e:
                logging.error(f"Error in prediction: {str(e)}")
                messagebox.showerror("Error", "Error processing the image.")
            break



def show_results(class_label, info):
    for widget in root.winfo_children():
        widget.pack_forget()

    result_label = tk.Label(root, text=f"Prediction", font=("Montserrat", 18, "bold"), fg="white", justify="center", bg="#202020")
    result_label.pack(pady=60)

    result_label = tk.Label(root, text=f"{class_label}", font=("Montserrat", 24, "bold"), fg="white", wraplength=900, justify="center", bg="#202020")
    result_label.pack(pady=0)
    
    info_label = tk.Label(root, text=f"Details",fg="white", font=("Montserrat", 18, "bold"), justify="center", bg="#202020")
    info_label.pack(pady=60)

    result_label = tk.Label(root, text=f"{info}", font=("Montserrat", 18, "bold"), fg="white", wraplength=900, justify="center", bg="#202020")
    result_label.pack(pady=0)

    back_button = tk.Button(root, text="Back", font=("Montserrat", 10), command=show_upload_page, width=20, height=2)
    back_button.pack(pady=60)

def show_upload_page():
    for widget in root.winfo_children():
        widget.pack_forget()

    head_label = tk.Label(root,text=" Skin Cancer Detection ", font=("Montserrat", 58, "bold"),fg="white", bg="#202020")
    head_label.pack(pady=150)

    upload_button = tk.Button(root, text="Upload Image", font=("Montserrat", 10), command=upload_image, width=20, height=2)
    upload_button.pack(pady=50)

    tk.Button(root, text="Capture from Camera", font=("Montserrat", 12), command=capture_image, width=25, height=2).pack(pady=20)

root = tk.Tk()
root.title("Skin Cancer Detection")
root.geometry("1000x800")
root.resizable(0,0)

background_image = Image.open("static/bg.png").resize((1200, 800))
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

show_upload_page()

root.mainloop()
