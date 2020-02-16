def my_function():
    """
    Sample function that prints Hi
    """
    print("Hi")


def my_addition_function(a: int, b: int):
    """
        Sample function that adds two integers.

        Our documentation starts off with a one-line sentence. We can follow it up
        with multiple lines that give a more complete description.

        :param int a: First number to add.
        :param int b: Second number to add.

        :return: The two numbers added together.
        :rtype: int
        :raises: None

        Then we can follow it up with an example:

        :Example:

            >>> result = my_addition_function(10, 15)
            >>> print(result)

        .. note::
            This is just a silly example. Don't really use this function to add
            numbers.

    """
    return a + b
