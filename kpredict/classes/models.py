from sklearn.base import RegressorMixin
from ..helpers import mape, sanitize_dataframe


class Model:
    """
    A wrapper around Regressor models from scikit-learn.

    ...
    
    Parameters
    ----------
    sklearn_algorithm : any scikit-learn Regressor
        Class of the scikit-learn algorithm to build the model
    hyperparameters : dict
        Dict of hyperparameters to give to the algorithm

    Methods
    -------
    fit(X_train, y_train)
        Call the algorithm fit methods to build the model, and saves the features list.

    predict(X)
        Align the features and return the predicted values from X

    test(X_test, y_test)
        Return the Mean Absolute Percentage Error given a test set
    """

    def __init__(self, sklearn_algorithm, hyperparameters):

        if not issubclass(sklearn_algorithm, RegressorMixin):
            raise Exception("The algorithm needs to be a sklearn regressor")

        self._algo = sklearn_algorithm
        self._model = sklearn_algorithm(**hyperparameters)

        self._features = None
        self._accuracy = None

    def fit(self, X_train, y_train, **kwargs):
        """Call the algorithm fit methods to build the model, and saves the features list.

        Parameters
        ----------
        X_train : Pandas DataFrame
            The training input samples.

        y_train : Pandas Series
            The target values (real numbers).
        """

        self._features = X_train.columns.values
        self._model.fit(X_train, y_train, **kwargs)

    def predict(self, X, **kwargs):
        """Align the features and return the predicted values from X

        Feature alignment is made but ignoring previously unknown features and set absent features at 1.

        Parameters
        ----------
        X : Pandas DataFrame or Pandas Series
            The training input samples.
            
        Returns
        -------
        y_predict : Pandas Series
            The predicted values from the model
        """

        X = sanitize_dataframe(X)

        for c in set(self._features).difference(set(X.columns.values)):
            X = X.assign(**{c: 1})

        return self._model.predict(X[self._features], **kwargs)

    def test(self, X_test, y_test, **kwargs):
        """Return the Mean Absolute Percentage Error given a test set

        Parameters
        ----------
        X_test : Pandas DataFrame
            The testing input samples.

        y_test : Pandas Series
            The target values (real numbers).
            
        Returns
        -------
        mape : float
            The MAPE value over the testing values
        """
        y_pred = self.predict(X_test)
        self._accuracy = mape(y_test, y_pred)
        return self._accuracy


class ShiftingModel(Model):
    """
    A wrapper around Regressor models from scikit-learn; allow transfer by model shifting.

    ...
    Parameters
    ----------
    sklearn_algorithm : any scikit-learn Regressor
        Class of the scikit-learn algorithm to build the model
    hyperparameters : dict
        Dict of hyperparameters to give to the algorithm
    base_model: Model
        The base model for the model shifting
    Methods
    -------
    fit(X_train, y_train)
        Call the algorithm fit methods to build the model, and saves the features list.

    predict(X)
        Align the features and return the predicted values from X

    test(X_test, y_test)
        Return the Mean Absolute Percentage Error given a test set
    """

    def __init__(self, sklearn_algorithm, hyperparameters, base_model: Model):

        super().__init__(sklearn_algorithm, hyperparameters)

        self._base_model = base_model

    def fit(self, X_train, y_train, **kwargs):
        """Call the algorithm fit methods to build the model, and saves the features list.

        Also takes care of getting the prediction from the base model.

        Parameters
        ----------
        X_train : Pandas DataFrame
            The training input samples.

        y_train : Pandas Series
            The target values (real numbers).
        """
        X_train["label_prediction"] = self._base_model.predict(X_train)

        self._features = X_train.columns.values
        self._model.fit(X_train, y_train, **kwargs)

    def predict(self, X, **kwargs):
        """Align the features and return the predicted values from X

        Feature alignment is made but ignoring previously unknown features and set absent features at 1.
        Also takes care of getting the prediction from the base model.

        Parameters
        ----------
        X : Pandas DataFrame or Pandas Series
            The training input samples.
            
        Returns
        -------
        y_predict : Pandas Series
            The predicted values from the model
        """

        X = sanitize_dataframe(X)

        for c in set(self._features).difference(set(X.columns.values)):
            X = X.assign(**{c: 1})

        X["label_prediction"] = self._base_model.predict(X)

        return self._model.predict(X[self._features], **kwargs)
