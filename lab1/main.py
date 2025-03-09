import os

from src.paint_console import PaintApp


class App:
    def __init__(self):
        self._app = PaintApp()

    @staticmethod
    def _try_to_tuple_int(params):
        try:
            return tuple(map(int, params))
        except ValueError:
            raise Exception('Invalid parameters')


    def run(self):
        main_menu_flag = True
        drawing_menu_flag = False
        object_menu_flag = False
        coords_warning_msg = f"(x < {self._app.canvas_width}, y < {self._app.canvas_height})"
        msg = ""

        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(msg)
            msg = ""
            self._app.render_canvas()

            if main_menu_flag:
                cmd = input("0 Exit | 1 Draw | 2 Obj selection menu | 3 Save | 4 Load | 5 Undo | 6 Redo\n").strip()

                try:
                    if cmd == "0":
                        break
                    elif cmd == "1":
                        drawing_menu_flag = True
                        main_menu_flag = False
                    elif cmd == "2":
                        object_menu_flag = True
                        main_menu_flag = False
                    elif cmd == "3":
                        filename = input("Enter filename: ")
                        self._app.save_file(filename)
                    elif cmd == "4":
                        filename = input("Enter filename: ")
                        self._app.load_file(filename)
                    elif cmd == "5":
                        self._app.undo()
                    elif cmd == "6":
                        self._app.redo()
                    else:
                        raise Exception("Invalid command")
                except Exception as e:
                    msg = str(e)
            elif drawing_menu_flag:
                cmd = input('0 Exit | 1 Rectangle | 2 Triangle | 3 Ellipse\n')

                try:
                    if cmd == "0":
                        pass
                    elif cmd == "1":
                        params = input(f"Enter parameters (x, y, width, height)" + coords_warning_msg).strip()
                        params = self._try_to_tuple_int(params.split())
                        if len(params) != 4:
                            raise ValueError("Invalid parameters")
                        self._app.draw_rectangle(*params)
                    elif cmd == "2":
                        params = input("Enter parameters (x0, y0, x1, y1, x2, y2)"
                                       f"(topmost y < {self._app.canvas_height}, "
                                       f"leftmost x < {self._app.canvas_width}): ").strip()
                        params = self._try_to_tuple_int(params.split())
                        if len(params) != 6:
                            raise ValueError("Invalid parameters")
                        self._app.draw_triangle(*params)
                    elif cmd == "3":
                        params = input("Enter parameters (x, y, vert.rad, hor.rad): " + coords_warning_msg).strip()
                        params = self._try_to_tuple_int(params.split())
                        if len(params) != 4:
                            raise ValueError("Invalid parameters")
                        self._app.draw_ellipse(*params)
                    else:
                        raise Exception("Invalid command")
                except Exception as e:
                    msg = str(e)

                drawing_menu_flag = False
                main_menu_flag = True
            elif object_menu_flag:
                cmd = input(
                    '0 - Exit | i - Info | p - Previous | n - Next | m - Move | e - Erase | b - change bg\n').strip()

                try:
                    if cmd == "0":
                        pass
                    elif cmd == "p":
                        self._app.select_previous()
                    elif cmd == "n":
                        self._app.select_next()
                    elif cmd == "m":
                        params = input("Enter parameters (new x, new y): " + coords_warning_msg).strip().split()
                        params = self._try_to_tuple_int(params)
                        if len(params) != 2:
                            raise ValueError("Invalid parameters")
                        self._app.move_figure(*params)
                    elif cmd == "i":
                        msg = " | ".join([f"{key}: {value}" for key, value in self._app.get_figure_info().items()])
                    elif cmd == "e":
                        self._app.remove_figure()
                    elif cmd == "b":
                        cmd = input("Enter new bg: ").strip()
                        self._app.change_figure_bg(cmd)
                    else:
                        raise Exception("Invalid command")
                except Exception as e:
                    msg = str(e)

                object_menu_flag = False
                main_menu_flag = True


if __name__ == '__main__':
    app = App()
    app.run()

    # user store
