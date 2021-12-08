#!/Users/zhouweijie/miniconda3/bin python
# -*- code: utf-8 -*-

import cv2
import socket

IP = "127.0.0.1"
PORT = 9999


def TcpClient(DATA):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((IP, PORT))  # 建立一个链接
    except ConnectionRefusedError:
        print("服务器无法连接，请确保服务器端已打开。")
        exit(0)
    if True:
        try:
            client.sendall(DATA.encode("utf-8"))
            print(DATA, "已发送")
            #data = client.recv(1024)  # 接收一个信息，并指定接收的大小 为1024字节
            #print("接收到:", data)
            #time.sleep(DELAY)
        except ConnectionAbortedError:
            print("服务器无法连接，请确保服务器端已打开。")
            exit(0)
        except KeyboardInterrupt:
            client.close()
            print("Tcp 客户端已关闭")
            exit(0)

def averageX(points):
    points_x = [point[0] for point in points]
    points_x.sort()
    # 抛弃的点数
    points_x = points_x[50:-50]
    return sum(points_x) / len(points_x)

def cutImage(img, up, down, left, right):
    return img[up:-down, left:-right]

def detect(tem_img, init_img):
    init_img = cutImage(init_img, 10, 10, 10, 10)
    cv2.GaussianBlur(init_img, (3, 3), 0)
    result = cv2.matchTemplate(init_img, tem_img, cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    height, width = tem_img.shape[:2]
    result_img = init_img[min_loc[1]:(min_loc[1] + height), min_loc[0]:(min_loc[0] + width)]
    cv2.imshow("a", result_img)
    # 螺栓螺母裁剪
    bolt_img = result_img[:150]
    nut_img = result_img[150:]
    # 螺栓螺母阈值
    bolt_img = cv2.inRange(bolt_img, (10, 10, 30), (200, 200, 250))
    nut_img = cv2.inRange(nut_img, (10, 10, 30), (200, 200, 250))
    cv2.dilate(bolt_img, (5, 5))
    cv2.dilate(nut_img, (5, 5))
    bolt_points = [(x, y) for x in range(bolt_img.shape[0]) for y in range(bolt_img.shape[1]) if bolt_img[x][y]==255]
    nut_points = [(x, y) for x in range(nut_img.shape[0]) for y in range(nut_img.shape[1]) if nut_img[x][y] == 255]
    bolt_x = averageX(bolt_points)
    nut_x = averageX(nut_points)
    return bolt_x, nut_x

if __name__ == "__main__":
    tem_img = cv2.imread("/Users/zhouweijie/Desktop/截屏2021-11-29 下午2.36.07.png")
    init_img = cv2.imread("/Users/zhouweijie/Desktop/截屏2021-11-29 上午11.31.17.png")
    cap = cv2.VideoCapture(0)
    while True:
        for i in range(10):
            ret, frame = cap.read()
            cv2.imshow("init", frame)
            try:
                bolt_x, nut_x = detect(tem_img, frame)
                delta = bolt_x - nut_x
                DATA = "{}is{}".format(i, delta)
                print(DATA)
                TcpClient(DATA)
            except:
                print("broke")
                continue
        cv2.waitKey(1)
    cap.release()
    cv2.destroyAllWindows()