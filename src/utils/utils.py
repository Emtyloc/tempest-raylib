from pyray import is_key_down, is_gamepad_button_down, KeyboardKey, GamepadButton, get_gamepad_axis_movement, \
    is_key_pressed, is_gamepad_button_pressed

#https://refactoring.guru/es/design-patterns/singleton/python/example

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


def is_input_left():
    return (
        is_key_down(KeyboardKey.KEY_LEFT)
        or is_gamepad_button_down(0, GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_LEFT)
        or get_gamepad_axis_movement(0, 0) < -0.1
    )


def is_input_right():
    return (
        is_key_down(KeyboardKey.KEY_RIGHT)
        or is_gamepad_button_down(0, GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_RIGHT)
        or get_gamepad_axis_movement(0, 0) > 0.1
    )


def is_input_fire():
    return is_key_down(KeyboardKey.KEY_A) or is_gamepad_button_down(
        0, GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_DOWN
    )


def is_input_zap_pressed():
    return is_key_pressed(KeyboardKey.KEY_SPACE) or is_gamepad_button_pressed(
        0, GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_RIGHT
    )


def is_input_start_pressed():
    return is_key_pressed(KeyboardKey.KEY_ENTER) or is_gamepad_button_pressed(
        0, GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_DOWN
    )
