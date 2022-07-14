import tkinter as tk
import random
import tkinter.font as font
class App(tk.Frame):
    def __init__(self,length,master=None):
        super().__init__(master)
        self.length = length
        master.title('パズル')
        master.geometry('600x400')
        self.master = master
        self.pack(anchor=tk.W)
        self.xIsNext = True
        self.board = Board(4)
        self.emptylabel = tk.Label()
        self.squares = []
        self.create_squares()
        self.placement_number()
        self.create_reset_button()

    def create_squares(self):
        labelFont = font.Font(size=30, weight='bold')
        for i in range(0,self.length):
            squares = []
            for j in range(0, self.length):
                square = tk.Label(self, text='', bg='white', bd=2,
                                font=labelFont, relief='groove', width=5, height=2)
                square.grid(column=j, row=i)
                square.place = (i,j)
                square.bind("<1>", self.left_click_v1)
                squares.append(square)
            self.squares.append(squares)
    def create_reset_button(self):
        button = tk.Button(self,textvariable='RESET',command=self.reset)
        button.pack(side = tk.LEFT)
    def placement_number(self):
        for i in range(0,self.length):
            for j in range(0, self.length):
                num = self.board[i,j]
                if num != 0:
                    self.squares[i][j]['text'] = str(num)
                else:
                    self.emptylabel = self.squares[i][j]
    def left_click_v1(self,event):
        label = event.widget
        if self.board.canselectplace_v1(label.place):
            self.board.select(label.place)
            self.emptylabel['text'] = label['text']
            label['text'] = ''
            self.emptylabel = label
        if self.board.getclear():
            for i in range(self.length):
                for j in range(self.length):
                    self.squares[i][j]['state'] = "disable"
    def left_click_v2(self,event):
        pass
    
    def reset(self):
        self.placement_number()
        for i in range(self.length):
            for j in range(self.length):
                self.squares[i][j]['state'] = "normal"



class Board:
    def __init__(self,length) -> None:
        self.length = length
        self.max_num = self.length**2 - 1
        self.canselect = []
        self.empty = ()
        self.init_placement()
        self.clear = False
        self.answer = []
        for i in range(self.length):
            answer = []
            for j in range(1,self.length+1):
                if j + self.length*i == self.length**2:
                    answer.append(0)
                else:
                    answer.append(j + self.length*i)
            self.answer.append(answer)
    def __getitem__(self,item):
        return self.board[item[0]][item[1]]
    # 生成
    def init_placement(self):
        self.clear = False
        self.board = [[0]*self.length]*self.length
        
        sample = random.sample(range(0,self.length**2),k=self.length**2)
        for i in range(self.length):
            startidx = i*self.length
            row = sample[startidx:startidx+self.length]
            self.board[i] = row
            if 0 in row:
                self.empty = (i,row.index(0))
    
    def canselectplace_v1(self,place):
        canselect = []
        # 上方向 条件:0行目じゃなければ動かせる
        if self.empty[0] != 0:
            canselect.append((self.empty[0]-1,self.empty[1]))
        # 下方向 条件:最下段じゃなければ動かせる
        if self.empty[0] != self.length-1:
            canselect.append((self.empty[0]+1,self.empty[1]))
        # 右方向 条件:一番右じゃなければ動かせる
        if self.empty[1] != 0:
            canselect.append((self.empty[0],self.empty[1]-1))
        # 左方向 条件:一番左じゃなければ動かせる
        if self.empty[1] != self.length-1:
            canselect.append((self.empty[0],self.empty[1]+1))
        return place in canselect

    def selectplace_v2(self,place):
        return self.empty[0] == place[0] or self.empty[1] == place[1]

    def getcanselect(self):
        return self.canselect
    def select(self,place):
        if self.canselectplace_v1(place):
            # 数字交換
            value = self.board[place[0]][place[1]]
            self.board[place[0]][place[1]] = 0
            self.board[self.empty[0]][self.empty[1]] = value

            # 空白場所交換
            self.empty = place

            # 選択できる場所変更
            if self.board == self.answer:
                self.clear = True
    def getclear(self):
        return self.clear

    def debuglog(self):
        print("board")
        print(self.board)
        print("empty")
        print(self.empty)

if __name__ == '__main__':
    root = tk.Tk()
    App(4,master=root)
    root.mainloop()