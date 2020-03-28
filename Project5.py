
import tkinter
from othello_game import *


def update_info(game):
    white_num, black_num = game.get_score()
    info = "black:%d, white:%d, "%(black_num, white_num)
    if game.is_over():
        info += "Game over, The winner is %s"%game.get_winner()
        put_msg(info)
    else:
        info +=  "It's %s player's trun"%game.turn
    game_info_label["text"] = info



def draw_state(game):
    canvas.delete(tkinter.ALL)
    
    height = canvas.winfo_height() 
    width = canvas.winfo_width() 
    
    row_num = game.row_num
    col_num = game.col_num

    h = height / row_num
    w = width / col_num
    
    for i in range(1, row_num):
        canvas.create_line(0, i*h, width, i*h)
    for j in range(1, col_num):
        canvas.create_line(j*w, 0, j*w, height)


    for i in range(row_num):
        for j in range(col_num):
            if game.board[i][j]:
                canvas.create_oval(j*w, i*h, (j+1)*w, (i+1)*h, fill=game.board[i][j].color)

    update_info(game)
    


entry_text = ""
    
def get_input(msg=""):

    def on_ok_button():
        global entry_text
        entry_text = entry.get()
        dialog_window.destroy()
    
    dialog_window = tkinter.Toplevel()
    
    label = tkinter.Label(master=dialog_window, text=msg)
    label.grid(row = 1, column = 0, padx = 10, pady = 10)

    entry = tkinter.Entry(master = dialog_window, width = 20)
    entry.grid(row = 2, column = 0, padx = 10, pady = 1)

    ok_button = tkinter.Button(master = dialog_window, text = 'OK', command = on_ok_button)
    ok_button.grid(row = 3, column = 0, padx = 10, pady = 10)

    dialog_window.grab_set()
    dialog_window.wait_window()

    return entry_text


def put_msg(msg=""):

    def on_ok_button():
        dialog_window.destroy()
    
    dialog_window = tkinter.Toplevel()
    label = tkinter.Label(master=dialog_window, text=msg)
    label.grid(row = 1, column = 0, padx = 10, pady = 10)

    ok_button = tkinter.Button(master = dialog_window, text = 'OK', command = on_ok_button)
    ok_button.grid(row = 2, column = 0, padx = 10, pady = 10)

    dialog_window.grab_set()
    dialog_window.wait_window()




def on_start_button():
    global game

    try:
        row_num = int(get_input("Please type the number of rows on the board, which must be an even integer between 4 and 16:"))
        col_num = int(get_input("Please type the number of columns  on the board, which must be an even integer between 4 and 16:"))
        first_player = get_input("Which of the players will move first(black or white, default is black) :")
        top_left_color = get_input("Which color disc will be in the top-left position(black or white, default is white):")
        win_flag = get_input("What it means to win the game 'most' or 'fewest'(most or fewest, default is most):")

        if not first_player:
            first_player = "black"
        if not top_left_color:
            top_left_color = "white"
        if not win_flag:
            win_flag = "most"

        game = OthelloState(row_num, col_num, first_player, top_left_color, win_flag)
        
    except OthelloError as e:
        put_msg(e)
    except Exception as e:
        put_msg(e)
        
    draw_state(game)


def canvas_resized(event):
    global game
    draw_state(game)



def on_button_down(event):
   #( global game
    x = event.x
    y = event.y
    height = canvas.winfo_height() 
    width = canvas.winfo_width()
    row = int( y / (height / game.row_num))
    col = int( x / (width / game.col_num))
    try:
        game.drop_disc(row, col)
    except OthelloError as e:
        #put_msg(e)
        print(e)
    except Exception as e:
        put_msg(e)
    draw_state(game)
    
    


if __name__ == "__main__":
    game = OthelloState()
    win = tkinter.Tk()
    canvas = tkinter.Canvas(master=win, width=400, height=400, background='yellow')
    canvas.grid(row=0, column=0, padx=20, pady=20, sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
    canvas.bind('<Configure>', canvas_resized)
    win.rowconfigure(0, weight=1)
    win.columnconfigure(0, weight=1)
    canvas.bind('<Button-1>', on_button_down)
    game_info_label = tkinter.Label(master=win, text="xxxxxxxxxx")
    game_info_label.grid(row = 1, column = 0)
    start_button = tkinter.Button(master=win, text='Restart The Game', command = on_start_button)
    start_button.grid(row=2, column=0, padx=5, pady=20)
    draw_state(game)
    update_info(game)
    win.mainloop()
