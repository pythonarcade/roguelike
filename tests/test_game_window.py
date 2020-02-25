from unittest.mock import call, Mock

from constants import NORMAL, SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, SELECT_LOCATION
from game_window import main, MyGame


def test_main(mocker):
    mock_game = mocker.patch("game_window.MyGame")
    mock_run = mocker.patch("game_window.arcade.run")

    main()

    assert mock_game.call_args == call(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    mock_game.return_value.setup.assert_called_once()
    mock_run.assert_called_once()


class TestMyGame:
    def test_init(self, mocker):
        mock_engine = mocker.patch("game_window.GameEngine")
        mock_arcade = mocker.patch("game_window.arcade")

        window = MyGame(100, 100, "foo")
        assert window.game_engine == mock_engine.return_value
        assert window.left_pressed is False
        assert window.right_pressed is False
        assert window.up_pressed is False
        assert window.down_pressed is False
        assert window.up_left_pressed is False
        assert window.up_right_pressed is False
        assert window.down_left_pressed is False
        assert window.down_right_pressed is False
        assert window.time_since_last_move_check == 0
        assert window.mouse_over_text is None
        assert window.mouse_position is None
        mock_arcade.set_background_color.assert_called_once_with(
            mock_arcade.color.BLACK
        )

    def test_setup(self, mocker):
        mock_engine = mocker.patch("game_window.GameEngine")
        mocker.patch("game_window.arcade")
        window = MyGame(100, 100, "foo")

        window.setup()

        mock_engine.return_value.setup.assert_called_once()

    def test_on_mouse_press_in_normal_state(self, mocker):
        mock_engine = mocker.patch("game_window.GameEngine")
        mock_pixel_to_char = mocker.patch("game_window.pixel_to_char")
        window = MyGame(100, 100, "foo")
        window.game_engine.game_state = NORMAL

        window.on_mouse_press(x=1.1, y=4.2, button=1, modifiers=0)

        mock_pixel_to_char.assert_not_called()
        mock_engine.return_value.grid_click.assert_not_called()
        assert window.game_engine.game_state == NORMAL

    def test_on_mouse_press_in_select_location_state(self, mocker):
        mock_engine = mocker.patch("game_window.GameEngine")
        mock_pixel_to_char = mocker.patch("game_window.pixel_to_char")
        mock_pixel_to_char.return_value = (Mock(), Mock())
        window = MyGame(100, 100, "foo")
        window.game_engine.game_state = SELECT_LOCATION

        window.on_mouse_press(x=1.1, y=4.2, button=1, modifiers=0)

        mock_pixel_to_char.asser_called_once_with(1.1, 4.2)
        mock_engine.return_value.grid_click.assert_called_once_with(
            *mock_pixel_to_char.return_value
        )
        assert window.game_engine.game_state == NORMAL
