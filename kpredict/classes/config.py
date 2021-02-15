import warnings
import re


class ConfigParser:
    """
    A parser for Linux kernel .config files

    ...
    
    Parameters
    ----------
    filename : string
        Path to the .config file

    Methods
    -------
    get_version()
        Return the version for the .config file

    get_activated_options()
        Return a list of activated options (flagged as "y")

    get_n_activated()
        Return the number of activated options
        
    
    """
    def __init__(self, filename):

        version_found = False

        self.activated_options = []

        with open(filename, "r") as f:

            for l in f.readlines():

                # If the line is commented, look for version
                if l.startswith("#"):
                    if not version_found:
                        if m := re.search("\d+\.\d+\.\d+", l):

                            # Get the version
                            self.version = m.group(0)
                            version_found = True

                            # Warn if not "Linux/x86"
                            if not "Linux/x86" in l:
                                warnings.warn(
                                    "Linux/x86 not found in config file. This predictor is made for Linux/x86, any other arch might suffer from high error rate."
                                )

                elif not l == "\n":

                    name, value = l.split("=")

                    # If the value is yes ("y"), add it to the list. All other values are discarded, at least for now
                    if value.strip("\n") == "y":
                        self.activated_options.append(name[7:])

    def get_version(self):
        """Return the version for the .config file
            
        Returns
        -------
        version : string
            The version extracted from the .config file
        """
        return self.version

    def get_activated_options(self):
        """Return a list of activated options
        
        Active options are the one set at "y"
            
        Returns
        -------
        activated_options : list of string
            The activated options extracted from the .config file
        """
        return self.activated_options

    def get_n_activated(self):
        """Return the number of activated options
        
        Active options are the one set at "y"
            
        Returns
        -------
        n_activated : int
            The number of activated options extracted from the .config file
        """
        return len(self.activated_options)
