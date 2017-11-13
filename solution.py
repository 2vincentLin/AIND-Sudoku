assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(sudoku):
    """Eliminate values using the naked twins strategy.
    Args:
        sudoku(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the sudoku dictionary with the naked twins eliminated from peers.
        
    1. generate all boxes with possibilities== 2
    2. go though all its peers to see if any box has the same value
    3. check where is the peers (rows, cols or square)
    4. go through every box in the unit except itself and the same value peer
        and replace
    """
    temp= [box for box in sudoku.keys() if len(sudoku[box]) == 2]
    for box in temp:
        for peer in peers[box]:
            if sudoku[peer] == sudoku[box]:
                for unit in units[box]:
                    if peer in unit:
                        for digit in sudoku[box]:
                            for e in unit:
                                if (e == box) or (e == peer):
                                    continue
                                sudoku[e]= sudoku[e].replace(digit, '')
                                #sudoku= assign_value(sudoku, e, sudoku[e].replace(digit, ''))
                            
    return sudoku

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]
    

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    temp= []
    all_digit= '123456789'
    for e in grid:
        if e == '.':
            temp.append(all_digit)
        elif e in all_digit:
            temp.append(e)
    return dict(zip(boxes, temp))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(sudoku):
    '''
    if a box with only one digit, then remove this digit from its peers
    Args:
        sudoku(dict): The sudoku in dictionary form
    Returns:
        the sudoku(dict) with the impossibles removed from peers
        
    1. generate list with boxes with only one digit
    2. remove this digit from its peers
    '''
    temp= [box for box in sudoku.keys() if len(sudoku[box]) == 1]
    for box in temp:
        for peer in peers[box]:
            sudoku[peer]= sudoku[peer].replace(sudoku[box], '')
            #sudoku= assign_value(sudoku, peer, sudoku[peer].replace(sudoku[box], ''))
    return sudoku


def only_choice(sudoku):
    '''
    if a digit only appears in one box in its unit, then fill this box with this digit
    
    Args:
        sudoku(dict): The sudoku in dictionary form
    Returns:
        sudoku(dict) 
        
    scan through rows, cols and squares. the scan from 1 to 9.
    if a digit only appears one time, then the box should fill with this digit.
    '''
    for unit in unitlist:
        for digit in '123456789':
            temp= [box for box in unit if digit in sudoku[box]]
            if len(temp)== 1:
                sudoku[temp[0]]= digit
                #sudoku= assign_value(sudoku, temp[0], digit)
    return sudoku

def reduce_puzzle(sudoku):
    '''
    Use eleminate, naked_twins and only_choice on a sudoku(dict)
    
    Args:
        sudoku(dict): The sudoku in dictionary form
    Returns:
        sudoku(dict)
        
    this function only stops at no box to solve, it's not guaranteed to solve

    '''
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_before = len([box for box in sudoku.keys() if len(sudoku[box]) == 1])


        eliminate(sudoku)
        naked_twins(sudoku)
        only_choice(sudoku)
        
        # Check how many boxes have a determined value, to compare
        solved_after = len([box for box in sudoku.keys() if len(sudoku[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_before == solved_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in sudoku.keys() if len(sudoku[box]) == 0]):
            return False
    return sudoku

def search(sudoku):
    '''
    search the answer, starting from box with least possibilities.
    
    Args:
        sudoku(dict): The sudoku in dictionary form
    Returns:
        sudoku(dict)
        
    1. reduce sudoku first
    2. find the unsolved box with least possibilities
    3. try the first number
    4. call this function again
    5. if all len(box) == 1, then return the sudoku since it's solved    
    '''
    sudoku= reduce_puzzle(sudoku)
    if sudoku == False:
        return False
    if all(len(sudoku[box])== 1 for box in boxes):
        # all(generate expression), so no need to use list comprehension
        return sudoku
    _, least_box= min((len(box), box) for box in boxes if len(sudoku[box]) > 1)
    # least_box has least possibilities
    # min(tuple of tuple) will compare element lexicographically
    # e.g (1,1) < (1,2), (2,1) > (1,3)
    
    for s in sudoku[least_box]:
        new_sudoku= sudoku.copy()
        new_sudoku[least_box]= s
        result= search(new_sudoku)
        if result:
            return result

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    result= search(grid_values(grid))
    if result:
        return result
    else:
        return False


rows = 'ABCDEFGHI'
cols = '123456789'
boxes= cross(rows, cols)

row_units= [cross(r, cols) for r in rows]
col_units= [cross(rows, c) for c in cols]
square_units= [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]

diagonal_units= [[],[]]

for i in range(len(rows)):
    diagonal_units[0].append(rows[i]+cols[i])
    
for i in range(len(rows)):
    diagonal_units[1].append(rows[i]+cols[::-1][i])


unitlist = row_units + col_units + square_units + diagonal_units


units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    diag_sudoku_grid= '1....4.8.85...6...94...86....4...87.....8.....98........9.....8...8.3..........2.'
    display(solve(diag_sudoku_grid))


    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
