import tkinter as tk
import random

SIZE = 10  # マスの数
MINE = 10  # 地雷の数
board = []  # マスの状態を格納
edges = []  # エッジデータを格納
countOpen = 0  # 開けたマス数 セットアップの判定にも利用する
active = True  # 画面操作可能か否か


def reset():  # 画面のリサイズとマスの再配置
    global SIZE, MINE, countOpen, active
    print("reset")

    SIZE = size.get()
    MINE = mine.get()

    # 地雷が多すぎる場合処理できない
    if MINE > SIZE**2:
        print("can't setup")
        return False

    windowSize = SIZE * 30 + 50
    root.geometry(f"{windowSize}x{windowSize}")
    canv.config(width=windowSize - 30, height=windowSize - 30)
    canv.delete("all")
    setTrout(SIZE)
    countOpen = 0
    active = True


# シフトクリックで分岐
def mousePressed(event):
    if event.state & 0x1:  # Shiftキーが押されているかどうかをチェック
        mousePressedRight(event)
    else:
        mousePressedLeft(event)


# 左クリックした時の処理
def mousePressedLeft(event):
    if not active:
        return
    obj = canv.find_overlapping(
        event.x, event.y, event.x, event.y
    )  # イベントが起きた位置にあるオブジェクトを得る
    if obj and "initial" in canv.gettags(obj[0]):  # マスが初期状態
        tagl = canv.gettags(obj[0])  # タグリスト
        delx, dely = tagl[0].split(",")  # 削除するマスの座標取得
        print(f"({delx}, {dely}) is deleted")
        if countOpen == 0:
            setup(int(delx), int(dely))
        chooseTrout(int(delx), int(dely), obj[0])
        # canv.delete(obj[0]) # マスの削除


# マスを選択した際の処理
def chooseTrout(x, y, obj):
    global countOpen
    board[y][x][0] = 1
    openTrout(x, y, obj)
    countOpen += 1
    if board[y][x][1]:  # 「地雷踏んだ」
        print("You Lose...")
        lose()
        return -1
    elif board[y][x][2] == 0:  # マスが非地雷かつ0
        queue = [[x, y]]  # 処理を行うマスを格納したキュー
        while queue:
            safeXY = queue.pop(0)
            xs, ys = safeXY[0], safeXY[1]
            # 周囲のマスを開ける
            for edge in edges[ys][xs]:  # 移動先のマス全てについて
                xp, yp = edge[0], edge[1]
                if board[yp][xp][0] == 0:  # マスが初期状態
                    board[yp][xp][0] = 1
                    countOpen += 1
                    objPs = canv.find_withtag(f"{xp},{yp}")
                    for p in objPs:
                        if "trout" in canv.gettags(p):
                            openTrout(xp, yp, p)
                    if board[yp][xp][2] == 0:  # マスの数字が0
                        queue.append([xp, yp])
    print(countOpen)
    if countOpen == SIZE**2 - MINE:
        print("You win!!")
        win()


# マスを開ける際の描画処理
def openTrout(x, y, obj):
    canv.itemconfig(obj, fill="white")  # 色の変更
    canv.dtag(obj, "initial")  # タグ削除
    canv.addtag_withtag("removed", obj)  # タグ追加

    # 数字の表示 2桁もいける
    # TODO:枠を触った時バグる
    objCs = canv.coords(obj)  # 座標の取得
    canv.create_text(
        (objCs[0] + objCs[2]) / 2,
        (objCs[1] + objCs[3]) / 2,
        text=board[y][x][2],
        font=("Helvetica", 24),
        fill="black",
        tags="number",
    )


# 右クリック時
def mousePressedRight(event):
    if not active:
        return
    if countOpen == 0:
        return
    obj = canv.find_overlapping(
        event.x, event.y, event.x, event.y
    )  # イベントが起きた位置にあるオブジェクトを得る
    if obj and "initial" in canv.gettags(obj[0]):  # マスが初期状態
        tagl = canv.gettags(obj[0])  # タグリスト
        delx, dely = tagl[0].split(",")  # マスの座標取得
        print(f"({delx}, {dely}) is planted flag")
        canv.dtag(obj[0], "initial")  # タグ削除
        canv.addtag_withtag("flagging", obj[0])  # タグ追加

        # 旗の表示
        objCs = canv.coords(obj)  # 座標の取得
        canv.create_text(
            (objCs[0] + objCs[2]) / 2,
            (objCs[1] + objCs[3]) / 2,
            text="F",
            font=("Helvetica", 24),
            fill="red",
            tags=(f"{delx},{dely}", "flag"),  # 旗座標,
        )
    elif obj and "flagging" in canv.gettags(obj[0]):  # マスが旗あり
        tagl = canv.gettags(obj[0])  # タグリスト
        delx, dely = tagl[0].split(",")  # マスの座標取得
        print(f"({delx}, {dely}) is deleted flag")
        canv.dtag(obj[0], "flagging")  # タグ削除
        canv.addtag_withtag("initial", obj[0])  # タグ追加

        objPs = canv.find_withtag(f"{delx},{dely}")
        for p in objPs:
            if "flag" in canv.gettags(p):
                canv.delete(p)


# マウスオーバー処理
def mouseMove(event):
    if not active:
        return
    if countOpen == 0:
        return
    # 全マスを初期の色に
    # 初期状態
    objs = canv.find_withtag("trout")
    for obj in objs:
        canv.itemconfig(obj, outline="black", width=1)

    objEnters = canv.find_overlapping(
        event.x, event.y, event.x, event.y
    )  # イベントが起きた位置にあるオブジェクトを得る
    if objEnters:
        for objEnter in objEnters:
            if not "trout" in canv.gettags(objEnter):  # マス以外のオブジェクトを無視
                continue

            # 指定マスの変化
            canv.itemconfig(objEnter, outline="yellow", width=2)

            # 周囲のマスへの指示
            tagl = canv.gettags(objEnter)
            if tagl:
                delx, dely = tagl[0].split(",")  # マスの座標取得
                connecting = edges[int(dely)][int(delx)]  # 接続先マスリスト
                for c in connecting:
                    connectTag = f"{c[0]},{c[1]}"
                    connect = canv.find_withtag(connectTag)  # 接続先マスを検索
                    if connect:
                        canv.itemconfig(connect[0], outline="red", width=2)
                        canv.tag_raise(connect[0])  # マスを前面へ

            canv.tag_raise(objEnter)  # 選択マスを前面へ
            # 全ての数字と旗を前面に
            nums = canv.find_withtag("number")
            for n in nums:
                canv.tag_raise(n)
            nums = canv.find_withtag("flag")
            for n in nums:
                canv.tag_raise(n)


# マスの設置
def setTrout(s):
    offsetx, offsety = 10, 10
    for y in range(s):  # 四角形の配置
        for x in range(s):
            canv.create_rectangle(
                offsetx + x * 30,
                offsety + y * 30,
                offsetx + (x + 1) * 30,
                offsety + (y + 1) * 30,
                fill="light gray",
                tags=(
                    f"{x},{y}",
                    "trout",
                    "initial",
                ),  # 座標, trout:マス, (initial:初期状態 removed:選択済 flagging:旗)
            )


# セットアップ
# 押した場所以外に地雷を設置するように
def setup(xin, yin):
    global board, edges, countOpen
    # マスの情報[y][x][操作状態, 地雷, 数字]
    # 操作状態: 初期:0, 踏んだ:1, 旗立て:2
    # 地雷: あり:true, なし:false
    # 数字: 周囲の地雷の数:int

    board = [[[0, False, 0] for _ in range(SIZE)] for _ in range(SIZE)]

    # 辺の情報[y][x][接続先リスト(x, y)]
    # 初期は空配列
    edges = [[[] for _ in range(SIZE)] for _ in range(SIZE)]
    for y in range(SIZE):
        for x in range(SIZE):
            for y1 in range(3):
                for x1 in range(3):
                    if x1 == 1 and y1 == 1:
                        continue
                    if 0 <= x + x1 - 1 < SIZE and 0 <= y + y1 - 1 < SIZE:
                        edges[y][x].append([x + x1 - 1, y + y1 - 1])

    # 地雷の設置
    mines = [[random.randrange(SIZE), random.randrange(SIZE)] for _ in range(MINE)]
    for mine in mines:
        xm, ym = mine[0], mine[1]
        while True:
            if (xin == xm and yin == ym) or board[ym][xm][
                1
            ]:  # ますが被った or 押したマスだった場合
                xm, ym = random.randrange(SIZE), random.randrange(SIZE)

            else:
                board[ym][xm][1] = True
                mine[0], mine[1] = xm, ym
                break

    # 各マスの数字を計算
    for y in range(SIZE):
        for x in range(SIZE):
            for p in edges[y][x]:
                if board[p[1]][p[0]][1]:  # 「接続先に地雷がある」
                    board[y][x][2] += 1

    return True


def win():
    global active

    canv.create_text(
        SIZE * 15 + 10,
        SIZE * 15 + 10,
        text="You Win!!",
        font=("Helvetica", 64),
        fill="red",
    )
    active = False


def lose():
    global active

    canv.create_text(
        SIZE * 15 + 10,
        SIZE * 15 + 10,
        text="You Lose...",
        font=("Helvetica", 64),
        fill="red",
    )
    active = False


# メイン処理
root = tk.Tk()
root.title("tk inter canvas")
root.geometry("350x350")

frm = tk.Frame(root)
frm.pack()

# メニューの作成
size = tk.IntVar()
mine = tk.IntVar()
size.set(10)
mine.set(10)
sizetext = tk.Label(frm, text="size:")
sizein = tk.Entry(frm, width=3, textvariable=size)
minetext = tk.Label(frm, text="mines:")
minein = tk.Entry(frm, width=3, textvariable=mine)
button = tk.Button(frm, text="reset", command=reset)
sizetext.pack(side=tk.LEFT)
sizein.pack(side=tk.LEFT)
minetext.pack(side=tk.LEFT)
minein.pack(side=tk.LEFT)
button.pack(side=tk.LEFT)

canv = tk.Canvas(root, bg="white", width=320, height=320)
canv.pack()

setTrout(SIZE)

canv.bind("<Motion>", lambda ev: mouseMove(ev))
canv.bind(
    "<Button-1>", lambda ev: mousePressed(ev)
)  # 左クリック押下イベント発生時のコールバック設定
canv.bind("<Button-2>", lambda ev: mousePressedRight(ev))  # 右クリックでのコールバック
root.mainloop()
