import pypi_package_example


def test_my_function(capfd):
    pypi_package_example.my_function()

    out, err = capfd.readouterr()
    assert out == "Hi\n"
