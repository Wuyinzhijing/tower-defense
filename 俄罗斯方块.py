import tkinter as tk


Row = 20
Col = 12

cell_size = 30

height = Row * cell_size
width = Col * cell_size

SHAPES = {
    "O": [(-1, -1), (0, -1), (-1, 0), (0, 0)],
    "S": [(-1, 0), (0, 0), (0, -1), (1, -1)],
    "T": [(-1, 0), (0, 0), (0, -1), (1, 0)],
    "I": [(0, 1), (0, 0), (0, -1), (0, -2)],
    "L": [(-1, 0), (0, 0), (-1, -1), (-1, -2)],
    "J": [(-1, 0), (0, 0), (0, 1), (0, -2)],
    "Z": [(-1, -1), (0, -1), (0, 0), (1, 0)]
}


SHAPESCOLOR = {
    "O": "blue",
    "S": "red",
    "T": "yellow",
    "I": "green",
    "L": "purple",
    "J": "orange",
    "Z": "Cyan",
}



win = tk.Tk()

def draw_cell_background(canvas, col, row, color = "#CCCCCC"):
    x0 = col * cell_size
    y0 = row * cell_size

    x1 = col * cell_size + cell_size
    y1 = row * cell_size + cell_size


    canvas.create_rectangle(x0, y0, x1, y1, fill = color, outline = 'white', width = 2)

def draw_blank_board(canvas):
    for ri in range(Row):
        for cj in range(Col):
            draw_cell_background(canvas, cj, ri)


def draw_cells(canvas, col, row, cell_list, color = "#CCCCCC"):
    for cell in cell_list:
        cell_col, cell_row = cell
        ci = cell_col + col
        ri = cell_row + row

        if 0 <= col < Col and 0 <= row < Row:
            draw_cell_background(canvas, ci, ri, color)


canvas = tk.Canvas(win, width=width, height=height)


canvas.pack()

draw_blank_board(canvas)

FPS = 500

def draw_block_move(canvas, block, direction=[0, 0]):

    shape_type = block['kind']
    c, r = block['cr']
    cell_list = block['cell_list']

    draw_cells(canvas, c, r, cell_list)

    dc, dr = direction
    new_c, new_r = c + dc, r + dr
    block['cr'] = [new_c, new_r]
    draw_cells(canvas, new_c, new_r, cell_list, SHAPESCOLOR[shape_type])


one_block = {
    'kind': 'O',
    'cell_list': SHAPES['O'],
    'cr': [3, 3],
}

draw_block_move(canvas, one_block)

def game_loop():
    win.update()

    down = [0,1]
    draw_block_move(canvas, one_block, down)
    win.after(FPS, game_loop)

game_loop()
win.mainloop()