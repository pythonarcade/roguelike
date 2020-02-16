import pypi_package_example


def test_my_addition_function():
    assert pypi_package_example.my_addition_function(5, 10) == 15
    assert pypi_package_example.my_addition_function(15, 10) == 25
    assert pypi_package_example.my_addition_function(-10, 10) == 0
