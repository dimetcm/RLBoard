import tkinter as tk
from PIL import Image, ImageTk

FILES_STR = "ABCDEFGH"


class Square:

    def __init__(self, square_name):
        assert len(square_name) == 2
        assert square_name[0] in FILES_STR
        assert 1 <= int(square_name[1]) <= 8

        self.file_idx = FILES_STR.index(square_name[0])
        self.rank_idx = int(square_name[1]) - 1


class ChessBoardGUI:

    def __init__(self, board_size = 400):
        self.board_size = board_size
        self.board_square_size = board_size / 8.0
        self.images = {}
        self.board_canvas = None
        self.window = tk.Tk()
        self.__create_board()
        self.__load_images()


    def __create_board(self):
        frame = tk.Frame()
        frame.pack()

        self.board_canvas = tk.Canvas(frame, bg="black", height=self.board_size + 1, width=self.board_size + 1, borderwidth=0,
                                 highlightthickness=0)
        self.board_canvas.pack()

        for y in range(8):
            for x in range(8):
                x_coord = x * self.board_square_size
                y_coord = y * self.board_square_size

                color = "wheat" if (x + y) % 2 == 0 else "sienna"
                self.board_canvas.create_rectangle(x_coord, y_coord, x_coord + self.board_square_size,
                                              y_coord + self.board_square_size,
                                              outline="black", fill=color)

        self.board_canvas.bind('<Motion>', self.__move)

    def __load_images(self):
        # lowercase for black, uppercase for white
        filenames = {
            'p': "b_pawn_png_512px.png",
            'r': "b_rook_png_512px.png",
            'n': "b_knight_png_512px.png",
            'b': "b_bishop_png_512px.png",
            'q': "b_queen_png_512px.png",
            'k': "b_king_png_512px.png",
            'P': "w_pawn_png_512px.png",
            'N': "w_knight_png_512px.png",
            'R': "w_rook_png_512px.png",
            'B': "w_bishop_png_512px.png",
            'Q': "w_queen_png_512px.png",
            'K': "w_king_png_512px.png",
        }

        path = "../../data/chess pieces/512h/"
        for k, v in filenames.items():
            # print(path + v)
            image_file = Image.open(path + v)
            image_file = image_file.resize((int(self.board_square_size - 5), int(self.board_square_size - 5)), Image.ANTIALIAS)
            self.images[k] = ImageTk.PhotoImage(image_file)

    def __move(self, event):
        print(self.convert_position_to_square_name(event.x, event.y))

    def convert_position_to_square_name(self, x, y):
        # todo: support board flipping
        file_idx = x // int(self.board_square_size)
        file_idx = min(file_idx, 7)

        rank = (self.board_size - y) // int(self.board_square_size)
        rank = min(rank, 7)
        return FILES_STR[file_idx] + str(rank + 1)

    def show(self):
        self.window.mainloop()

    def add_piece(self, piece, square):
        assert piece in self.images

        x_pos = (square.file_idx + 0.5) * self.board_square_size
        y_pos = (7 - square.rank_idx + 0.5) * self.board_square_size
        self.board_canvas.create_image(x_pos, y_pos, image=self.images[piece])


boardGUI = ChessBoardGUI()
boardGUI.add_piece('p', Square('A7'))
boardGUI.add_piece('k', Square('E8'))
boardGUI.show()
