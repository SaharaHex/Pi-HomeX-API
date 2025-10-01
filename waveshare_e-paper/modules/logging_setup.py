import logging
import os

def setup_logging(to_console=True, log_filename='dashboard.log', level=logging.INFO):
    """
    Configures logging to either console or a log file one directory above this module.

    Parameters:
        to_console (bool): If True, logs to console. If False, logs to file.
        log_filename (str): Name of the log file.
        level (int): Logging level.
    """
    handlers = []

    if to_console:
        handlers.append(logging.StreamHandler())
    else:
        # Get parent directory of the 'modules' folder
        parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        log_path = os.path.join(parent_dir, log_filename)
        handlers.append(logging.FileHandler(log_path))

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=handlers
    )
