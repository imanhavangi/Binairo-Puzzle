from copy import deepcopy
import math
import State
        

def check_Adjancy_Limit(state: State):

    #check rows
    for i in range(0,state.size):
        for j in range(0,state.size-2):
            if(state.board[i][j].value.upper()==state.board[i][j+1].value.upper() and 
            state.board[i][j+1].value.upper()==state.board[i][j+2].value.upper() and
            state.board[i][j].value !='_'and 
            state.board[i][j+1].value !='_'and
            state.board[i][j+2].value !='_' ):
                
                return False
    #check cols
    for j in range(0,state.size): # cols
        for i in range(0,state.size-2): # rows
            if(state.board[i][j].value.upper()==state.board[i+1][j].value.upper() 
            and state.board[i+1][j].value.upper()==state.board[i+2][j].value.upper() 
            and state.board[i][j].value !='_'
            and state.board[i+1][j].value !='_'
            and state.board[i+2][j].value !='_' ):
               
                return False
    
    return True

def check_circles_limit(state:State): # returns false if number of white or black circles exceeds board_size/2
    #check in rows
    for i in range(0,state.size): # rows
        no_white_row=0
        no_black_row=0
        for j in range(0,state.size): # each col
            # if cell is black or white and it is not empty (!= '__')
            if (state.board[i][j].value.upper()=='W' and state.board[i][j].value != '_'): no_white_row+=1
            if (state.board[i][j].value.upper()=='B' and state.board[i][j].value != '_'): no_black_row+=1
        if no_white_row > state.size/2 or no_black_row > state.size/2:
            
            return False
        no_black_row=0
        no_white_row=0

    # check in cols
    for j in range(0,state.size):#cols
        no_white_col=0
        no_black_col=0
        for i in range(0,state.size): # each row
            # if cell is black or white and it is not empty (!= '__')
            if (state.board[i][j].value.upper()=='W' and state.board[i][j].value != '_'): no_white_col+=1
            if (state.board[i][j].value.upper()=='B' and state.board[i][j].value != '_'): no_black_col+=1
        if no_white_col > state.size/2 or no_black_col > state.size/2:
            
            return False
        no_black_col=0
        no_white_col=0
    
    return True

def is_unique(state:State): # checks if all rows are unique && checks if all cols are unique
    # check rows
    for i in range(0,state.size-1):
        for j in range(i+1,state.size):
            count = 0
            for k in range(0,state.size):
                if(state.board[i][k].value.upper()==state.board[j][k].value.upper()
                and state.board[i][k].value!='_'
                and state.board[j][k].value!='_'):
                    count+=1
            if count==state.size:
                
                return False
            count=0

    # check cols
    for j in range(0,state.size-1):
        for k in range(j+1,state.size):
            count_col =0 
            for i in range(0,state.size):
                 if(state.board[i][j].value.upper()==state.board[i][k].value.upper()
                 and state.board[i][j].value != '_'
                 and state.board[i][k].value != '_' ):
                    count_col+=1
            if count_col == state.size:
               
                return False
            count_col=0 
   
    return True

def is_assignment_complete(state:State): # check if all variables are assigned or not
    for i in range(0,state.size):
        for j in range(0,state.size):
            if(state.board[i][j].value == '_'): # exists a variable wich is not assigned (empty '_')
                
                return False

    
    return True

def is_consistent(state:State):
    
    return check_Adjancy_Limit(state) and check_circles_limit(state) and is_unique(state)

def check_termination(state:State):
    
    return is_consistent(state) and is_assignment_complete(state)


def backtrack1(state):
    if is_assignment_complete(state):
        return state

    i = 0
    j = 0
    while i < state.size and state.board[i][j].value != '_':
        j += 1
        if j == state.size:
            j = 0
            i += 1
    first = state.board[i][j]
    
    for domain in first.domain:
        local_state = deepcopy(state)
        local_state.board[first.x][first.y].value = domain
        if is_consistent(local_state):
            result = backtrack1(local_state)
            if result is not None:
                return result
    return None

def backtrack2(state):
    if is_assignment_complete(state):
        return state
    
    v = None

    i = 0
    j = 0
    while i < state.size and not ((state.board[i][j].value == '_') and (state.board[i][j].domain == 'w' or state.board[i][j].domain == 'b')):
        j += 1
        if j == state.size:
            j = 0
            i += 1

    if (i < state.size and j < state.size):
        if (state.board[i][j].value == '_' and (state.board[i][j].domain == 'w' or state.board[i][j].domain == 'b')):
            v = deepcopy(state.board[i][j])

    if v is None:
        for i in range(state.size):
            for j in range(state.size):
                if(state.board[i][j].value == '_'):
                    v = deepcopy(state.board[i][j])
                    break
                else:
                    continue
                break
    
    if v.domain == ['b'] or v.domain == ['w']:
        local_state = deepcopy(state)
        local_state.board[v.x][v.y].value = v.domain[0]
        new_state = forward_checking(local_state,v)
        if (is_consistent(new_state)):
            result = backtrack2(local_state)
            if result is not None:
                return result

    row = v.x
    col = v.y
    white_count = 0
    black_count = 0
    for i in range(0,state.size):
        if state.board[row][i].value == 'W' or state.board[row][i].value == 'w':
            white_count += 1
        if state.board[row][i].value == 'B' or state.board[row][i].value == 'b':
            black_count += 1
    for i in range(0,state.size):
        if state.board[i][col].value == 'W' or state.board[i][col].value == 'w':
            white_count += 1
        if state.board[i][col].value == 'B' or state.board[i][col].value == 'b':
            black_count += 1
    if white_count > black_count:
        v.domain.reverse()
    for domain in v.domain:
        local_state = deepcopy(state)
        local_state.board[v.x][v.y].value = domain
        new_state = forward_checking(local_state,v)
        if is_consistent(new_state):
            result = backtrack2(local_state)
            if result is not None:
                return result
    return None

def forward_checking(state, variable):
    local_state = deepcopy(state)
    row = variable.x
    column = variable.y

    white_colored = 0
    black_colored = 0
    for c in range(0,local_state.size):
        color = local_state.board[row][c].value
        if color == 'w' or 'W':
            white_colored += 1
        elif color == 'b' or 'B':
            black_colored += 1
    if white_colored == local_state.size / 2:
        for c in range(0,local_state.size):
            cell = local_state.board[row][c]
            if cell.value == '_':
                cell.value = 'b'
    elif black_colored == local_state.size /2:
        for c in range(0,local_state.size):
            cell = local_state.board[row][c]
            if cell.value == '_' :
               cell.value = 'w'

    white_colored = 0
    black_colored = 0
    for r in range(0,local_state.size):
        color = local_state.board[r][column].value
        if color == 'w' or 'W':
            white_colored += 1
        elif color == 'b' or 'B':
            black_colored += 1
    if white_colored == local_state.size / 2:
        for r in range(0,local_state.size):
            cell = local_state.board[r][column]
            if cell.value == '_':
               cell.value = 'b'
    elif black_colored == local_state.size /2:
        for r in range(0,local_state.size):
            cell = local_state.board[r][column]
            if cell.value == '_':
                cell.value = 'w'


    current_cell = 'n'
    next_cell = 'n'
    for c in range(0,local_state.size):
        color = local_state.board[row][c].value
        current_cell = next_cell
        next_cell = color
        
        if (current_cell.lower() == next_cell.lower()):
            if (current_cell == 'w' or current_cell =='W'):
                try:
                    cell = local_state.board[row][c-2]
                    if cell.value == '_':
                        cell.value = 'b'
                except:
                    pass
                try:
                    cell = local_state.board[row][c+1]
                    if cell.value == '_':
                       cell.value = 'b'
                except:
                    pass
            elif (current_cell == 'b' or current_cell == 'B'):
                try:
                    cell = local_state.board[row][c-2]
                    if cell.value == '_':
                       cell.value = 'w'
                except:
                    pass
                try:
                    cell = local_state.board[row][c+1]
                    if cell.value == '_':
                        cell.value = 'w'
                except:
                    pass
        

    current_cell = 'n'
    next_cell = 'n'
    for r in range(0,local_state.size):
        color = local_state.board[r][column].value
        current_cell = next_cell
        next_cell = color
        if (current_cell.lower() == next_cell.lower()):
            if (current_cell == 'w' or current_cell == 'W'):
                try:
                    cell = local_state.board[r-2][column]
                    if cell.value == '_':
                        cell.value = 'b'
                except:
                    pass
                try:
                    cell = local_state.board[r+1][column]
                    if cell.value == '_':
                        cell.value = 'b'
                except:
                    pass
            elif (current_cell == 'b' or current_cell == 'B'):
                try:
                    cell = local_state.board[r-2][column]
                    if cell.value == '_':
                        cell.value = 'w'
                except:
                    pass
                try:
                    cell = local_state.board[r+1][column]
                    if cell.value == '_':
                       cell.value = 'w'
                except:
                    pass
    return local_state

