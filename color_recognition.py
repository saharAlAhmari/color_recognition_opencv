import cv2
import pandas as pd

csv = pd.read_csv("colors.csv", names=["color", "color_name", "hex", "R", "G", "B"], header=None)
cap = cv2.VideoCapture(0)

clicked = False
r = g = b = xpos = ypos = 0

def get_color_name(R, G, B):
    minimum = 10000
    cname = "Unknown"
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = frame[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow("Color Recognition")
cv2.setMouseCallback("Color Recognition", draw_function)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if clicked:
        cv2.rectangle(frame, (20, 20), (600, 60), (b, g, r), -1)
        text = get_color_name(r, g, b) + f" R={r} G={g} B={b}"
        cv2.putText(frame, text, (30, 50), 2, 0.8, (255, 255, 255), 2)
    
    cv2.imshow("Color Recognition", frame)

    if cv2.waitKey(20) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
