# Importaciones
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
import api_functions as af

# Se instancia la aplicación
app = FastAPI()

# Funciones
@app.get(path="/", response_class=HTMLResponse, tags=["Home"])
async def home():
    '''
    Página de inicio que muestra una presentación.

    Returns:
    HTMLResponse: Respuesta HTML que muestra la presentación.
    '''
    return await af.presentacion()

@app.get(path='/userdata', description="Muestra la cantidad de dinero gastado por el usuario, el porcentaje de recomendación y la cantidad de items que tiene el mismo.", tags=["Consultas Generales"])
async def userdata(user_id: str = Query(..., description="Identificador único del usuario", example="EchoXSilence")):
    return await af.userdata(user_id)

@app.get(path='/countreviews', description="Muestra el resultado de la clasificación de las fechas de inicio y fin proporcionadas.", tags=["Consultas Generales"])
async def countreviews(fecha_inicio: str = Query(..., description="Fechas de inicio para filtrar la información", example='2011-11-05'), fecha_fin: str = Query(..., description="Fechas de Fin para filtrar la información", example='2012-12-24')):
    return await af.countreviews(fecha_inicio, fecha_fin)

@app.get(path='/genre', description="Muestra la posición del ranking donde se encuentra el género del juego proporcionado.", tags=["Consultas Generales"])
async def genre(genero: str = Query(..., description="Género del videojuego", example='Simulation')):
    return await af.genre(genero)

@app.get(path='/userforgenre', description="Muestra el Top 5 de usuarios con más horas de juego en el género dado, con su URL y user_id.", tags=["Consultas Generales"])
async def userforgenre(genero: str = Query(..., description="Género del videojuego", example='Simulation')):
    return await af.userforgenre(genero)

@app.get(path='/developer', description="Muestra la cantidad de items y porcentaje de contenido Free por año de ese desarrollador.", tags=["Consultas Generales"])
async def developer(desarrollador: str = Query(..., description="Desarrollador del videojuego", example='Valve')):
    return await af.developer(desarrollador)

@app.get('/sentiment_analysis', description="Muestra la cantidad de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento para el año proporcionado.", tags=["Consultas Generales"])
async def sentiment_analysis(anio: str = Query(..., description="Año para filtrar los sentimientos de las reseñas", example="2009")):
    return await af.sentiment_analysis(anio)

@app.get('/recomendacion_juego', description="Muestra los juegos recomendados a partir del nombre del juego proporcionado.", tags=["Recomendación"])
async def recomendacion_juego(game: str = Query(..., description="Juego a partir del cuál se hace la recomendación de otros juego", example="Killing Floor")):
    return await af.recomendacion_juego(game)

@app.get('/recomendacion_usuario', description="Muestra los juegos recomendados para el usuario proporcionado.", tags=["Recomendación"])
async def recomendacion_usuario(user: str = Query(..., description="Usuario a partir del cuál se hace la recomendación de los juego", example="76561197970982479")):
    return await af.recomendacion_usuario(user)
