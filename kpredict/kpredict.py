import warnings
import json
import os

import pandas as pd
from joblib import load

from .exceptions import VersionNotSupported
from .classes.config import ConfigParser
from .helpers import formating_size

available_versions = {
    "4.13.3": {
        "model": "model_413.joblib",
        "options_list": "tristate_options_413.json",
    },
    "4.15.0": {
        "model": "model_415.joblib",
        "options_list": "tristate_options_415.json",
    },
    "4.20.0": {
        "model": "model_420.joblib",
        "options_list": "tristate_options_420.json",
    },
    "5.0.0": {"model": "model_500.joblib", "options_list": "tristate_options_500.json"},
    "5.4.0": {"model": "model_504.joblib", "options_list": "tristate_options_504.json"},
    "5.7.0": {"model": "model_507.joblib", "options_list": "tristate_options_507.json"},
    "5.8.0": {"model": "model_508.joblib", "options_list": "tristate_options_508.json"},
}


def match_version(version):
    """
    Return either the version given if supported, or the corresponding major version supported.


    Parameters
    ----------
    version : str
        The version given

    Raises
    ------
    VersionNotSupported
        If the version given has no model available.
            
    Returns
    -------
    version : string
        The closest version supported
    """

    if version in available_versions:
        return version

    matching_major_version = [i for i in available_versions.keys() if i.startswith(".".join(version.split(".")[:-1]))]

    if len(matching_major_version) == 0:
        raise VersionNotSupported

    warnings.warn(
        "The selected model is not from the exact same version, only the same major version. It could lead to high error rate."
    )
    return matching_major_version[-1]


def get_features_from_config(cp, version):
    """Return the features given a ConfigParser and a version

    Parameters
    ----------
    cp : ConfigParser
        ConfigParser instance extracting information from .config file

    version : str
        The version given
        
    Returns
    -------
    features : dict
        Features and their encoded value
    """

    with open(
        os.path.join(
            os.path.dirname(__file__),
            "data",
            available_versions[version]["options_list"],
        ),
        "r",
    ) as f:
        options = json.load(f)

    features = {i: 0 for i in options}

    for i in cp.get_activated_options():
        features[i] = 1

    features["active_options"] = cp.get_n_activated()

    return features


def get_model(version):
    """Return the model corresponding to the version

    Parameters
    ----------
    version : str
        The version given
        
    Returns
    -------
    model : Model
        The loaded model given the version
    """
    return load(
        os.path.join(
            os.path.dirname(__file__), "models", available_versions[version]["model"]
        )
    )


def predict(features, version):
    """Return a predicted kernel size given a list of features and a version

    Parameters
    ----------
    features : dict
         Dict containing features name and value

    version : str
        The version given
        
    Returns
    -------
    predicted_kernel_size : float
        The predicted kernel size
    """
    s = pd.Series(features)

    model = get_model(version)

    return model.predict(s)[0]


def predict_from_file(filename, version=None):
    """Return a predicted kernel size given a .config file

    The returned tuple contains the value and the formated value

    Parameters
    ----------
    filename : str
         Path to the Linux kernel .config file

    version : str
        The version given
        
    Returns
    -------
    tuple(value, formatted_value) : tuple(float, string)
        Predicted kernel size and its formatted equivalent
    """

    cp = ConfigParser(filename)

    if version is None:
        version = match_version(cp.get_version())

    features = get_features_from_config(cp, version)

    value = predict(features, version)

    return value, formating_size(value)
