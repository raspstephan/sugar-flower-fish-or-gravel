def load_configuration(configuration_file=None):
    """
    Loads the configuration file CONFIG.ini.
    1. If provided load configuration_file
    2. Attempt to load from home directory
    3. Attempt to load from relative path inside git structure

    Usage:
        To load the configuration within other scripts
        the following lines make sure, that no
        absolute path to this module have to be given.
        
        from subprocess import check_output
        git_rep_path = check_output(["git", "rev-parse", "--show-toplevel"]).strip().decode()
        sys.path.append(git_rep_path+'/config')
        from load_config import load_configuration
        CONFIG=load_configuration()

    Args:
        configuration_file: optional: complete path to the configuration file.

    Returns:
        instance of ConfigParser class with extended interpolation.
    """
    import os
    import configparser

    dir_path = os.path.dirname(os.path.realpath(__file__))
    ini_path = dir_path.split("cloud-classification")[0] + "cloud-classification/config/CONFIG.ini"
    if not isinstance(configuration_file, str):
        if os.path.isfile(os.getenv("HOME")+"/CONFIG.ini"):
            configuration_file = os.getenv("HOME")+"/CONFIG.ini"
        elif os.path.isfile(ini_path):
            configuration_file = ini_path

        if not os.path.isfile(configuration_file):
            raise FileNotFoundError(
                "No Configuration File 'PATH.ini' found. Please create one in your home directory "
                "or provide the path via the argument parsing -c.")
        else:
            print("Using configuration file: %s" % configuration_file)

    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read(configuration_file)
    return config
