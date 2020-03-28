
def change_color(color):
    if color == "white":
        return "black"
    elif color == "black":
        return "white"

    
class OthelloError(Exception):
    pass


class Disc():
    
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def turn_color(self):
        self.color = change_color(self.color)



class OthelloState():
    
    def __init__(self, row_num=8, col_num=8, first_player="black", top_left_color="white", win_flag="most"):
        
        if row_num < 4 or row_num > 16 or row_num % 2 == 1:
            raise OthelloError("The number of rows on the board, which must be an even integer between 4 and 16")
        
        if col_num < 4 or col_num > 16 or col_num % 2 == 1:
            raise OthelloError("The number of columns  on the board, which must be an even integer between 4 and 16")
            

        if first_player not in ["black", "white"]:
            raise OthelloError("The first player's should be black or white")
        
        if top_left_color not in ["black", "white"]:
            raise OthelloError("The top left color should be black or white")
        
        if win_flag not in ["most", "fewest"]:
            raise OthelloError("The win flag should be most or fewest")

        self.row_num = row_num
        self.col_num = col_num
        self.board = [[None for i in range(col_num)] for j in range(row_num)]

        self.turn = first_player

        self.board[int(row_num/2)-1][int(col_num/2)-1] = Disc(top_left_color)
        self.board[int(row_num/2)][int(col_num/2)] = Disc(top_left_color)
        self.board[int(row_num/2)-1][int(col_num/2)] = Disc(change_color(top_left_color))
        self.board[int(row_num/2)][int(col_num/2)-1] = Disc(change_color(top_left_color))
        
        self.win_flag = win_flag


    def drop_disc(self, row, col):
        if row < 0 or row >= self.row_num or col < 0 or col >= self.col_num:
            raise OthelloError("There is not this place on the board")

        if self.board[row][col]:
            raise OthelloError("This place already exist disc")
        
        disc = Disc(self.turn)

        turn_list = self.check_disc(row, col, disc.color)
        if not turn_list:
            raise OthelloError("Can't drop here")
        
        for i, j in turn_list:
            self.board[i][j].turn_color()
            
            
        self.board[row][col] = disc

        self.turn_player()

    


    def check_disc(self, row, col, color):
        row_num = self.row_num
        col_num = self.col_num

        self.turn_list = []


        self.temp_list = []
        for i in range(row+1, self.row_num):
            j = col
            if not self._check_handle(i, j, color):
                break
            
        
        self.temp_list = []
        for i in range(row-1, -1, -1):
            j = col
            if not self._check_handle(i, j, color):
                break
            

        self.temp_list = []
        for j in range(col+1, self.col_num):
            i = row
            if not self._check_handle(i, j, color):
                break

        
    
        self.temp_list = []
        for j in range(col-1, -1, -1):
            i = row
            if not self._check_handle(i, j, color):
                break


        self.temp_list = []
        for n in range(1, row_num + col_num):
            i = row + n
            j = col + n
            if i >= row_num or j >= col_num:
                break
            if not self._check_handle(i, j, color):
                break
            
            
        self.temp_list = []
        for n in range(1, row_num + col_num):
            i = row - n
            j = col - n
            if i < 0 or j < 0:
                break
            if not self._check_handle(i, j, color):
                break


        self.temp_list = []
        for n in range(1, row_num + col_num):
            i = row + n
            j = col - n
            if i >= row_num or j < 0:
                break
            if not self._check_handle(i, j, color):
                break


        self.temp_list = []
        for n in range(1, row_num + col_num):
            i = row - n
            j = col + n
            if i < 0 or j >= col_num:
                break
            if not self._check_handle(i, j, color):
                break



        return self.turn_list


    def _check_handle(self, i, j, color):
        disc_current = self.board[i][j]
        if not disc_current:
            return False
        elif disc_current.color == color:
            self.turn_list += self.temp_list
            return False
        elif disc_current.color != color:
            self.temp_list.append([i,j])
            return True
        return False


    def turn_player(self):
        for i in range(self.row_num):
            for j in range(self.col_num):
                if not self.board[i][j]:
                    if self.check_disc(i, j, change_color(self.turn)):
                        self.turn = change_color(self.turn)
                        return
        print("%s disc is not place to drop"%change_color(self.turn))



    def is_over(self):
        for i in range(self.row_num):
            for j in range(self.col_num):
                if not self.board[i][j]:
                    if self.check_disc(i, j, "white") or self.check_disc(i, j, "black"):
                        return False
        return True

    
    def get_score(self):
        white_num = 0
        black_num = 0
        for i in range(self.row_num):
            for j in range(self.col_num):
                if self.board[i][j]:
                    if self.board[i][j].color == "white":
                        white_num += 1
                    elif self.board[i][j].color == "black":
                        black_num += 1
        return white_num, black_num


    def get_winner(self):
        if not self.is_over():
            raise OthelloError("The game has not over")

        white_num, black_num = self.get_score()

        if self.win_flag == "fewest":
            white_num = 0 - white_num
            black_num = 0 - black_num
        
        if white_num == black_num:
            return "draw"
        elif white_num > black_num:
            return "white"
        elif white_num < black_num:
            return "black"


    def print_state(self):
        white_num, black_num = self.get_score()

        print("black:%d, white:%d"%(black_num, white_num))
        print(" ", end=" ")
        for c in range(self.col_num):
            print(c, end=" ")
            
        for i in range(self.row_num):
            print()
            print(i, end=" ")
            for j in range(self.col_num):
                if not self.board[i][j]:
                    print(" ", end=" ")
                elif self.board[i][j].color == "black":
                    print("●", end=" ")
                elif self.board[i][j].color == "white":
                    print("○", end=" ")           
        print()
        print("It's %s player's trun"%self.turn)


def test():
        
    game = OthelloState(6, 8)
    game.print_state()

    game.drop_disc(3,5)
    game.print_state()

    game.drop_disc(4,3)
    game.print_state()

    game.drop_disc(3,2)
    game.print_state()

    game.drop_disc(2,5)
    game.print_state()

    game.drop_disc(1,4)
    game.print_state()

    try:
        game.drop_disc(1,4)
        game.print_state()
    except OthelloError as e:
        print(e)

    game.drop_disc(2,2)
    game.print_state()

    game.drop_disc(1,3)
    game.print_state()

    game.drop_disc(3,6)
    game.print_state()



if __name__ == "__main__":
    test()

    


    
