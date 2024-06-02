# del.py 
import os

import sqlite3

import tkinter as tk

from tkinter import messagebox

from tkinter import ttk

from tkcalendar import DateEntry


if os.path.exists('requests.db'):
    os.remove('requests.db')

def create_db():
    try:
