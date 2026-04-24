from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
import statistics

app = FastAPI(title="servidor inteligente de calificacion")

"""
base de datos (sqlite)
"""

def get_db():
    conn = sqlite3.connect("umb.db")
    return conn

def crear_tablas():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS calificaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        estudiante_id INTEGER,
        materia TEXT,
        nota REAL
    )
    """)

    conn.commit()
    conn.close()

crear_tablas()

"""
modelos
"""

class estudiante(BaseModel):
    nombre: str

class calificacion(BaseModel):
    estudiante_id: int
    materia: str
    nota: float

"""
ia simple 
"""

def evaluar_desempeno(notas):
    if len(notas) == 0:
        return {"error": "sin calificaciones"}
    
    promedio = statistics.mean(notas)

    if promedio >= 9:
        estado = "excelente"
        recomendacion = "puede participar en proyectos"

    elif promedio >= 7:
        estado = "regular"
        recomendacion = "debe reforzar algunos temas"

    else:
        estado = "en riesgo"
        recomendacion = "requiere tutorias"

    return {
        "promedio": round(promedio, 2),
        "estado": estado,
        "recomendacion": recomendacion
    }

"""
endpoints
"""

@app.get("/")
def inicio():
    return {"mensaje": "servidor funcionando"}

@app.post("/estudiante")
def agregar_estudiante(est: estudiante):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO estudiantes (nombre) VALUES (?)", (est.nombre,))
    conn.commit()
    conn.close()
    return {"mensaje": "estudiante agregado"}

@app.post("/calificacion")
def agregar_calificacion(cal: calificacion):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO calificaciones (estudiante_id, materia, nota)
    VALUES (?, ?, ?)
    """, (cal.estudiante_id, cal.materia, cal.nota))
    conn.commit()
    conn.close()
    return {"mensaje": "calificacion agregada"}

@app.get("/evaluar/{estudiante_id}")
def evaluar(estudiante_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT nota FROM calificaciones WHERE estudiante_id = ?", (estudiante_id,))
    datos = cursor.fetchall()
    conn.close()

    notas = [d[0] for d in datos]
    return evaluar_desempeno(notas)