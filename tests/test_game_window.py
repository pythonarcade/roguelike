from unittest.mock import call, Mock

import pytest

from constants import (
    NORMAL,
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    SELECT_LOCATION,
    SPRITE_HEIGHT,
    SPRITE_WIDTH,
    STATUS_PANEL_HEIGHT,
    EXPERIENCE_PER_LEVEL,
)
from game_window import main, MyGame
from themes.current_theme import colors


@pytest.fixture()
def mock_arcade(mocker):
    mocker.patch("arcade.Window.__init__")
    return mocker.patch("game_window.arcade")


@pytest.fixture()
def mock_draw_text(mock_arcade):
    return mock_arcade.draw_text


@pytest.fixture()
def mock_draw_lrtb_rectangle_outline(mock_arcade):
    return mock_arcade.draw_lrtb_rectangle_outline


@pytest.fixture()
def window(mock_arcade):
    return MyGame(100, 100, "foo")


@pytest.fixture()
def mock_engine(mocker):
    return mocker.patch("game_window.GameEngine")


@pytest.fixture()
def mock_pixel_to_char(mocker):
    return mocker.patch("game_window.pixel_to_char")


def test_main(mocker, mock_arcade):
    mock_game = mocker.patch("game_window.MyGame")

    main()

    mock_game.assert_called_once_with(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    mock_game.return_value.setup.assert_called_once()
    mock_arcade.run.assert_called_once()


class TestMyGame:
    def test_init(self, mock_arcade, mock_engine, window):
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
        assert window.character_sheet_buttons == mock_arcade.SpriteList.return_value
        mock_arcade.set_background_color.assert_called_once_with((255, 255, 255))

    def test_setup(self, mock_arcade, mock_engine, window):
        mock_sprites = [Mock() for _ in range(4)]
        mock_arcade.Sprite.side_effect = mock_sprites

        window.setup()

        mock_engine.return_value.setup.assert_called_once()
        sprite_names = ["attack", "defense", "hp", "capacity"]
        centre_ys = [602, 565, 528, 491]
        for mock_sprite, name, centre_y in zip(mock_sprites, sprite_names, centre_ys):
            assert mock_sprite.name == name
            assert mock_sprite.center_x == 200
            assert mock_sprite.center_y == centre_y
        assert mock_arcade.SpriteList.return_value.append.call_args_list == [
            call(mock_sprite) for mock_sprite in mock_sprites
        ]

    def test_on_mouse_press_in_normal_state(
        self, mock_arcade, mock_engine, mock_pixel_to_char, window
    ):
        window.game_engine.game_state = NORMAL

        window.on_mouse_press(x=1.1, y=4.2, button=1, modifiers=0)

        mock_pixel_to_char.assert_not_called()
        mock_engine.return_value.grid_click.assert_not_called()
        assert window.game_engine.game_state == NORMAL

    def test_on_mouse_press_in_select_location_state(
        self, mock_arcade, mock_engine, mock_pixel_to_char, window
    ):
        mock_pixel_to_char.return_value = (Mock(), Mock())
        window.game_engine.game_state = SELECT_LOCATION

        window.on_mouse_press(x=1.1, y=4.2, button=1, modifiers=0)

        mock_pixel_to_char.asser_called_once_with(1.1, 4.2)
        mock_engine.return_value.grid_click.assert_called_once_with(
            *mock_pixel_to_char.return_value
        )

    def test_draw_sprites_and_status_panel(
        self, mocker, mock_arcade, mock_engine, window
    ):
        mock_gl = mocker.patch("game_window.gl")

        window.draw_sprites_and_status_panel()

        mock_engine.return_value.cur_level.dungeon_sprites.draw.assert_called_once_with(
            filter=mock_gl.GL_NEAREST
        )
        mock_engine.return_value.cur_level.entities.draw.assert_called_once_with(
            filter=mock_gl.GL_NEAREST
        )
        mock_engine.return_value.cur_level.creatures.draw.assert_called_once_with(
            filter=mock_gl.GL_NEAREST
        )
        mock_engine.return_value.characters.draw.assert_called_once_with(
            filter=mock_gl.GL_NEAREST
        )
        mock_arcade.draw_xywh_rectangle_filled.assert_called_once_with(
            0, 0, SCREEN_WIDTH, STATUS_PANEL_HEIGHT, colors["status_panel_background"],
        )

    def test_on_draw_in_normal_state(self, mocker, mock_arcade, window):
        mock_draw_sprites_and_status_panel = mocker.patch(
            "game_window.MyGame.draw_sprites_and_status_panel"
        )
        mock_draw_in_normal_state = mocker.patch(
            "game_window.MyGame.draw_in_normal_state"
        )
        window.game_engine.game_state = NORMAL

        window.on_draw()

        mock_arcade.start_render.assert_called_once()
        mock_draw_sprites_and_status_panel.assert_called_once()
        mock_draw_in_normal_state.assert_called_once()

    def test_on_draw_in_select_location_state(self, mocker, mock_arcade, window):
        mock_draw_sprites_and_status_panel = mocker.patch(
            "game_window.MyGame.draw_sprites_and_status_panel"
        )
        mock_draw_in_select_location_state = mocker.patch(
            "game_window.MyGame.draw_in_select_location_state"
        )
        window.game_engine.game_state = SELECT_LOCATION

        window.on_draw()

        mock_arcade.start_render.assert_called_once()
        mock_draw_sprites_and_status_panel.assert_called_once()
        mock_draw_in_select_location_state.assert_called_once()

    def test_draw_hp_and_status_bar_for_fifth_level(
        self, mocker, mock_arcade, mock_draw_text, mock_engine, window
    ):
        mock_draw_status_bar = mocker.patch("game_window.draw_status_bar")
        lvl = len(EXPERIENCE_PER_LEVEL) + 1
        mock_engine.return_value.player.fighter.level = lvl
        xp = EXPERIENCE_PER_LEVEL[-1] + 1
        mock_engine.return_value.player.fighter.current_xp = xp
        mock_hp = mock_engine.return_value.player.fighter.hp
        mock_max_hp = mock_engine.return_value.player.fighter.max_hp

        window.draw_hp_and_status_bar()

        assert mock_draw_text.call_args_list == [
            call(f"HP: {mock_hp}/{mock_max_hp}", 0, 0, colors["status_panel_text"]),
            call(f"XP: {xp:,}", 100, 0, (0, 0, 0, 255)),
            call(f"Level: {lvl}", 200, 0, (0, 0, 0, 255)),
        ]
        mock_draw_status_bar.assert_called_once_with(
            65 / 2 + 2, 24, 65, 10, mock_hp, mock_max_hp
        )

    def test_draw_hp_and_status_bar_for_fourth_level(
        self, mocker, mock_arcade, mock_draw_text, mock_engine, window
    ):
        mock_draw_status_bar = mocker.patch("game_window.draw_status_bar")
        lvl = len(EXPERIENCE_PER_LEVEL)
        mock_engine.return_value.player.fighter.level = lvl
        xp = EXPERIENCE_PER_LEVEL[-1] - 1
        mock_engine.return_value.player.fighter.current_xp = xp
        mock_hp = mock_engine.return_value.player.fighter.hp
        mock_max_hp = mock_engine.return_value.player.fighter.max_hp

        window.draw_hp_and_status_bar()

        assert mock_draw_text.call_args_list == [
            call(f"HP: {mock_hp}/{mock_max_hp}", 0, 0, colors["status_panel_text"]),
            call(f"XP: {xp:,}/{xp + 1:,}", 100, 0, (0, 0, 0, 255)),
            call(f"Level: {lvl}", 200, 0, (0, 0, 0, 255)),
        ]
        mock_draw_status_bar.assert_called_once_with(
            65 / 2 + 2, 24, 65, 10, mock_hp, mock_max_hp
        )

    def test_draw_inventory_no_selected_item(
        self,
        mock_arcade,
        mock_draw_lrtb_rectangle_outline,
        mock_draw_text,
        mock_engine,
        window,
    ):
        mock_engine.return_value.player.inventory.capacity = 2
        mock_engine.return_value.selected_item = None
        mock_item = Mock()
        mock_item.configure_mock(name="Holy Hand Grenade")
        mock_engine.return_value.player.inventory.items = [mock_item, None]
        window.draw_inventory()

        assert mock_draw_text.call_args_list == [
            call("1: Holy Hand Grenade", 0.0, 40, (0, 0, 0, 255)),
            call("2: ", 480.0, 40, (0, 0, 0, 255)),
        ]
        mock_draw_lrtb_rectangle_outline.assert_not_called()

    def test_draw_inventory_with_selected_item(
        self,
        mock_arcade,
        mock_draw_lrtb_rectangle_outline,
        mock_draw_text,
        mock_engine,
        window,
    ):
        mock_engine.return_value.player.inventory.capacity = 2
        mock_engine.return_value.selected_item = 1
        mock_item = Mock()
        mock_item.configure_mock(name="Holy Hand Grenade")
        mock_engine.return_value.player.inventory.items = [mock_item, None]
        ordering_manager = Mock()
        ordering_manager.attach_mock(mock_draw_text, "draw_text")
        ordering_manager.attach_mock(
            mock_draw_lrtb_rectangle_outline, "draw_lrtb_rectangle_outline"
        )

        window.draw_inventory()

        assert ordering_manager.method_calls == [
            call.draw_text("1: Holy Hand Grenade", 0.0, 40, (0, 0, 0, 255)),
            call.draw_lrtb_rectangle_outline(
                479.0, 955.0, 60, 40, mock_arcade.color.BLACK, 2
            ),
            call.draw_text("2: ", 480.0, 40, (0, 0, 0, 255)),
        ]

    def test_draw_in_normal_state(self, mocker, mock_arcade, mock_engine, window):
        mock_draw_hp = mocker.patch("game_window.MyGame.draw_hp_and_status_bar")
        mock_draw_inventory = mocker.patch("game_window.MyGame.draw_inventory")
        mock_handle_and_draw_messages = mocker.patch(
            "game_window.MyGame.handle_and_draw_messages"
        )
        mock_draw_mouse_over_text = mocker.patch(
            "game_window.MyGame.draw_mouse_over_text"
        )

        window.draw_in_normal_state()

        mock_draw_hp.assert_called_once()
        mock_draw_inventory.assert_called_once()
        mock_handle_and_draw_messages.assert_called_once()
        mock_draw_mouse_over_text.assert_called_once()

    def test_draw_in_select_location_state(
        self, mocker, mock_arcade, mock_pixel_to_char, window
    ):
        mock_grid_coordinates = Mock(), Mock()
        mock_pixel_to_char.return_value = mock_grid_coordinates
        mock_char_to_pixel = mocker.patch("game_window.char_to_pixel")
        mock_center_coordinates = Mock(), Mock()
        mock_char_to_pixel.return_value = mock_center_coordinates
        mock_mouse_position = Mock(), Mock()
        window.mouse_position = mock_mouse_position

        window.draw_in_select_location_state()

        mock_pixel_to_char.assert_called_once_with(*mock_mouse_position)
        mock_char_to_pixel.assert_called_once_with(*mock_grid_coordinates)
        mock_arcade.draw_rectangle_outline.assert_called_once_with(
            mock_center_coordinates[0],
            mock_center_coordinates[1],
            SPRITE_WIDTH,
            SPRITE_HEIGHT,
            mock_arcade.color.LIGHT_BLUE,
            2,
        )
