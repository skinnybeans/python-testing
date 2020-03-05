from tutorial.transaction import process_transaction
import pytest

from unittest.mock import patch
from unittest.mock import Mock
from unittest.mock import MagicMock
from unittest.mock import create_autospec


# The basis of all unit testing in pytest are test functions.
# Functions and  files with a prefix of 'test_'
# are identified as tests.

def test_this_function():
    pass


# To help unit test our code, we often need to mock out dependencies
# Python provides mock objects that can do this for us.
def test_mock():
    mock = Mock()                   # Create a magic mock which is a special type of mock
    mock.do_something_random()      # Call some random method on the mock object

    # Mock objects record information about how they are called
    print('\n do_something_random.call_count: %s' %
          (mock.do_something_random.call_count))
    print(' some_other_function.call_count: %s' %
          (mock.some_other_function.call_count))

    # They also have some builtin functions for asserting
    mock.do_something_random.assert_called_once()

    # Just make sure you get the function right or the mock will treat it like a normal function call
    # Try changing that to .assert_called_once()
    mock.some_other_function.called_once()


def read_file(path):
    ''' function to practice patching with
    '''
    print(f'\n inside read_file trying to open: {path}')
    file = open(path)
    return file.readlines()


''' Write a test that just calls read_file with a junk argument
    it should throw an error
'''


def test_patch_read_files():
    ''' We can make read_files actually point to a mock object
    '''
    patcher = patch('test_mocks.read_file')
    patcher.start()

    # Notice the print statement from read_files function doesn't get called
    result = read_file('some_path')

    print(f'\n result: {result}')

    # patcher must be stopped manually or it will  remain  in place
    # for  subsequent function calls
    patcher.stop()


def test_patch_read_files_builtin():
    ''' Patching the built in read() function can also be done
    '''
    patcher = patch('builtins.open')

    # patcher.start actually returns a mock object to  manipulate
    mock = patcher.start()

    # the read() function  returns a file object
    # so lets mock that as  well
    returned_file_object = Mock(name='file-object')

    # set the return value of the mock when it is called
    mock.return_value = returned_file_object

    # our read_file function calls readlines on the file
    # we can specify what we want readlines to return when called
    returned_file_object.readlines.return_value = 'Hi from the mock'

    # output should show the read_file function getting called now
    result = read_file('some_path')
    print(f' result: {result}')
    print(' mock.call_count: %s' % (mock.call_count))
    print(' returned_file_object.read_lines.call_count: %s' %
          (returned_file_object.readlines.call_count))

    patcher.stop()


def test_patch_check_arguments():
    ''' How do we ensure a function is called with the correct arguments?
    '''
    patcher = patch('test_mocks.read_file')
    mock = patcher.start()

    read_file()  # We'd like this to error, because read_file needs an argument

    # We can interrogate how a function was called
    print(f'\n mock calls: {mock.mock_calls}')

    # If we call it again....
    read_file('path/filename.txt')
    print(f' mock calls: {mock.mock_calls}')

    patcher.stop()


@patch('test_mocks.read_file')
def test_patching_decorator(patched_func):
    ''' Mocking and patching can be done as a decorator
        which is much easier
    '''
    patched_func.return_value = 'Patched me'
    print(read_file('some file'))

    # an easier way of checking a function is called with expected params
    patched_func.assert_called_once_with('some file')

    # no need to clean up when  using a decorator!


@patch('test_mocks.read_file', autospec=True)
def test_patching_with_autospec(patched_func):
    ''' Autospec creates a mock with the same signature as the mocked object
        Autospec gives protection against calling non-existant methods on mocks
    '''
    patched_func.return_value = 'Patched me'

    print(read_file('some file'))   # Try calling read_file without an argument

    # patched_func.what_is_this()   # Try running the following function call with and without autospec set


def my_patching_function(path):
    return 'hello from the custom function'


@patch('test_mocks.read_file', my_patching_function)
def test_explicit_object():
    ''' Patching can be done with another user defined object
        The mock is not passed into the test function as a parameter in this case
    '''
    print('\n %s' % (read_file('some path')))


class Bank():
    ''' Simple class to show patching of class functions
    '''

    def __init__(self):
        self.name = 'I am a bank'
        self.accounts = {}

    def add_account(self, account_name):
        if self.accounts.get(account_name, None) is not None:
            raise Exception('Duplicate account!')

        self.accounts[account_name] = 0  # set balance of accounts to 0

    def get_account_balance(self, account_name):
        return self.accounts[account_name]


@patch('test_mocks.Bank.add_account')
def test_mock_class(add_account):
    ''' Functions in classes can be mocked as well
    '''
    add_account.return_value = 'Yo I added something'
    my_bank = Bank()

    result = my_bank.add_account('myAccount')
    print(f'\n {result}')

    my_bank.add_account.assert_called_once()


def test_class_statically():
    ''' A neat trick to test class functions without instantiating
        an object. Can be useful for objects with lots of internal state
        you want to preconfigure
    '''

    mock_bank = Mock()
    mock_bank.accounts = {}
    mock_bank.accounts['my-account'] = 5

    with pytest.raises(Exception) as ex:       # Expect an exception to be thrown in the following statements
        Bank.add_account(mock_bank, 'my-account')

    print('\n mock bank accounts: %s' % (mock_bank.accounts))   # We still have the account with 5 in it

    print(f' exception info: {ex.value} ')


@patch('tutorial.transaction.trunc')    # As trunc is imported directly into transaction it must be patched there
@patch('time.time')         # The top level time package is imported, so we can patch it like this
def test_patching_location(time, trunc):
    ''' Functions must be patched in the correct scope
        Note the order that multiple patch arguments are passed into the function
    '''

    time.return_value = 0
    trunc.return_value = 5
    print('')
    process_transaction('1234', 500)
