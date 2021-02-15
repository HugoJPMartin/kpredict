import kpredict
import pytest
import numpy as np

def test_match_version(config_1, config_2):
    assert kpredict.match_version(config_1.get_version()) == "5.8.0"
    assert kpredict.match_version(config_2.get_version()) == "5.8.0"
    
    
def test_match_version_warning(config_2, recwarn):
    kpredict.match_version(config_2.get_version())

    assert len(recwarn) == 1

def test_match_version_no_warning(config_1, recwarn):
    kpredict.match_version(config_1.get_version())

    assert len(recwarn) == 0
    
    
def test_get_features(config_1, config_2):
    
    features_1 = kpredict.get_features_from_config(config_1, config_1.get_version())
    
    assert "active_options" in features_1
    assert features_1["DEBUG_INFO"] == 0
    
    features_2 = kpredict.get_features_from_config(config_2, kpredict.match_version(config_2.get_version()))
    
    assert "active_options" in features_2
    assert features_2["DEBUG_INFO"] == 1
    
    
def test_predict(config_1, config_2):
    
    features_1 = kpredict.get_features_from_config(config_1, kpredict.match_version(config_1.get_version()))
    features_2 = kpredict.get_features_from_config(config_2, kpredict.match_version(config_2.get_version()))
    
    value_1 = kpredict.predict(features_1, kpredict.match_version(config_1.get_version()))
    value_2 = kpredict.predict(features_2, kpredict.match_version(config_2.get_version()))
    
    assert type(value_1) == np.float64
    assert type(value_2) == np.float64
    assert value_1 < value_2
    
def test_predict_from_file(config_file):
    value, formated_value = kpredict.predict_from_file(config_file)
    
    assert type(value) == np.float64
    assert type(formated_value) == str
    
def test_unsupported_version(config_3):
    with pytest.raises(kpredict.exceptions.VersionNotSupported):
        kpredict.match_version(config_3.get_version())