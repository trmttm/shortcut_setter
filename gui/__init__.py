import json
from typing import Callable

from interface_view import ViewABC
from stacker import Stacker
from stacker import widgets as w
from view_tkinter.TkImplementations.keyboard_shortcut import modifier_to_elements_str

KEY_CANCEL = 'Cancel'
KEY_APPLY = 'Apply'
KEY_DONE = 'Done'


def get_entry_id(n) -> str:
    return f'entry_command_{n}'


def get_shortcut_label_id(n) -> str:
    return f'label_command_{n}'


def top(s: Stacker):
    return s.hstack(
        w.Spacer(),
        w.Label('label_title').text('Configure Shortcut Keys').padding(0, 20),
        w.Spacer(),
    )


def scrollable(s: Stacker, commands_to_short_cuts: dict):
    return s.vstack_scrollable(
        *tuple(s.hstack(
            w.CheckButton(f'check_button_command_{n}').padding(30, 0),
            w.Label(f'label_command_{n}').text(f'{n}. {command_name}'),
            w.Entry(get_entry_id(n)).default_value(shortcut_key),
            w.Label(get_shortcut_label_id(n)).text(shortcut_key).width(30).padding(30, 0),
            w.Spacer().adjust(-3),
        ) for (n, (command_name, shortcut_key)) in enumerate(commands_to_short_cuts.items()))
    )


def buttons(s: Stacker, callback: Callable):
    return s.hstack(
        w.Spacer(),
        w.Button('button_cancel').text('Cancel').command(lambda: callback(KEY_CANCEL)),
        w.Button('button_apply').text('Apply').command(lambda: callback(KEY_APPLY)),
        w.Button('button_done').text('Done').command(lambda: callback(KEY_DONE)),
        w.Spacer(),
    )


def create_view_model_of_shortcut_setter(callback: Callable, commands_to_short_cuts: dict, specified_parent=None):
    from stacker import Stacker
    stacker = Stacker(specified_parent=specified_parent)
    stacker.vstack(
        top(stacker),
        scrollable(stacker, commands_to_short_cuts),
        buttons(stacker, callback),
        w.Spacer().adjust(-2),
    )
    return stacker.view_model


def load_shortcut_configuration_file(file_path):
    with open(file_path) as json_file:
        return json.load(json_file)


def save_shortcut_configuration_file(file_path, data: dict):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file)


def get_state(v: ViewABC, n_commands: int):
    return tuple(v.get_value(get_shortcut_label_id(n)) for n in range(n_commands))


def bind_commands(n: int, v: ViewABC):
    v.set_keyboard_shortcut_handler(get_entry_id(n), lambda modifier, key: upon_keyboard_to_entry(n, v, modifier, key))


def upon_keyboard_to_entry(i: int, v: ViewABC, modifier, key):
    modifier_keys = modifier_to_elements_str.get(modifier, '')
    keyboard_shortcut_str = ''
    for n, modifier_key_str in enumerate(modifier_keys):
        if modifier_key_str:
            if n > 0:
                keyboard_shortcut_str += f',{modifier_key_str.capitalize()}'
            else:
                keyboard_shortcut_str += f'{modifier_key_str.capitalize()}'

    if keyboard_shortcut_str and key:
        keyboard_shortcut_str += f',{key.upper()}'
    else:
        keyboard_shortcut_str += f'{key.upper()}'

    if keyboard_shortcut_str:
        v.set_value(get_entry_id(i), '')
        v.set_value(get_shortcut_label_id(i), keyboard_shortcut_str)
