

def test_version(config_1, config_2):
    assert config_1.get_version() == "5.8.0"
    assert config_2.get_version() == "5.8.1"
    
def test_activated_options(config_1, config_2):
    assert not "DEBUG_INFO" in config_1.get_activated_options()
    assert "DEBUG_INFO" in config_2.get_activated_options()
    
def test_n_activated_options(config_1, config_2):
    assert config_1.get_n_activated() + 1 == config_2.get_n_activated()