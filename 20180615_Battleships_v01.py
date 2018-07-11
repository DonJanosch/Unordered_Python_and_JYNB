splash = 'O'
hit = 'X'
ship = '8'
water = ' '
board_delimiter = '|'
board_size = 10
ascii_offset = 97
position_delimiter = ','

chr2col_dict = {chr(num+ascii_offset):num for num in range(board_size)}
col2chr_dict = {num:chr(num+ascii_offset) for num in range(board_size)}
chr2col = lambda x: chr2col_dict[str(x).lower()]
col2chr = lambda colum_numner:col2chr_dict[int(colum_numner)]
possible_rows,possible_cols = list(col2chr_dict.keys()),list(col2chr_dict.values())
orientations = ['l','u','r','d']

fill_num = lambda number:' '*(len(str(board_size))-len(str(number)))+str(number)

board = [[water for _ in range(board_size)] for _ in range(board_size)]

def position_to_coordinates(position):
    return (int(position[1])-1,chr2col(position[0]))

def print_board():
    print(fill_num(' '),' '.join(col2chr(row) for row in range(board_size)))
    for row in range(board_size):
        print('{}{}{}{}{}'.format(fill_num(row+1),board_delimiter,board_delimiter.join(board[row][col] for col in range(board_size)),board_delimiter,fill_num(row+1)))
    print(fill_num(' '),' '.join(col2chr(num) for num in range(board_size)))

def ask_for_ship_placement_position():
    position_ok = False
    while not position_ok:
        position = input('Please enter the ships position (coordinate) and orientation (up, left, right, down) separated with {} e.g. A1{}down:\n'.format(position_delimiter,position_delimiter)).split(position_delimiter)
        if len(position)==2:
            if len(position[0])==2:
                if position[1].lower()[0] in orientations and position[0].lower()[0] in possible_cols and int(position[0][1]) in possible_rows:                
                    position_ok = True
    return (position_to_coordinates(position[0]),position[1])

def place_ship(position,orientation,ship_length):
    row,col = position
    if orientation == 'u':
        pass
    

print_board()
pos,orientation = ask_for_ship_placement_position()

