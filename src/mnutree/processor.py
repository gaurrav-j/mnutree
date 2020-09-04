# -*- coding: utf-8 -*-
"""A module to read the csv file containig the menu data.
   The module than form the parent child relation ship in csv data.
   The module gives a list containing dictoniaries. The dictonry
   follow the parent child structure as derived from the csv menu file.
"""
import re
from pathlib import Path
from argparse import Namespace
from typing import List, Tuple, Dict, Any

from mnutree import info

__author__ = "Gaurav J"
__copyright__ = "Mastek India Pvt. Ltd"
__license__ = "MIT"

KEYS = "label", "id", "link"

def normallize(line: str) -> str:
    """The function currently removes extra quotes and replaces comma.
       The function uses regex to find a comma in quotes.
       The extra comma in csv file is an issue as it prevents
       the separation of the coloums.

       Parameters
       ----------
       line : string
        the line as read from the csv file
    """
    quotes: List = re.findall(r'"(.*?)"', line)
    if len(quotes) != 0:
        for quote in quotes:
            line = line.replace(quote, quote.replace(",", "\u02cc"))
            line = line.replace("\"", "")

    info("normallize: {}", line, debug=True)
    return line


def process(args: Namespace) -> Tuple[Path, List]:
    """The main method doing heavy lifting.
       The method to process the csv file
       to the JSON tree structure as required

       Parameters
       ----------
       args : dictionary
        the csv file path from command line

       Returns
       -------
       tuple
        the file path & parent-child dictionary of menus
    """
    if args.csv_file.find("/") > -1:
        file_path: Path = Path(args.csv_file)
    else:
        file_path = Path("./"+args.csv_file)

    menu_list: List = []
    object_cache: Dict[str, Any] = {}

    with open(file_path, "r") as file:
        line_count: int = 0
        for line in file:
            line = line.rstrip()
            if line_count == 0:
                line_count += 1
                info("process:header: {} ", line, debug=True)
            else:
                line_count += 1
                line = normallize(line)
                list_of_items_in_line: List = [word for word in line.split(',')
                    if word and word != "\n"]
                len_list_of_items_in_line: int = len(list_of_items_in_line)
                info("process: {} . len --> {}, list_of_items_in_line --> {}",
                    line_count, len_list_of_items_in_line, list_of_items_in_line, debug=True)
                if len_list_of_items_in_line != 0:
                    create_menu(list_of_items_in_line, menu_list, object_cache)

    info("process: The file path is {} ", file_path.with_suffix('.json'))

    return file_path.with_suffix('.json'), menu_list


def create_menu(list_of_items_in_line: List, menu_list: List, object_cache: Dict[str, Any]):
    """The method implementing the algo.
       The method takes the list of list_of_items_in_line (menu items)
       and transforms them into lists & dictionary. It
       then insert the childeren at appropriate places.

       Parameters
       ----------
       list_of_items_in_line : list
        the list of menu item as obtained from single line of csv file

       menu_list : list
        the main root list which will finally have json replica

       object_cache : dictionary
        the dictionary to hold the menu items
    """
    info("create_menu: {}", menu_list, debug=True)

    list_of_items_in_line.pop(0)
    item_to_group: int = 3
    item_group_list = [list_of_items_in_line[i:i + item_to_group]
        for i in range(0, len(list_of_items_in_line), item_to_group)]

    for word_list in item_group_list:
        menu_item = {key: word.replace("\u02cc", ",") if key == KEYS[0] else word
            for key, word in zip(KEYS, word_list)}

        pid = parent_id(menu_item, KEYS[2], KEYS[1])

        if pid is None:
            item = find(menu_item[KEYS[1]], menu_list)
            if item is None:
                info("create_menu:root: {} --> {}", menu_item[KEYS[1]], menu_item)
                menu_list.append(menu_item)
                object_cache[menu_item[KEYS[1]]] = menu_item
        else:
            info("create_menu:child: {} --> {}", menu_item[KEYS[1]], menu_item, debug=True)

            if menu_item[KEYS[1]] in object_cache:
                cached_item = object_cache[menu_item[KEYS[1]]]
                cached_item[KEYS[0]] = menu_item[KEYS[0]]
                cached_item[KEYS[2]] = menu_item[KEYS[2]]

            if menu_item[KEYS[1]] not in object_cache:
                object_cache[menu_item[KEYS[1]]] = menu_item

            if pid not in object_cache:
                object_cache[pid] =  {
                    KEYS[0]:'none',
                    KEYS[1]:f'{pid}',
                    KEYS[2]:'none'
                }
                menu_parent = find(pid, menu_list)
                if menu_parent is None:
                    menu_list.append(object_cache[pid])

            parent = object_cache[pid]
            if parent is not None and "children" in parent:
                child = find(menu_item[KEYS[1]], parent["children"])
                if child is None:
                    parent["children"].append(menu_item)
                    object_cache[parent[KEYS[1]]] = parent
            else:
                if parent is not None:
                    parent["children"] = [menu_item]
                    object_cache[parent[KEYS[1]]] = parent


def parent_id(menu_item, split_attribute, match_attribute):
    """The method to extract parent id.
       The method extracts the parent id from the link
       The last id is the menu item id and the secon last id
       is the parent id. This parent id is returned or None

       Parameters
       ----------
       menu_item : dictionary
        the representation of the menu item

       split_attribute : string
        the attribute which is to be split for parent id extraction

       match_attribute : string
        the attribute for cross verification of the item

       Returns
       -------
       int
        the id of the parent menu item
    """
    link = menu_item[split_attribute].split("/")
    pid = link[-2]
    if pid.isdigit() and menu_item[match_attribute] == link[-1]:
        info("parent_id: found parent id {}", pid, debug=True)
        return pid

    return None

def find(item_id, items):
    """The method to search item in the list.
       The method finds an item in the list given it's id

       Parameters
       ----------
       item_id : string
        the id of the menu item
       items : list
        the list to check for

       Returns
       -------
       dictionary
        the representation of the menu item or None
    """
    for item in items:
        if "children" in item and len(item["children"]) != 0:
            child = find(item_id, item["children"])
            if child is not None:
                return child

        if item[KEYS[1]] == item_id:
            return item

    return None
