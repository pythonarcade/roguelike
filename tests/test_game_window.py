from unittest.mock import call, Mock

from constants import (
    NORMAL,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SELECT_LOCATION,
    STATUS_PANEL_HEIGHT,
    colors,
)
from game_window import main, MyGame


def test_main(mocker):
    mock_game = mocker.patch("game_window.MyGame")
    mock_run = mocker.patch("game_window.arcade.run")

    main()

    mock_game.assert_called_once_with(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
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
        window.close()

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

    def test_on_draw_in_normal_state(self, mocker):
        mock_arcade = mocker.patch("game_window.arcade")
        mock_gl = mocker.patch("game_window.gl")
        mock_engine = mocker.patch("game_window.GameEngine")
        mock_draw_in_normal_state = mocker.patch(
            "game_window.MyGame.draw_in_normal_state"
        )
        window = MyGame(100, 100, "foo")
        window.game_engine.game_state = NORMAL

        window.on_draw()

        mock_arcade.start_render.assert_called_once()
        mock_engine.return_value.dungeon_sprites.draw.assert_called_once_with(
            filter=mock_gl.GL_NEAREST
        )
        mock_engine.return_value.entities.draw.assert_called_once_with(
            filter=mock_gl.GL_NEAREST
        )
        mock_engine.return_value.characters.draw.assert_called_once_with(
            filter=mock_gl.GL_NEAREST
        )
        mock_arcade.draw_xywh_rectangle_filled.assert_called_once_with(
            0, 0, SCREEN_WIDTH, STATUS_PANEL_HEIGHT, colors["status_panel_background"],
        )
        mock_draw_in_normal_state.assert_called_once()

    def test_on_draw_in_select_location_state(self, mocker):
        mock_arcade = mocker.patch("game_window.arcade")
        mock_gl = mocker.patch("game_window.gl")
        mock_engine = mocker.patch("game_window.GameEngine")
        mock_draw_in_select_location_state = mocker.patch(
            "game_window.MyGame.draw_in_select_location_state"
        )
        window = MyGame(100, 100, "foo")
        window.game_engine.game_state = SELECT_LOCATION

        window.on_draw()

        mock_arcade.start_render.assert_called_once()
        mock_engine.return_value.dungeon_sprites.draw.assert_called_once_with(
            filter=mock_gl.GL_NEAREST
        )
        mock_engine.return_value.entities.draw.assert_called_once_with(
            filter=mock_gl.GL_NEAREST
        )
        mock_engine.return_value.characters.draw.assert_called_once_with(
            filter=mock_gl.GL_NEAREST
        )
        mock_arcade.draw_xywh_rectangle_filled.assert_called_once_with(
            0, 0, SCREEN_WIDTH, STATUS_PANEL_HEIGHT, colors["status_panel_background"],
        )
        mock_draw_in_select_location_state.assert_called_once()

    def test_draw_in_normal_state_with_mouse_not_over_text_no_selected_item_and_no_messages_in_queue(
        self, mocker
    ):
        mock_arcade = mocker.patch("game_window.arcade")
        mock_draw_status_bar = mocker.patch("game_window.draw_status_bar")
        mock_engine = mocker.patch("game_window.GameEngine")
        mock_engine.return_value.player.inventory.capacity = 2
        mock_engine.return_value.selected_item = None
        mock_hp = mock_engine.return_value.player.fighter.hp
        mock_max_hp = mock_engine.return_value.player.fighter.max_hp
        mock_item = Mock()
        mock_item.configure_mock(name="Holy Hand Grenade")
        mock_engine.return_value.player.inventory.items = [mock_item, None]
        window = MyGame(100, 100, "foo")

        window.draw_in_normal_state()

        assert mock_arcade.draw_text.call_args_list == [
            call(f"HP: {mock_hp}/{mock_max_hp}", 0, 0, colors["status_panel_text"],),
            call("1: Holy Hand Grenade", 0.0, 40, (0, 0, 0, 255)),
            call("2: ", 360.0, 40, (0, 0, 0, 255)),
        ]
        mock_draw_status_bar.assert_called_once_with(
            65 / 2 + 2, 24, 65, 10, mock_hp, mock_max_hp
        )
        mock_arcade.draw_lrtb_rectangle_outline.assert_not_called()
