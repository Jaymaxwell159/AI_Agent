def print_verbose_content(message, verbose=False, verbose_message=None):
    """
    Print messages based on verbose mode.
    
    Args:
        message (str): The default message to print
        verbose (bool): Whether to print in verbose mode
        verbose_message (str, optional): The verbose message to print. If None, uses message
    """
    if verbose:
        print(verbose_message if verbose_message is not None else message)
    else:
        print(message)
