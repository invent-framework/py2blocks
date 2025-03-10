import py2blocks


def setup():
    # Ensure that the user-defined functions are empty before each test.
    py2blocks.USER_DEFINED_FUNCTIONS = {}
