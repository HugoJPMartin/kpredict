import pandas as pd
from sklearn.metrics import make_scorer


def mape(y_true, y_pred):
    """Return the Mean Absolute Percentage Error

    Parameters
    ----------
    y_true : array-like of shape (n_samples,) or (n_samples, n_outputs)
        Ground truth (correct) target values.

    y_pred : array-like of shape (n_samples,) or (n_samples, n_outputs)
        Estimated target values.
    """
    return pd.Series(((y_pred - y_true) / y_true).abs() * 100).mean()


score_mape = make_scorer(mape, greater_is_better=False)


def sanitize_dataframe(x):
    """Check if x is a Pandas DataFrame or Series. Transform to DataFrame if x is a Series.

    Parameters
    ----------
    x : anything
        Value to be checked

    Raises
    ------
    Exception
        If x is not a Pandas Series or DataFrame
    """
    if not isinstance(x, pd.Series) and not isinstance(x, pd.DataFrame):
        raise Exception("The variable needs to be a pandas Series or DataFrame")

    if isinstance(x, pd.Series):
        x = pd.DataFrame(x).T
    return x


def formating_size(size):
    """Return an int formatted to human readable size

    Taken from here : https://stackoverflow.com/a/1094933

    Parameters
    ----------
    size : int
        Value to be formatted
    """
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(size) < 1024.0:
            return "%3.1f%s%s" % (size, unit, "B")
        size /= 1024.0
    return "%.1f%s%s" % (size, "Yi", "B")
