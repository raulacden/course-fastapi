import pytest



def test_equal_or_not_equal():
    assert 1 == 1
    
def test_is_instance():
    assert isinstance(1, int)
    assert not isinstance("1", int)
    
def test_boolean():
    validate = True
    assert validate is True
    assert ('hello' == 'world') is False
    
def test_type():
    assert type(1) == int
    assert type('hello') == str

def test_greater_and_less_than():
    assert 5 > 3
    assert 2 < 4
    assert not (1 > 10)

def test_list():
    my_list = [1, 2, 3]
    assert len(my_list) == 3
    assert my_list[0] == 1
    assert my_list[-1] == 3
    
class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years
        
@pytest.fixture
def default_employee():
    return Student("John", "Doe", "Computer Science", 3)
        
def test_person_initialization(default_employee):
    assert default_employee.first_name == "John", "First name should be 'John'"
    assert default_employee.last_name == "Doe", "Last name should be 'Doe'"
    assert default_employee.major == "Computer Science", "Major should be 'Computer Science'"
    assert default_employee.years == 3, "Years should be 3"