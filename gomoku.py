''' By Anup Deb and Rojigan Gengatharan '''
 

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    ''' Function: Return whether or not a sequence is bounded, semi-bounded, or unbound
    Parameters: the list board, integer x and y end values, length of sequence, change in x and y'''
    x_begin = find_begin_x(x_end, length, d_x)                              
    y_begin = find_begin_y(y_end, length, d_y)
    
    if bounded(board, x_end, y_end, d_y, d_x,"end") + bounded(board, x_begin, y_begin, d_y, d_x, "begin") == 2:
        return "CLOSED"
    elif bounded(board, x_end, y_end,  d_y, d_x, "end") + bounded(board, x_begin, y_begin,  d_y, d_x, "begin") == 1:
        return "SEMIOPEN"
    elif bounded(board, x_end, y_end,  d_y, d_x, "end") + bounded(board, x_begin, y_begin,  d_y, d_x, "begin") == 0:
        return "OPEN"
    
    
def is_empty(board):
    '''Function: Return whether or not the board is empty
    Pareameters: the list board'''
    for i in range(len(board)):                 #Increments through every element in board   
        for j in range(len(board[0])):
            if board[i][j] != " ":
                return False
    return True
    
def bounded(board, x, y, d_y, d_x, ending):
    boundary = [0,len(board) - 1]                   #values
    if ending == "end":
        return int((x in boundary and d_x != 0) or (y in boundary and d_y != 0) or board[y+d_y][x+d_x] != " ")
    elif ending == "begin":
        return int((x in boundary and d_x != 0) or (y in boundary and d_y != 0) or board[y-d_y][x-d_x] != " ")
        
def find_begin_x(x_end,length,d_x):
    '''Function: returns x value at beginning of sequence
    Parameters: ending x_value and change in x, both integers'''      
    return x_end - ((length - 1) * d_x)            #final - change = initial
    
def find_begin_y(y_end, length,d_y):
    '''Function: returns y value at beginning of sequence
    Parameters: ending y_value and change in y, both integers'''
    return y_end - ((length - 1) * d_y)
    
def search_max(board):
    first_check_completed = False 
    for i in range(len(board)):
        for j in range(len(board[0])):
            if first_check_completed == True: 
                if board[i][j] == " ":
                    board[i][j] = "b"
                    current = score(board)
                    if current > max:
                        max = current
                        move_y = i
                        move_x = j
                    board[i][j] = " "
            elif first_check_completed == False:
                if board[i][j] == " ":
                    move_y = i
                    move_x = j
                    board[i][j] = "b"
                    current = score(board)
                    max = current
                    board[i][j] = " "
                    first_check_completed = True 
    return move_y, move_x
    
def is_win(board):
    if detect_rows(board, "b", 5)[0] > 0 or detect_rows(board, "b", 5)[1] > 0 or  detect_rows_including_closed(board, "b", 5)[2] > 0:
        return "Black won"
    elif detect_rows(board, "w", 5)[0] > 0 or detect_rows(board, "w", 5)[1] > 0 or detect_rows_including_closed(board, "w", 5)[2] > 0:
        return "White won"
    else:
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == " ":
                    return "Continue playing"
        return "Draw"

    
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    '''assumes x_start and y_start are given on the edge of the board'''
    a, b, c = detect_row_including_closed(board, col, y_start, x_start, length, d_y, d_x)
    return a, b 
def detect_row_including_closed(board, col, y_start, x_start, length, d_y, d_x):      

    length_of_row = 1
    #sets values to return to 0 initially 
    
    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0
    
    #this variable will be used to measure the length of a sequence 
    measured_length = 0
    
    #finds the ending coordinate of the row
    row_x_end = x_start 
    row_y_end = y_start 
    while (row_x_end < len(board) and row_x_end >= 0) and (row_y_end < len(board) and row_y_end >= 0): 
        row_x_end += d_x
        row_y_end += d_y
        length_of_row += 1
    row_x_end -= d_x
    row_y_end -= d_y
    length_of_row -= 1

   
    #goes through squares one by one, from start to end of a row, finds the number of open sequences and semiopen sequences 
    
    #for loop goes through squares in the row
    for i in range(0, length_of_row):
        #measures the length of a sequence containing only squares of the same colour
        if board[y_start + i * d_y][x_start + i * d_x] == col:
            measured_length += 1
        
        #if the measured length is the length we're looking for, then see if sequence is open or semiopen, if it's closed we don't accumulate anything
        else:
            if measured_length == length:
                if is_bounded(board, y_start + (i - 1) * d_y , x_start + (i - 1) * d_x , length, d_y, d_x) == "OPEN":
                    open_seq_count += 1
                elif is_bounded(board, y_start + (i - 1) * d_y, x_start + (i - 1) * d_x, length, d_y, d_x) == "SEMIOPEN":
                    semi_open_seq_count += 1
                elif is_bounded(board, y_start + (i - 1) * d_y, x_start + (i - 1) * d_x, length, d_y, d_x) == "CLOSED":
                    closed_seq_count += 1    
            #to measure length of next sequence
            measured_length = 0             
        
    #once for loop is finished, the last sequence it checked might have been a relevant one 
    if measured_length == length:
        if is_bounded(board, y_start + i * d_y, x_start + i * d_x, length, d_y, d_x) == "OPEN":
            open_seq_count += 1
        elif is_bounded(board, y_start + i * d_y, x_start + i * d_x, length, d_y, d_x) == "SEMIOPEN":
            semi_open_seq_count += 1
        elif is_bounded(board, y_start + (i - 1) * d_y, x_start + (i - 1) * d_x, length, d_y, d_x) == "CLOSED":
            closed_seq_count += 1      
    
    
    return open_seq_count, semi_open_seq_count, closed_seq_count    
def detect_rows(board, col, length):
    a, b, c = detect_rows_including_closed(board, col,length)
    return a, b
    
def detect_rows_including_closed(board, col,length):
    open_seq_count, semi_open_seq_count, closed_seq_count = 0, 0, 0
   
    #check all horizontal vertical first
    #detect_row(board, col, y_start, x_start, length, d_y, d_x)
    
    for i in range(len(board)): 
        open_seq_count += detect_row_including_closed(board, col, 0, i, length, 1, 0)[0]
        semi_open_seq_count += detect_row_including_closed(board, col, 0, i, length, 1,0)[1]
        closed_seq_count += detect_row_including_closed(board, col, 0, i, length, 1, 0)[2] 
        
    for i in range(len(board)):
        open_seq_count += detect_row(board, col, i, 0, length, 0, 1)[0]
        semi_open_seq_count += detect_row(board, col, i, 0, length, 0, 1)[1]  
        closed_seq_count += detect_row_including_closed(board, col, i, 0, length, 0, 1)[2] 
        
    #go through all left to right diagonals     
    for i in range(len(board)):
        open_seq_count += detect_row(board, col, 0, i, length, 1,1)[0]
        semi_open_seq_count += detect_row(board, col, 0, i, length, 1,1)[1]  
        closed_seq_count += detect_row_including_closed(board, col, 0, i, length, 1,1)[2]  
    for i in range(1,len(board)): 
        open_seq_count += detect_row(board, col, i, 0, length, 1,1)[0]
        semi_open_seq_count += detect_row(board, col, i, 0, length, 1,1)[1] 
        closed_seq_count += detect_row_including_closed(board, col, i, 0, length, 1,1)[2] 
        
    
    #go through all right to left diagonals
    for i in range(len(board)):
        open_seq_count += detect_row(board, col, 0, i, length, 1, -1)[0]
        semi_open_seq_count += detect_row(board, col, 0, i, length, 1, -1)[1] 
        closed_seq_count += detect_row_including_closed(board, col, 0, i, length, 1, -1)[2]
    for i in range(1,len(board)): 
        open_seq_count += detect_row(board, col, i, 7, length, 1, -1)[0]
        semi_open_seq_count += detect_row(board, col, i, 7, length, 1, -1)[1] 
        closed_seq_count += detect_row_including_closed(board, col, i, 7, length, 1, -1)[2]
    
    
    return open_seq_count, semi_open_seq_count, closed_seq_count
    
def score(board):
    MAX_SCORE = 100000
    
    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}
    
    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)
        
    
    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE
    
    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE
        
    return (-10000 * (open_w[4] + semi_open_w[4])+ 
            500  * open_b[4]                     + 
            50   * semi_open_b[4]                + 
            -100  * open_w[3]                    + 
            -30   * semi_open_w[3]               + 
            50   * open_b[3]                     + 
            10   * semi_open_b[3]                +  
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

    
def print_board(board):
    
    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"
    
    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1]) 
    
        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"
    
    print(s)
    

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board
                


def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))
        
    
    

        
    
def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])
    
    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)
            
        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
            
            
        
        
        
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)
        
        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        
            
            
def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col        
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    
    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    
    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #     
    
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);
    
    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #        
    #        
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0


board = make_empty_board(8) 
            
if __name__ == '__main__':
    play_gomoku(8)