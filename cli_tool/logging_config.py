import logging

def setup_logging(verbose=False, log_file="app.log"):
    """
    Sets up logging to both a file and the console.
    :param verbose: Enable verbose (DEBUG) output if True.
    :param log_file: The file where logs will be written.
    """

    log_level = logging.DEBUG if verbose else logging.INFO
    logger = logging.getLogger()
    logger.setLevel(log_level)


    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    #file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    logger.addHandler(file_handler)
    #console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    logger.addHandler(console_handler)
