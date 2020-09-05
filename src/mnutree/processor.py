# -*- coding: utf-8 -*-
"""A module to read the csv file containig the menu data.
   The module than form the parent child relation ship in csv data.
   The module gives a list containing dictoniaries. The dictonry
   follow the parent child structure as derived from the csv menu file.
"""
import re
from pathlib import Path
from argparse import Namespace
from collections import defaultdict
from typing import List, Tuple, Dict, DefaultDict, Optional, Any

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
    quotes: List[str] = re.findall(r'"(.*?)"', line)
    if len(quotes) != 0:
        for quote in quotes:
            line = line.replace(quote, quote.replace(",", "\u02cc"))
            line = line.replace("\"", "")

    info("normallize: {}", line, debug=True)
    return line


def process(args: Namespace) -> Tuple[Path, List[Dict[str, Any]]]:
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
    file_path: Path = Path(args.csv_file) if args.csv_file.find("/") > -1\
    else Path("./"+args.csv_file)

    menu_list: List[Dict[str, Any]] = []
    object_cache: DefaultDict[str, Dict[str, Any]] = defaultdict(lambda : {})

    with file_path.open() as file:
        line: str
        line_count: int = 0
        for line in file:
            line = line.rstrip()
            if line_count == 0:
                line_count += 1
                info("process:header: {} ", line, debug=True)
            else:
                line_count += 1
                line = normallize(line)
                list_of_items_in_line: List[str] = [word for word in line.split(',')
                    if word and word != "\n"]
                len_list_of_items_in_line: int = len(list_of_items_in_line)
                info("process: {} . len --> {}, list_of_items_in_line --> {}",
                    line_count, len_list_of_items_in_line, list_of_items_in_line, debug=True)
                if len_list_of_items_in_line != 0:
                    create_menu(list_of_items_in_line, menu_list, object_cache)

    info("process: The file path is {} ", file_path.with_suffix('.json'))

    return file_path.with_suffix('.json'), menu_list


def create_menu(list_of_items_in_line: List[str], menu_list: List[Dict[str, Any]],
     object_cache: DefaultDict[str, Dict[str, Any]]) -> None:
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
    item_group_list: List[List[str]] = [list_of_items_in_line[i:i + item_to_group]
        for i in range(0, len(list_of_items_in_line), item_to_group)]

    word_list: List[str]
    for word_list in item_group_list:
        menu_item: Dict[str, Any] = {key: word.replace("\u02cc", ",") if key == KEYS[0] else word
            for key, word in zip(KEYS, word_list)}

        pid: Optional[str] = parent_id(menu_item, KEYS[2], KEYS[1])

        if pid is None:
            cached_item: Dict[str, Any] = object_cache[menu_item[KEYS[1]]]
            cached_item.setdefault(KEYS[0], menu_item[KEYS[0]])
            cached_item.setdefault(KEYS[1], menu_item[KEYS[1]])
            cached_item.setdefault(KEYS[2], menu_item[KEYS[2]])

            root_item: Optional[Dict[str, Any]] = find(cached_item[KEYS[1]], menu_list)
            info("root item --> {}", root_item, debug=True)
            if not root_item:
                info("create_menu:root: {} --> {}", menu_item[KEYS[1]], menu_item)
                menu_list.append(cached_item)
        else:
            info("create_menu:child: {} --> {}", menu_item[KEYS[1]], menu_item, debug=True)

            cached_item = object_cache[menu_item[KEYS[1]]]
            cached_item.setdefault(KEYS[0], menu_item[KEYS[0]])
            cached_item.setdefault(KEYS[1], menu_item[KEYS[1]])
            cached_item.setdefault(KEYS[2], menu_item[KEYS[2]])

            parent: Dict[str, Any] = object_cache[pid]
            parent.setdefault(KEYS[1], pid)
            parent.setdefault("children", [cached_item])

            child: Optional[Dict[str, Any]] = find(cached_item[KEYS[1]], parent["children"])
            if not child:
                parent["children"].append(cached_item)

def parent_id(menu_item: Dict[str, Any], split_attribute: str,
    match_attribute: str) -> Optional[str]:
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
    pid: str = link[-2]
    if pid.isdigit() and menu_item[match_attribute] == link[-1]:
        info("parent_id: found parent id {}", pid, debug=True)
        return pid

    return None

def find(item_id: str, items: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
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
    if len(items) == 0:
        return None

    for item in items:
        if item[KEYS[1]] == item_id:
            return item
    return None