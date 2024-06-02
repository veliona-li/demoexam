# del.py 
import os

import sqlite3

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkcalendar import DateEntry

 Удаление старой базы данных, если она существует
if os.path.exists('requests.db'):
    os.remove('requests.db')

 Функции работы с базой данных
def create_db():
    try:
