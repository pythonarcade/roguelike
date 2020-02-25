from unittest.mock import call

from game_window import main


def test_main(mocker):
    mock_game = mocker.patch("game_window.MyGame")
    mock_width = mocker.patch("game_window.SCREEN_WIDTH")
    mock_height = mocker.patch("game_window.SCREEN_HEIGHT")
    mock_title = mocker.patch("game_window.SCREEN_TITLE")
    mock_run = mocker.patch("game_window.arcade.run")

    main()

    assert mock_game.call_args == call(mock_width, mock_height, mock_title)
    mock_game.return_value.setup.assert_called_once()
    mock_run.assert_called_once()
