# -*- coding: utf-8 -*-
"""The test script for the processor module
"""
from mnutree.processor import find
from mnutree.processor import process
from mnutree.processor import parent_id
from mnutree.processor import normallize
from mnutree.processor import create_menu

__author__ = "Gaurav J"
__copyright__ = "Mastek India Pvt. Ltd"
__license__ = "MIT"

def test_normallize():
    """The method to check if comma within quotes is replaced
        with unicode character \u02cc. This will ensure that line
        is properly split by comma. The \u02cc charcter is again replaced
        with comma after the line split. This ensures that data is not tampered
        in any way. The replacement is hard to detect by human eye, so any logs etc
        will not look bad.
    """
    line = "\"PIZZA, PASTA & GARLIC BREAD\",178985,https://groceries"
    corrected_line = normallize(line)
    assert corrected_line is not None
    assert corrected_line == "PIZZAˌ PASTA & GARLIC BREAD,178985,https://groceries"

def test_process(cmd_arg):
    """The test method for processor.process method
    """
    file_path, menu_list = process(cmd_arg)
    assert file_path.name == "data.json"
    assert file_path.parent.name == "tests"
    assert menu_list is not None

def test_create_menu(menu_item):
    """The method to create json hiearchical menu from the
        given list of items as extracted from a line in the given csv file
    """
    menu_list = []
    object_cache = {}

    list_of_items_in_line = [
        "https://groceries.morrisons.com/browse",
        menu_item.get('label'),
        menu_item.get('id'),
        menu_item.get('link')
    ]

    create_menu(list_of_items_in_line, menu_list, object_cache)

    assert menu_list is not None
    assert object_cache is not None
    assert menu_list == [{'label': 'none', 'id': '178969', 'link': 'none', 'children': [menu_item]}]
    assert object_cache == {menu_item.get('id'): menu_item,
                            '178969': {'label': 'none', 'id': '178969', 'link': 'none',
                            'children': [menu_item]}}

def test_parent_id(menu_item):
    """The method to check if parent id is being properly
       extracted from the link. The parent id is avilable
       at second last position in the link
    """
    pid = parent_id(menu_item, "link", "id")
    assert pid is not None
    assert pid == '178969'

def test_find(menu_item):
    """The method to find an item(dict) in the list
       of given dict objects
    """
    menu_list = [{'label': 'none', 'id': '178969', 'link': 'none', 'children': [menu_item]}]
    parent = find('178969', menu_list)
    assert parent is not None
    assert parent == {'label': 'none', 'id': '178969', 'link': 'none', 'children': [menu_item]}

    child = find('178975', menu_list)
    assert child is not None
    assert child == menu_item
