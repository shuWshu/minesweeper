# マインスイーパーを作った
## 使用ツール
- python
- tkinter
## 各ファイルの説明
### Minesweeper_GUI.py
マインスイーパーで遊べる．
マスのサイズや地雷の数はboxに入力して変更する．
左クリックでマスを開く，シフトクリックor右クリックで旗を立てる．
コア部分の実装を有向グラフで行ったため，マス同士の接続を色々弄れるようになっている，今後何か追加してみたい．
### Minesweeper.py
↑をコンソール上で遊べる