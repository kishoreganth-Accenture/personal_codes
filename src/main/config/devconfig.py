import configparser
import os

import mysql.connector

db_config = configparser.ConfigParser()


def connect_db(env):
    db_config.read(os.path.dirname(os.getcwd()) + '\\config\\{}.property'.format(env))
    host = db_config.get(env, 'host')
    user = db_config.get(env, 'user')
    password = db_config.get(env, 'password')
    db = db_config.get(env, 'db')
    return host, user, password, db
