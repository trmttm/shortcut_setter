import unittest


class MyTestCase(unittest.TestCase):
    def test_gui(self):
        from view_tkinter import View
        from interface_tk import top_level_options
        from interface_tk import widget_model
        app = View()

        import shortcut_setter
        file_path = 'keyboard_shortcut.json'
        commands_to_short_cuts = shortcut_setter.load_shortcut_configuration_file(file_path)
        n_commands = len(commands_to_short_cuts)

        specified_parent = 'toplevel_root'
        title = 'Filter setting'
        width = 1000
        height = 500
        options = top_level_options(title, (width, height))

        def callback(command_str):
            print(command_str, shortcut_setter.get_state(app, n_commands))
            if command_str == shortcut_setter.KEY_CANCEL:
                pass
            elif command_str == shortcut_setter.KEY_APPLY:
                data = dict(zip(commands_to_short_cuts.keys(), shortcut_setter.get_state(app, n_commands)))
                shortcut_setter.save_shortcut_configuration_file(file_path, data)
            elif command_str == shortcut_setter.KEY_DONE:
                data = dict(zip(commands_to_short_cuts.values(), shortcut_setter.get_state(app, n_commands)))
                shortcut_setter.save_shortcut_configuration_file(file_path, data)
                app.close(specified_parent)

        view_model_root = [widget_model('root', specified_parent, 'toplevel', 0, 0, 0, 0, 'nswe', **options)]
        view_model_popup = shortcut_setter.create_view_model_of_shortcut_setter(callback, commands_to_short_cuts,
                                                                                specified_parent)
        view_model = view_model_root + view_model_popup
        app.add_widgets(view_model)
        [shortcut_setter.bind_commands(n, app) for n in range(n_commands)]
        app.launch_app()


if __name__ == '__main__':
    unittest.main()
