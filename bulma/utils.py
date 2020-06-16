def css_class_string(*args):
    """
    Builds a css class string from provided arguments.
    Filters out falsy values and joins truthy into a string
    """
    return ' '.join([arg for arg in args if bool(arg) is True])
