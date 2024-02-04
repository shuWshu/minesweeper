import random

SIZE = 10
MINE = 10
board = []
edges = []

# セットアップ
def setup():
    global board, edges
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
            if board[ym][xm][1] == True:  # 既にある
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

    printboard("player")


# ゲーム部分
def mainGame():
    global board, edges
    # ゲーム部分
    countOpen = 0
    while True:
        try:
            # 命令入力[x, y, mode]
            # mode: 踏む:0(or無し), 旗:1
            inputText = input("入力(x y mode): ")
            if inputText == "cmine":
                printboard("mine")
                continue
            else:
                inputXYm = list(map(int, inputText.split()))
        except Exception as e:  # システム終了以外のエラーを取る
            print(e)
            continue

        # 入力が正しいかの判定
        if len(inputXYm) < 2 or 3 < len(inputXYm):
            print("Error: Input length is incorrect")
            continue

        xin, yin = inputXYm[0], inputXYm[1]
        if len(inputXYm) == 2 or inputXYm[2] == 1:  # 「踏む」
            if 0 <= xin < SIZE and 0 <= yin < SIZE and board[yin][xin][0] != 2:
                board[yin][xin][0] = 1
                countOpen += 1
                if board[yin][xin][1]:  # 「地雷踏んだ」
                    printboard("player")
                    print("You Lose...")
                    break
                elif board[yin][xin][2] == 0:  # マスが非地雷かつ0
                    queue = [[xin, yin]]  # 処理を行うマスを格納したキュー
                    while queue:
                        safeXY = queue.pop(0)
                        xs, ys = safeXY[0], safeXY[1]
                        # 周囲のマスを開ける
                        for edge in edges[ys][xs]:  # 移動先のマス全てについて
                            xp, yp = edge[0], edge[1]
                            if board[yp][xp][0] == 0:  # マスが初期状態
                                board[yp][xp][0] = 1
                                countOpen += 1
                                if board[yp][xp][2] == 0:  # マスの数字が0
                                    queue.append([xp, yp])
                # 勝利判定
                if countOpen == SIZE**2 - MINE:
                    printboard("player")
                    print("You Win!")
                    break
        elif inputXYm[2] == 0:  # 「初期に戻す」
            if 0 <= xin < SIZE and 0 <= yin < SIZE:
                if board[yin][xin][0] == 2:
                    board[yin][xin][0] = 0
        elif inputXYm[2] == 2:  # 「旗立て」
            if 0 <= xin < SIZE and 0 <= yin < SIZE:
                if board[yin][xin][0] == 0:
                    board[yin][xin][0] = 2
        else:
            continue

        printboard("player")


# 出力
# mode= mine: 地雷の有無
# mode= edges: 辺の数
# mode= num: 地雷の数
# mode= state: マスの状態
# mode= player: プレイヤー用
def printboard(mode="mine"):
    global SIZE, board, edges
    print("-" * (SIZE + 3))
    print("  ", end="")
    for i in range(SIZE):
        print(i, end="")
    print("")
    print("")
    for y in range(SIZE):
        print(f"{y} ", end="")
        for x in range(SIZE):
            if mode == "mine":
                if board[y][x][1] == False:
                    print("◯", end="")
                if board[y][x][1] == True:
                    print("×", end="")

            if mode == "edges":
                print(len(edges[y][x]), end="")

            if mode == "num":
                if board[y][x][1] == True:
                    print("x", end="")
                else:
                    print(board[y][x][2], end="")

            if mode == "state":
                print(board[y][x][0], end="")

            if mode == "player":
                if board[y][x][0] == 0:
                    print("■", end="")
                elif board[y][x][0] == 2:
                    print("□", end="")
                else:
                    if board[y][x][1]:
                        print("×", end="")
                    else:
                        print(board[y][x][2], end="")

        print("")
    print("-" * (SIZE + 3))


def main():
    setup()
    mainGame()


if __name__ == "__main__":
    main()
