from pyray import get_touch_point_count, get_touch_point_id, get_touch_position, MouseButton, GamepadButton, \
    is_mouse_button_pressed, is_key_pressed, is_key_down, KeyboardKey, is_gamepad_button_down, \
    get_gamepad_axis_movement, is_mouse_button_down, is_gamepad_button_pressed


class InputManager():
    """handles input from keyboard, gamepad (digital and analog), touch screen"""
    def __init__(self):
        self.joystick_touch_id = -1
        self.touch_origin = 0
        self.touch_offset = 0.0
        self.touch_ids = []

    def is_input_left(self):
        return (
                is_key_down(KeyboardKey.KEY_LEFT)
                or is_gamepad_button_down(0, GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_LEFT)
                or get_gamepad_axis_movement(0, 0) < -0.1
                or self.get_touch_virtual_axis_movement() < 0.0
        )


    def is_input_right(self):
        return (
                is_key_down(KeyboardKey.KEY_RIGHT)
                or is_gamepad_button_down(0, GamepadButton.GAMEPAD_BUTTON_LEFT_FACE_RIGHT)
                or get_gamepad_axis_movement(0, 0) > 0.1
                or self.get_touch_virtual_axis_movement() > 0.0
        )


    def is_input_fire(self):
        return is_key_down(KeyboardKey.KEY_A) or is_gamepad_button_down(
            0, GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_DOWN
        ) or is_mouse_button_down(MouseButton.MOUSE_BUTTON_RIGHT)
        # second finger touch also works as right button, tap to fire


    def is_input_zap_pressed(self):
        return is_key_pressed(KeyboardKey.KEY_SPACE) or is_gamepad_button_pressed(
            0, GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_RIGHT
        ) or is_mouse_button_down(MouseButton.MOUSE_BUTTON_MIDDLE)
        # third finger touch also works as middle button, tap two fingers to fire


    def is_input_start_pressed(self):
        return is_key_pressed(KeyboardKey.KEY_ENTER) or is_gamepad_button_pressed(
            0, GamepadButton.GAMEPAD_BUTTON_RIGHT_FACE_DOWN
        ) or is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT)
        # first finger touch also works as left button


    def update_touch_input(self):
        """tracks finger touches, first one becomes virtual joystick"""
        self.touch_ids.clear()
        for i in range(get_touch_point_count()):
            self.touch_ids.append(get_touch_point_id(i))
            if self.joystick_touch_id == -1:
                self.joystick_touch_id = get_touch_point_id(i)
                self.touch_origin = get_touch_position(i).x
        if self.joystick_touch_id != -1:
            if self.joystick_touch_id in self.touch_ids:
                self.touch_offset = get_touch_position(self.touch_ids.index(self.joystick_touch_id)).x - self.touch_origin
            else:
                self.joystick_touch_id = -1
                self.touch_offset = 0

    def get_touch_virtual_axis_movement(self):
        """return virtual joystick y axis - drag finger on screen to control"""
        return max(-1.0, min(self.touch_offset/30, 1.0))

    def get_combined_axis_movement(self):
        """returns physical controller y axis and also virtual joystick y axis"""
        return get_gamepad_axis_movement(0, 0) + self.get_touch_virtual_axis_movement()