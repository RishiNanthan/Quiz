import cv2
from box import Box
import PySimpleGUI as pg

boxes = []
previous_box = None
pg.theme("DarkAmber")
questions = []


def get_questions():
    global questions
    questions = []
    with open("questions.txt", "r") as f:
        questions = f.readlines()


get_questions()


def create_layout(ques_no, ques, choice=None):
    if choice is None:
        return [
            [pg.Text(" ", size=(50, 2))],
            [pg.Text(" " * 20 + f"Question {ques_no+1}/28", font=("Helvetica", 15))],
            [pg.Text(" ", size=(50, 2))],
            [pg.Text(ques, font=("Helvetica", 18))],
            [pg.Text(" ", size=(50, 2))],
            [pg.Text(" ", size=(50, 2))],
            [pg.Text(" ", size=(40, 1)), pg.Ok("  OK  ")]
        ]
    else:
        lay = [
            [pg.Text(" " * 15 + f"Question {ques_no+1}/28")],
            [pg.Text(" ", size=(50, 1))],
            [pg.Text(ques)],
        ]
        for i in choice:
            lay += [[pg.Radio(i, 1)]]
        lay += [[pg.Ok("OK")]]
        return lay


def on_mouse_click(event, x, y, flags, param):
    global previous_box
    if event == cv2.EVENT_LBUTTONUP:
        for i, box in enumerate(boxes):
            if box.x < x < box.x1 and box.y < y < box.y1 and not box.clicked:
                box.clicked = True
                win = pg.Window("Quiz", alpha_channel=0.95, no_titlebar=True)
                win.Layout(create_layout(i, questions[i]))
                b, val = win.Read()
                win.close()
                param[box.y:box.y1, box.x:box.x1, :] = box.org


def main():
    global boxes
    img = cv2.imread('sample.png')
    img = cv2.resize(img, (1920, 1080))
    img = cv2.resize(img, (img.shape[1]//2, img.shape[0]//2))
    w, h = img.shape[0]//7, img.shape[1]//4
    qn = 1
    for i in range(4):
        for j in range(7):
            x, y, x1, y1 = h*i, w*j, h*(i+1), w*(j+1)
            b = Box((x, y), (x1, y1))
            b.set_original(img[y:y1, x:x1, :])
            boxes += [b]
            img = cv2.rectangle(img, (x, y), (x1, y1), (255, 255, 255), 2)
            img[y:y1, x:x1, :] = (0, 0, 0)
            img = cv2.putText(img, f"Q{qn}", ((x+x1-40)//2, (y+y1+20)//2), cv2.QT_FONT_NORMAL, 1, (200, 200, 250), 1)
            qn += 1

    while True:
        cv2.namedWindow("img", cv2.WINDOW_NORMAL)
        cv2.imshow('img', img)
        cv2.setWindowProperty("img", cv2.WND_PROP_ASPECT_RATIO, cv2.WINDOW_NORMAL)
        cv2.setMouseCallback('img', on_mouse_click, param=img)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
