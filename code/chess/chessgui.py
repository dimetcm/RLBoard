import tkinter as tk

board_size = 300
board_square_size = board_size / 8.0


def convert_position_to_square_name(x, y):
    # todo: support board flipping
    files_str = "ABCDEFGH"
    file_idx = x // int(board_square_size)
    file_idx = min(file_idx, 7)

    rank = (board_size - y) // int(board_square_size)
    rank = min(rank, 7)
    return files_str[file_idx] + str(rank + 1)


def move(event):
    print(convert_position_to_square_name(event.x, event.y))


def create_board():
    frame = tk.Frame()
    frame.pack()

    board_canvas = tk.Canvas(frame, bg="black", height=board_size + 1, width=board_size + 1, borderwidth=0,
                             highlightthickness=0)
    board_canvas.pack()

    for y in range(8):
        for x in range(8):
            x_coord = x * board_square_size
            y_coord = y * board_square_size

            color = "wheat" if (x + y) % 2 == 0 else "black"
            board_canvas.create_rectangle(x_coord, y_coord, x_coord + board_square_size, y_coord + board_square_size,
                                          outline="black", fill=color)

    board_canvas.bind('<Motion>', move)


window = tk.Tk()
create_board()
window.mainloop()
