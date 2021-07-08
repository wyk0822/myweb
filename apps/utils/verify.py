# -*- coding: utf-8 -*-
import re
import os.path
from IPy import IP


base_path = os.path.dirname(os.path.abspath(__file__))

RETRY_TIMES = 3





def verify_username(username):
    try:
        if len(username) > 32:
            return False
        return True
    except:
        return False


def verify_password(passwrod):
    try:
        if len(passwrod) < 8 or len(passwrod) > 32:
            return False
        pattern1 = re.compile(r'[0-9A-Za-z]+')
        if re.findall(pattern1, passwrod):
            pattern2 = re.compile(r'[^0-9A-Za-z]+')
            if re.findall(pattern2, passwrod):
                return False
            return True
        else:
            return False
    except:
        return False


def verify_ipv4_address(ip):
    try:
        if not re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", ip):
            return False
        IP(ip)
        return True
    except:
        return False


def verify_ipv4_cidrs(cidr):
    try:
        if not re.match(r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}/(?:[0-9]|1[0-6]?)$", cidr):
            return False
        IP(cidr)
        return True
    except:
        return False






def verify_register_address(addr_str):
    pattern = re.compile("^https?\:\/\/[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62}){0,4}")
    m = re.match(pattern, addr_str)
    if m:
        if m.group(0) == addr_str:
            if not re.findall('--', addr_str):
                return True
    return False


def verify_url_prefix(addr_str):
    pattern = re.compile("^https?\:\/\/[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+(:6553[0-5]|:655[0-2]\d|:65[0-4]\d{2}|:6[0-4]\d{4}|:[1-5]\d{4}|:[1-9]\d{1,3}|:[0-9]){0,1}")
    m = re.match(pattern, addr_str)
    if m:
        if m.group(0) == addr_str:
            return True
    return False


