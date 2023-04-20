import unittest


class MyTestCase(unittest.TestCase):
    def test_gui(self):
        from view_tkinter import View
        app = View()

        import gui
        file_path = 'keyboard_shortcut.json'
        commands_to_short_cuts = gui.load_shortcut_configuration_file(file_path)
        n_commands = len(commands_to_short_cuts)

        def callback(command_str):
            if command_str == gui.KEY_CANCEL:
                pass
            elif command_str == gui.KEY_APPLY:
                data = dict(zip(commands_to_short_cuts.keys(), gui.get_state(app, n_commands)))
                gui.save_shortcut_configuration_file(file_path, data)
            elif command_str == gui.KEY_DONE:
                data = dict(zip(commands_to_short_cuts.values(), gui.get_state(app, n_commands)))
                gui.save_shortcut_configuration_file(file_path, data)
            print(command_str, gui.get_state(app, n_commands))

        view_model = gui.create_view_model_of_shortcut_setter(callback, commands_to_short_cuts)
        app.add_widgets(view_model)
        [gui.bind_commands(n, app) for n in range(n_commands)]
        app.launch_app()


if __name__ == '__main__':
    unittest.main()
