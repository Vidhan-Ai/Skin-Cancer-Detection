from flask import Flask, request, render_template
from PIL import Image
import numpy as np
import skin_cancer_detection as SCD
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def runhome():
    return render_template("home.html")

@app.route("/showresult", methods=["GET", "POST"])
def show():
    if "pic" not in request.files or request.files["pic"].filename == "":
        return render_template("home.html", error="No file uploaded or invalid file.")
    try:
        pic = request.files["pic"]
        inputimg = Image.open(pic).convert("RGB")
        inputimg = inputimg.resize((28, 28))
        img = np.array(inputimg).reshape(-1, 28, 28, 3)

        result = SCD.model.predict(img)
        result = result.tolist()
        max_prob = max(result[0])
        class_ind = result[0].index(max_prob)
        logging.info(f"Prediction: {SCD.classes[class_ind]} with probability {max_prob:.2f}")
        class_info = {
            0: ("Actinic Keratosis", "Actinic keratosis also known as solar keratosis or senile keratosis are names given to intraepithelial keratinocyte dysplasia. As such they are a pre-malignant lesion or in situ squamous cell carcinomas and thus a malignant lesion."),
            1: ("Basal Cell Carcinoma", "Basal cell carcinoma is a type of skin cancer. Basal cell carcinoma begins in the basal cells — a type of cell within the skin that produces new skin cells as old ones die off.Basal cell carcinoma often appears as a slightly transparent bump on the skin, though it can take other forms. Basal cell carcinoma occurs most often on areas of the skin that are exposed to the sun, such as your head and neck"),
            2: ("Benign Lichenoid Keratosis", "Benign lichenoid keratosis (BLK) usually presents as a solitary lesion that occurs predominantly on the trunk and upper extremities in middle-aged women. The pathogenesis of BLK is unclear; however, it has been suggested that BLK may be associated with the inflammatory stage of regressing solar lentigo (SL)1"),
            3: ("Dermatofibroma", "Dermatofibromas are small, noncancerous (benign) skin growths that can develop anywhere on the body but most often appear on the lower legs, upper arms or upper back. These nodules are common in adults but are rare in children. They can be pink, gray, red or brown in color and may change color over the years."),
            4: ("Melanocytic Nevus", "A melanocytic nevus (also known as nevocytic nevus, nevus-cell nevus and commonly as a mole) is a type of melanocytic tumor that contains nevus cells. Some sources equate the term mole with ‘melanocytic nevus’, but there are also sources that equate the term mole with any nevus form."),
            5: ("Pyogenic Granuloma", "Pyogenic granulomas are skin growths that are small, round, and usually bloody red in color. They tend to bleed because they contain a large number of blood vessels. They’re also known as lobular capillary hemangioma or granuloma telangiectaticum."),
            6: ("Melanoma", "Melanoma, the most serious type of skin cancer, develops in the cells (melanocytes) that produce melanin — the pigment that gives your skin its color. Melanoma can also form in your eyes and, rarely, inside your body, such as in your nose or throat. The exact cause of all melanomas isn't clear, but exposure to ultraviolet (UV) radiation from sunlight or tanning lamps and beds increases your risk of developing melanoma."),
        }

        class_label, info = class_info.get(class_ind, ("Unknown", "Information not available."))


        return render_template("results.html", result=class_label, info=info)

    except Exception as e:
        logging.error(f"Error in prediction: {str(e)}")
        return render_template("home.html", error="Error processing image.")

@app.route("/terms")
def terms():
    return render_template("terms.html")

if __name__ == "__main__":
    app.run()
