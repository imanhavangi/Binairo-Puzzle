from time import time
from Binairo import *
from Cell import *
from State import *
## w b  
def main():
    input_numbers = []  ## first row = size of puzzle(n)  ## second row = number of cells that have color in the statrt  (m)  ## row 3 to row 3+m : 
    input=open("input2.txt").readlines()
    for line in input:
        line = line.rstrip()
        numbers = line.split(' ')
        n = [int(number) for number in numbers]
        input_numbers.append(n)
    

    board = []
    size_puzzle = input_numbers[0][0]
    for i in range(0,size_puzzle):
        row = []
        for j in range(0,size_puzzle):
            cell = Cell(i,j)
            row.append(cell)
        board.append(row)
    # print(board[0][1].domain)
   
    for i in range(2,len(input_numbers)) :
        
        
        if input_numbers[i][2]==0 : # w
            board[input_numbers[i][0]][input_numbers[i][1]].value='W'
            board[input_numbers[i][0]][input_numbers[i][1]].domain=['n']

        if input_numbers[i][2]==1 :  # b
            board[input_numbers[i][0]][input_numbers[i][1]].value='B'
            board[input_numbers[i][0]][input_numbers[i][1]].domain=['n']
       
    state = State(size_puzzle,board)  
    print('initial board:')
    state.print_board()
    start_time =time()
    #backTrack(state)   implement backTrack and other csp functions in Binairo.py

    end_time= time()
    print('time: ',end_time-start_time)



if __name__=="__main__":
    main()

 