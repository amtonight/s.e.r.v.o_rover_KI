import cv2
import numpy as np

def predict_digit(img, model):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, th = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return None, 0.0, img

    c = max(cnts, key=cv2.contourArea)
    if cv2.contourArea(c) < 1000:
        return None, 0.0, img

    x, y, w, h = cv2.boundingRect(c)
    roi = th[y:y+h, x:x+w]
    roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
    roi = roi.astype("float32") / 255.0
    roi = roi.reshape(1, 28, 28, 1)

    probs = model.predict(roi, verbose=0)[0]
    idx = int(np.argmax(probs))
    prob = probs[idx]
    digit = idx + 1

    # Annotiere das Originalbild
    img_annotated = img.copy()
    cv2.rectangle(img_annotated, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(img_annotated, f"{digit}:{prob:.2f}", (x, y-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return digit, prob, img_annotated