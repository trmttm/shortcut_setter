import unittest


class MyTestCase(unittest.TestCase):
    def test_gui(self):
        import gui
        commands_to_short_cuts = {
            'Do this1': 'Shift,Control,a',
            'Do this2': 'Shift,Control,b',
            'Do this3': 'Shift,Control,b',
            'Do this4': 'Shift,Control,b',
            'Do this5': 'Shift,Control,b',
            'Do this6': 'Shift,Control,b',
            'Do this7': 'Shift,Control,b',
            'Do this8': 'Shift,Control,b',
            'Do this9': 'Shift,Control,b',
            'Do this10': 'Shift,Control,b',
        }
        from view_tkinter import View
        app = View()

        def callback(command_str):
            if command_str == gui.KEY_CANCEL:
                pass
            elif command_str == gui.KEY_APPLY:
                pass
            elif command_str == gui.KEY_DONE:
                pass
            print(command_str, gui.get_state(app, len(commands_to_short_cuts)))

        view_model = gui.create_view_model_of_shortcut_setter(callback, commands_to_short_cuts)
        app.add_widgets(view_model)
        [gui.bind_commands(n, app) for n in range(len(commands_to_short_cuts))]
        app.launch_app()


if __name__ == '__main__':
    unittest.main()
