#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Supermercado Click & Collect - Aplicación web sencilla
Solo usa la librería estándar de Python: http.server, sqlite3, json, urllib.parse
No requiere Flask, FastAPI, Django, React ni paquetes de pip.

Comando para correr:
    python server.py

URL del navegador:
    Cliente:  http://localhost:8000/
    Admin:    http://localhost:8000/admin
"""

import http.server
import socketserver
import sqlite3
import json
import urllib.parse
from datetime import datetime

DB_NAME = "supermercado.db"
PORT = 8000


def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL DEFAULT 0,
            categoria TEXT NOT NULL DEFAULT 'General',
            stock INTEGER NOT NULL DEFAULT 0
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            cliente TEXT NOT NULL,
            telefono TEXT NOT NULL,
            horario TEXT NOT NULL,
            estado TEXT NOT NULL DEFAULT 'Pendiente',
            fecha TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS reservation_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reservation_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario REAL NOT NULL,
            FOREIGN KEY (reservation_id) REFERENCES reservations(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    c.execute("SELECT COUNT(*) AS cnt FROM products")
    if c.fetchone()["cnt"] == 0:
        productos = [
            ("Leche Entera 1L", 1.20, "Lácteos", 50),
            ("Huevos (docena)", 3.50, "Lácteos", 30),
            ("Pan Integral", 2.00, "Panadería", 25),
            ("Pollo (1 kg)", 5.90, "Carnicería", 20),
            ("Manzanas (bolsa)", 2.80, "Frutas y Verduras", 40),
            ("Arroz (1 kg)", 1.50, "Despensa", 60),
            ("Detergente", 4.20, "Limpieza", 15),
            ("Coca Cola 2L", 2.50, "Bebidas", 35),
            ("Papas fritas", 1.80, "Snacks", 28),
            ("Papel Higiénico (4 rollos)", 3.00, "Limpieza", 22),
        ]
        c.executemany(
            "INSERT INTO products (nombre, precio, categoria, stock) VALUES (?, ?, ?, ?)",
            productos,
        )

    c.execute("SELECT COUNT(*) AS cnt FROM reservations")
    if c.fetchone()["cnt"] == 0:
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        c.execute(
            "INSERT INTO reservations (codigo, cliente, telefono, horario, estado, fecha) VALUES (?, ?, ?, ?, ?, ?)",
            ("#RES-001", "Juan Pérez", "+56 9 1234 5678", "10:00 - 11:00", "Pendiente", ahora),
        )
        rid1 = c.lastrowid
        c.execute(
            "INSERT INTO reservation_items (reservation_id, product_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
            (rid1, 1, 2, 1.20),
        )
        c.execute(
            "INSERT INTO reservation_items (reservation_id, product_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
            (rid1, 3, 1, 2.00),
        )
        c.execute("UPDATE products SET stock = stock - 2 WHERE id = 1")
        c.execute("UPDATE products SET stock = stock - 1 WHERE id = 3")

        c.execute(
            "INSERT INTO reservations (codigo, cliente, telefono, horario, estado, fecha) VALUES (?, ?, ?, ?, ?, ?)",
            ("#RES-002", "María García", "+56 9 8765 4321", "11:00 - 12:00", "Listo para retirar", ahora),
        )
        rid2 = c.lastrowid
        c.execute(
            "INSERT INTO reservation_items (reservation_id, product_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
            (rid2, 4, 1, 5.90),
        )
        c.execute(
            "INSERT INTO reservation_items (reservation_id, product_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
            (rid2, 5, 3, 2.80),
        )
        c.execute("UPDATE products SET stock = stock - 1 WHERE id = 4")
        c.execute("UPDATE products SET stock = stock - 3 WHERE id = 5")

    conn.commit()
    conn.close()
