#!/usr/bin/env python3
"""Genera bitácora de aprendizaje 2023 con commits repartidos todo el año."""
import os
import random
import subprocess
import sys
from datetime import datetime, timedelta

RAIZ = os.path.dirname(os.path.abspath(__file__))
random.seed(2023)

MODULOS = [
    ("01-python-basico", "Fundamentos de Python", [
        "variables y tipos", "listas y diccionarios", "bucles for y while",
        "funciones", "ficheros txt", "excepciones try except", "modulos import",
    ]),
    ("02-git-github", "Control de versiones", [
        "primer repo", "commits y ramas", "merge basico", "gitignore",
        "pull requests", "resolver conflictos",
    ]),
    ("03-html-css", "Web estatica", [
        "estructura html5", "flexbox", "grid layout", "formularios",
        "responsive mobile", "landing personal",
    ]),
    ("04-javascript", "JS en el navegador", [
        "dom basico", "eventos click", "fetch api", "localstorage",
        "validacion formulario", "mini todo list",
    ]),
    ("05-sql", "Bases de datos", [
        "select where", "joins", "group by", "insert update",
        "indices", "diseno tablas pedidos",
    ]),
    ("06-flask", "Backend Python", [
        "hola flask", "rutas dinamicas", "plantillas jinja",
        "formularios post", "sqlite conexion", "api json simple",
    ]),
    ("07-pandas", "Analisis de datos", [
        "read csv", "filtros", "groupby ventas", "matplotlib grafico",
        "limpieza nulos", "export excel",
    ]),
    ("08-scikit-learn", "Machine learning", [
        "train test split", "regresion lineal", "clasificacion knn",
        "matriz confusion", "cross validation", "pipeline sklearn",
    ]),
    ("09-docker", "Contenedores", [
        "dockerfile python", "build imagen", "docker compose",
        "volumenes", "redes", "deploy local",
    ]),
    ("10-proyecto-final", "Mini proyecto integrador", [
        "esquema proyecto", "modelo datos", "api rest", "tests basicos",
        "readme documentacion", "refactor codigo", "demo final",
    ]),
]

MENSAJES_EXTRA = [
    "repaso de apuntes", "arreglo typo", "practica del finde",
    "ejercicio del curso", "notas de clase", "wip", "ya funciona",
    "limpio codigo", "añado comentarios", "prueba en local",
]


def git(*args, env=None):
    e = os.environ.copy()
    if env:
        e.update(env)
    r = subprocess.run(["git"] + list(args), cwd=RAIZ, capture_output=True, text=True, env=e)
    if r.returncode != 0:
        print(r.stderr or r.stdout)
        sys.exit(r.returncode)
    return r.stdout.strip()


def fechas_2023():
    """~200 dias con actividad repartidos por 2023."""
    inicio = datetime(2023, 1, 10)
    fin = datetime(2023, 12, 20)
    fechas = []
    actual = inicio
    while actual <= fin:
        # menos commits en agosto y navidad
        mes = actual.month
        prob = 0.62
        if mes in (1, 2, 3, 6, 9, 10, 11):
            prob = 0.72
        if mes == 8:
            prob = 0.22
        if mes == 12 and actual.day > 18:
            prob = 0.18
        if actual.weekday() < 5 and random.random() < prob:
            hora = random.randint(9, 23)
            minuto = random.randint(0, 59)
            f = actual.replace(hour=hora, minute=minuto, second=random.randint(0, 59))
            fechas.append(f)
        if random.random() < 0.22:
            f2 = actual.replace(hour=random.randint(18, 23), minute=random.randint(0, 59))
            fechas.append(f2)
        actual += timedelta(days=1)
    fechas.sort()
    return fechas


def escribir(ruta, contenido):
    os.makedirs(os.path.dirname(ruta), exist_ok=True) if os.path.dirname(ruta) else None
    with open(ruta, "w", encoding="utf-8", newline="\n") as f:
        f.write(contenido)


def commit_en(fecha, mensaje):
    env = {
        "GIT_AUTHOR_NAME": "Diego Castilla",
        "GIT_AUTHOR_EMAIL": "castilla204@gmail.com",
        "GIT_COMMITTER_NAME": "Diego Castilla",
        "GIT_COMMITTER_EMAIL": "castilla204@gmail.com",
        "GIT_AUTHOR_DATE": fecha.strftime("%Y-%m-%d %H:%M:%S +0100"),
        "GIT_COMMITTER_DATE": fecha.strftime("%Y-%m-%d %H:%M:%S +0100"),
    }
    git("add", "-A")
    check = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=RAIZ)
    if check.returncode != 0:
        git("commit", "-m", mensaje, env=env)


def main():
    # limpiar si existe .git previo
    git_dir = os.path.join(RAIZ, ".git")
    if os.path.exists(git_dir):
        import shutil
        shutil.rmtree(git_dir)

    git("init")
    git("branch", "-M", "main")

    escribir(".gitignore", "env/\n__pycache__/\n*.pyc\n.DS_Store\n")
    escribir("README.md", "# bitacora-dev-2023\n\nApuntes y ejercicios de 2023.\n")
    commit_en(datetime(2023, 1, 8, 19, 30, 0), "empiezo bitacora de aprendizaje 2023")

    fechas = fechas_2023()
    idx_mod = 0
    idx_ej = 0
    contador = 0

    for fecha in fechas:
        if idx_mod >= len(MODULOS):
            carpeta, titulo, ejercicios = MODULOS[-1]
        else:
            carpeta, titulo, ejercicios = MODULOS[idx_mod]

        if idx_ej >= len(ejercicios):
            idx_mod = min(idx_mod + 1, len(MODULOS) - 1)
            idx_ej = 0
            carpeta, titulo, ejercicios = MODULOS[idx_mod]

        ej = ejercicios[idx_ej]
        idx_ej += 1
        contador += 1

        ext = "py" if "python" in carpeta or "flask" in carpeta or "pandas" in carpeta or "scikit" in carpeta else "md"
        if "html" in carpeta or "javascript" in carpeta:
            ext = "html" if idx_ej % 2 else "js"
        if "sql" in carpeta:
            ext = "sql"

        ruta = os.path.join("2023", carpeta, f"ejercicio_{idx_ej:02d}.{ext}")
        escribir(
            ruta,
            f"# {titulo} — {ej}\n\nFecha: {fecha.strftime('%Y-%m-%d')}\n\n"
            f"Practica personal de Diego Castilla.\n",
        )

        escribir(
            os.path.join("2023", carpeta, "notas.md"),
            f"# {titulo}\n\nProgreso: {idx_ej}/{len(ejercicios)} ejercicios.\n",
        )

        if random.random() < 0.3:
            msg = random.choice(MENSAJES_EXTRA)
        else:
            msg = f"{carpeta}: {ej}"

        commit_en(fecha, msg)

    # readme final
    escribir(
        "README.md",
        """# bitacora-dev-2023

Bitácora de aprendizaje de **Diego Castilla** durante 2023.

Recorrido por Python, web, SQL, Flask, pandas, scikit-learn y Docker. Cada carpeta en `2023/` son ejercicios y notas que fui haciendo poco a poco mientras cursaba DAW y empezaba con IA.

## Contenido

| Carpeta | Tema |
|---------|------|
| 01-python-basico | Python desde cero |
| 02-git-github | Git y GitHub |
| 03-html-css | Web estática |
| 04-javascript | JS en el navegador |
| 05-sql | SQL y modelado |
| 06-flask | API y backend |
| 07-pandas | Análisis de datos |
| 08-scikit-learn | ML introductorio |
| 09-docker | Contenedores |
| 10-proyecto-final | Mini proyecto integrador |

Año 2023 — repositorio de práctica personal.
""",
    )
    commit_en(datetime(2023, 12, 20, 17, 45, 0), "cierro la bitacora 2023")

    total = subprocess.run(["git", "rev-list", "--count", "HEAD"], cwd=RAIZ, capture_output=True, text=True)
    print(f"Listo: {total.stdout.strip()} commits en 2023")


if __name__ == "__main__":
    main()
