from unittest.mock import call, Mock, sentinel

import pytest

from constants import (
    SCREEN_HEIGHT,
    SCREEN_TITLE,
    SCREEN_WIDTH,
    STATE,
    SPRITE_HEIGHT,
    SPRITE_WIDTH,
    STATUS_PANEL_HEIGHT,
    EXPERIENCE_PER_LEVEL,
)
from game_window import main, MyGame
from themes.current_theme import colors


@pytest.fixture
def mock_arcade(mocker):
    mocker.patch("arcade.Window.__init__")
    return mocker.patch("game_window.arcade")


@pytest.fixture
def mock_draw_text(mock_arcade):
    return mock_arcade.draw_text


@pytest.fixture
def mock_draw_lrtb_rectangle_outline(mock_arcade):
    return mock_arcade.draw_lrtb_rectangle_outline


@pytest.fixture
def mock_get_sprites_at_point(mock_arcade):
    return mock_arcade.get_sprites_at_point


@pytest.fixture
def mock_draw_sprites_and_status_panel(mocker):
    return mocker.patch("game_window.MyGame.draw_sprites_and_status_panel")


@pytest.fixture
def window(mock_arcade):
    return MyGame(100, 100, "foo")


@pytest.fixture
def mock_engine(mocker):
    return mocker.patch("game_window.GameEngine")


@pytest.fixture
def mock_player(mock_engine):
    return mock_engine.return_value.player


@pytest.fixture
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

    def test_draw_hp_and_status_bar_for_fourth_level(
        self, mocker, mock_arcade, mock_draw_text, mock_player, window
    ):
        mock_draw_status_bar = mocker.patch("game_window.draw_status_bar")
        lvl = len(EXPERIENCE_PER_LEVEL)
        mock_player.fighter.level = lvl
        xp = EXPERIENCE_PER_LEVEL[-1] - 1
        mock_player.fighter.current_xp = xp
        mock_hp = mock_player.fighter.hp
        mock_max_hp = mock_player.fighter.max_hp

        window.draw_hp_and_status_bar()

        assert mock_draw_text.call_args_list == [
            call(f"HP: {mock_hp}/{mock_max_hp}", 0, 0, colors["status_panel_text"]),
            call(f"XP: {xp:,}/{xp + 1:,}", 100, 0, (0, 0, 0, 255)),
            call(f"Level: {lvl}", 200, 0, (0, 0, 0, 255)),
        ]
        mock_draw_status_bar.assert_called_once_with(
            65 / 2 + 2, 24, 65, 10, mock_hp, mock_max_hp
        )

    def test_draw_hp_and_status_bar_for_fifth_level(
        self, mocker, mock_arcade, mock_draw_text, mock_player, window
    ):
        mock_draw_status_bar = mocker.patch("game_window.draw_status_bar")
        lvl = len(EXPERIENCE_PER_LEVEL) + 1
        mock_player.fighter.level = lvl
        xp = EXPERIENCE_PER_LEVEL[-1] + 1
        mock_player.fighter.current_xp = xp
        mock_hp = mock_player.fighter.hp
        mock_max_hp = mock_player.fighter.max_hp

        window.draw_hp_and_status_bar()

        assert mock_draw_text.call_args_list == [
            call(f"HP: {mock_hp}/{mock_max_hp}", 0, 0, colors["status_panel_text"]),
            call(f"XP: {xp:,}", 100, 0, (0, 0, 0, 255)),
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
        mock_player,
        window,
    ):
        mock_player.inventory.capacity = 2
        mock_engine.return_value.selected_item = None
        mock_item = Mock()
        mock_item.configure_mock(name="Holy Hand Grenade")
        mock_player.inventory.items = [mock_item, None]
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
        mock_player,
        window,
    ):
        mock_player.inventory.capacity = 2
        mock_engine.return_value.selected_item = 1
        mock_item = Mock()
        mock_item.configure_mock(name="Holy Hand Grenade")
        mock_player.inventory.items = [mock_item, None]
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

    def test_draw_mouse_over_text_when_it_is_there(
        self, mock_arcade, mock_draw_text, mock_engine, window,
    ):
        window.mouse_over_text = "foo"
        mock_mouse_position = (Mock(), Mock())
        window.mouse_position = mock_mouse_position

        window.draw_mouse_over_text()

        mock_arcade.draw_xywh_rectangle_filled.assert_called_once_with(
            *mock_mouse_position, 100, 16, mock_arcade.color.BLACK
        )
        mock_draw_text.assert_called_once_with(
            "foo", *mock_mouse_position, mock_arcade.csscolor.WHITE
        )

    def test_draw_mouse_over_text_when_it_is_not_there(
        self, mock_arcade, mock_draw_text, mock_engine, window,
    ):
        window.mouse_over_text = None

        window.draw_mouse_over_text()

        mock_arcade.draw_xywh_rectangle_filled.assert_not_called()
        mock_draw_text.assert_not_called()

    def test_draw_in_normal_state_does_stuff_in_order(
        self, mocker, mock_arcade, mock_engine, window
    ):
        mock_draw_hp = mocker.patch("game_window.MyGame.draw_hp_and_status_bar")
        mock_draw_inventory = mocker.patch("game_window.MyGame.draw_inventory")
        mock_handle_messages = mocker.patch("game_window.MyGame.handle_messages")
        mock_draw_messages = mocker.patch("game_window.MyGame.draw_messages")
        mock_draw_mouse_over_text = mocker.patch(
            "game_window.MyGame.draw_mouse_over_text"
        )
        ordering_manager = Mock()
        ordering_manager.attach_mock(mock_draw_hp, "draw_hp")
        ordering_manager.attach_mock(mock_draw_inventory, "draw_inventory")
        ordering_manager.attach_mock(mock_handle_messages, "handle_messages")
        ordering_manager.attach_mock(mock_draw_messages, "draw_messages")
        ordering_manager.attach_mock(mock_draw_mouse_over_text, "draw_mouse_over_text")

        window.draw_in_normal_state()

        assert ordering_manager.method_calls == [
            call.draw_hp,
            call.draw_inventory,
            call.handle_messages,
            call.draw_messages,
            call.draw_mouse_over_text,
        ]

    def test_draw_in_select_location_state_with_mouse_position(
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

    def test_draw_in_select_location_state_without_mouse_position(
        self, mock_arcade, mock_pixel_to_char, window
    ):
        window.mouse_position = None

        window.draw_in_select_location_state()

        mock_pixel_to_char.assert_not_called()

    def test_draw_character_screen_without_ability_points(
        self, mock_arcade, mock_draw_text, mock_engine, mock_player, window
    ):
        mock_player.fighter.ability_points = 0

        window.draw_character_screen()

        mock_arcade.draw_xywh_rectangle_filled.assert_called_once_with(
            0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, colors["status_panel_background"],
        )

        character_sheet_elements = [
            "Character Screen",
            f"Attack: {mock_player.fighter.power}",
            f"Defense: {mock_player.fighter.defense}",
            f"HP: {mock_player.fighter.hp} / {mock_player.fighter.max_hp}",
            f"Max Inventory: {mock_player.inventory.capacity}",
            f"Level: {mock_player.fighter.level}",
        ]
        y_values = [
            pytest.approx(x, 0.1) for x in [627, 583.8, 547.8, 511.8, 475.8, 439.8]
        ]
        text_sizes = [24] + [20] * 5

        for call_, element, y_value, text_size in zip(
            mock_draw_text.call_args_list,
            character_sheet_elements,
            y_values,
            text_sizes,
        ):
            assert call_ == call(
                element, 10, y_value, colors["status_panel_text"], text_size
            )

        mock_arcade.SpriteList.return_value.draw.assert_not_called()

    def test_draw_character_screen_with_ability_points(
        self, mock_arcade, mock_player, window
    ):
        mock_player.fighter.ability_points = 1

        window.draw_character_screen()

        mock_arcade.SpriteList.return_value.draw.assert_called_once()

    def test_handle_messages_limits_message_list_to_two(
        self, mock_draw_text, mock_engine, window
    ):
        mock_engine.return_value.messages = ["foo", "bar", "baz"]

        window.handle_messages()

        assert mock_engine.return_value.messages == ["bar", "baz"]

    def test_handle_messages_does_not_touch_two_element_message_list(
        self, mock_draw_text, mock_engine, window
    ):
        mock_engine.return_value.messages = ["foo", "bar"]

        window.handle_messages()

        assert mock_engine.return_value.messages == ["foo", "bar"]

    def test_draw_messages(self, mock_draw_text, mock_engine, window):
        mock_engine.return_value.messages = ["foo", "bar"]

        window.draw_messages()

        assert mock_draw_text.call_args_list == [
            call("foo", 300, 20, colors["status_panel_text"]),
            call("bar", 300, 0, colors["status_panel_text"]),
        ]

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

    def test_handle_character_screen_click_does_nothing_if_character_has_no_ability_points(
        self, mock_get_sprites_at_point, mock_player, window
    ):
        mock_player.fighter.ability_points = 0

        window.handle_character_screen_click(sentinel.x, sentinel.y)

        mock_get_sprites_at_point.assert_not_called()

    def test_handle_character_screen_click_increases_power_if_attack_button_is_clicked(
        self, mock_arcade, mock_get_sprites_at_point, mock_player, window
    ):
        mock_player.fighter.ability_points = 1
        mock_player.fighter.power = 1
        mock_attack = Mock()
        mock_attack.configure_mock(name="attack")
        mock_get_sprites_at_point.return_value = [mock_attack]

        window.handle_character_screen_click(sentinel.x, sentinel.y)

        mock_arcade.get_sprites_at_point.assert_called_once_with(
            (sentinel.x, sentinel.y), mock_arcade.SpriteList.return_value
        )

        assert mock_player.fighter.ability_points == 0
        assert mock_player.fighter.power == 2

    def test_handle_character_screen_click_increases_defense_if_defense_button_is_clicked(
        self, mock_arcade, mock_get_sprites_at_point, mock_player, window
    ):
        mock_player.fighter.ability_points = 1
        mock_player.fighter.defense = 1
        mock_defense = Mock()
        mock_defense.configure_mock(name="defense")
        mock_get_sprites_at_point.return_value = [mock_defense]

        window.handle_character_screen_click(sentinel.x, sentinel.y)

        mock_arcade.get_sprites_at_point.assert_called_once_with(
            (sentinel.x, sentinel.y), mock_arcade.SpriteList.return_value
        )

        assert mock_player.fighter.ability_points == 0
        assert mock_player.fighter.defense == 2

    def test_handle_character_screen_click_increases_max_hp_if_hp_button_is_clicked(
        self, mock_arcade, mock_get_sprites_at_point, mock_player, window
    ):
        mock_player.fighter.ability_points = 1
        mock_player.fighter.max_hp = 5
        mock_hp = Mock()
        mock_hp.configure_mock(name="hp")
        mock_get_sprites_at_point.return_value = [mock_hp]

        window.handle_character_screen_click(sentinel.x, sentinel.y)

        mock_arcade.get_sprites_at_point.assert_called_once_with(
            (sentinel.x, sentinel.y), mock_arcade.SpriteList.return_value
        )

        assert mock_player.fighter.ability_points == 0
        assert mock_player.fighter.max_hp == 10

    def test_handle_character_screen_click_increases_capacity_if_capacity_button_is_clicked(
        self, mock_arcade, mock_get_sprites_at_point, mock_player, window
    ):
        mock_player.fighter.ability_points = 1
        mock_player.inventory.capacity = 1
        mock_capacity = Mock()
        mock_capacity.configure_mock(name="capacity")
        mock_get_sprites_at_point.return_value = [mock_capacity]

        window.handle_character_screen_click(sentinel.x, sentinel.y)

        mock_arcade.get_sprites_at_point.assert_called_once_with(
            (sentinel.x, sentinel.y), mock_arcade.SpriteList.return_value
        )

        assert mock_player.fighter.ability_points == 0
        assert mock_player.inventory.capacity == 2

    def test_on_mouse_press_in_normal_state(
        self, mock_arcade, mock_engine, mock_pixel_to_char, window
    ):
        window.game_engine.game_state = STATE.NORMAL

        window.on_mouse_press(x=1.1, y=4.2, button=1, modifiers=0)

        mock_pixel_to_char.assert_not_called()
        mock_engine.return_value.grid_click.assert_not_called()
        assert window.game_engine.game_state == STATE.NORMAL

    def test_on_mouse_press_in_select_location_state(
        self, mock_arcade, mock_engine, mock_pixel_to_char, window
    ):
        mock_pixel_to_char.return_value = (Mock(), Mock())
        window.game_engine.game_state = STATE.SELECT_LOCATION

        window.on_mouse_press(x=1.1, y=4.2, button=1, modifiers=0)

        mock_pixel_to_char.asser_called_once_with(1.1, 4.2)
        mock_engine.return_value.grid_click.assert_called_once_with(
            *mock_pixel_to_char.return_value
        )

    def test_on_mouse_press_in_character_screen_state(
        self, mocker, mock_arcade, mock_engine, mock_pixel_to_char, window
    ):
        mock_handle_character_screen_click = mocker.patch(
            "game_window.MyGame.handle_character_screen_click"
        )
        window.game_engine.game_state = STATE.CHARACTER_SCREEN

        window.on_mouse_press(x=1.1, y=4.2, button=1, modifiers=0)

        mock_handle_character_screen_click.assert_called_once_with(1.1, 4.2)
        mock_pixel_to_char.assert_not_called()
        mock_engine.return_value.grid_click.assert_not_called()

    def test_on_draw_in_select_location_state(
        self, mocker, mock_arcade, mock_draw_sprites_and_status_panel, window
    ):
        mock_draw_in_select_location_state = mocker.patch(
            "game_window.MyGame.draw_in_select_location_state"
        )
        window.game_engine.game_state = STATE.SELECT_LOCATION

        window.on_draw()

        mock_arcade.start_render.assert_called_once()
        mock_draw_sprites_and_status_panel.assert_called_once()
        mock_draw_in_select_location_state.assert_called_once()

    def test_on_draw_in_normal_state(
        self, mocker, mock_arcade, mock_draw_sprites_and_status_panel, window
    ):
        mock_draw_in_normal_state = mocker.patch(
            "game_window.MyGame.draw_in_normal_state"
        )
        window.game_engine.game_state = STATE.NORMAL

        window.on_draw()

        mock_arcade.start_render.assert_called_once()
        mock_draw_sprites_and_status_panel.assert_called_once()
        mock_draw_in_normal_state.assert_called_once()

    def test_on_draw_in_character_screen_state(
        self, mocker, mock_arcade, mock_draw_sprites_and_status_panel, window
    ):
        mock_draw_character_screen = mocker.patch(
            "game_window.MyGame.draw_character_screen"
        )
        window.game_engine.game_state = STATE.CHARACTER_SCREEN

        window.on_draw()

        mock_arcade.start_render.assert_called_once()
        mock_draw_sprites_and_status_panel.assert_called_once()
        mock_draw_character_screen.assert_called_once()
