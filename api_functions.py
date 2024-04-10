## FUNCIONES 

# Librerias
import pandas as pd
import operator
from functools import lru_cache

# Cargar Datos
df_reviews = pd.read_parquet('Datasets/df_reviews.parquet')
df_gastos_items = pd.read_parquet('Datasets/df_gastos_items.parquet')
df_genre_ranking = pd.read_parquet('Datasets/df_genre_ranking.parquet')
df_playtime_forever = pd.read_parquet('Datasets/df_playtime_forever.parquet')
df_items_developer = pd.read_parquet('Datasets/df_items_developer.parquet')
piv_norm = pd.read_parquet('Datasets/piv_norm.parquet')
item_sim_df = pd.read_parquet('Datasets/item_sim_df.parquet')
user_sim_df = pd.read_parquet('Datasets/user_sim_df.parquet')

def presentacion():
    '''
    Página de presentación HTML para la API Steam de consultas de videojuegos.
    '''
    return '''
    <html>
        <head>
            <title>API Steam</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                    text-align: center;
                }
                p {
                    color: #666;
                    text-align: center;
                    font-size: 18px;
                    margin-top: 20px;
                }
            </style>
        </head>
        <body>
            <h1>API de consultas de videojuegos de la plataforma Steam</h1>
            <p>API de Steam donde se pueden hacer diferentes consultas sobre la plataforma de videojuegos.</p>
        </body>
    </html>
    '''

def userdata(user_id):
    '''
    Esta función devuelve información sobre un usuario según su 'user_id'.
         
    Args:
        user_id (str): Identificador único del usuario.
    
    Returns:
        dict: Un diccionario que contiene información sobre el usuario.
            - 'cantidad_dinero' (int): Cantidad de dinero gastado por el usuario.
            - 'porcentaje_recomendacion' (float): Porcentaje de recomendaciones realizadas por el usuario.
            - 'total_items' (int): Cantidad de items que tiene el usuario.
    '''
    # Filtra por el usuario de interés
    usuario = df_reviews[df_reviews['user_id'] == user_id]
    # Calcula la cantidad de dinero gastado para el usuario de interés
    cantidad_dinero = df_gastos_items[df_gastos_items['user_id']== user_id]['price'].iloc[0]
    # Busca el count_item para el usuario de interés    
    count_items = df_gastos_items[df_gastos_items['user_id']== user_id]['items_count'].iloc[0]
    
    # Calcula el total de recomendaciones realizadas por el usuario de interés
    total_recomendaciones = usuario['reviews_recommend'].sum()
    # Calcula el total de reviews realizada por todos los usuarios
    total_reviews = len(df_reviews['user_id'].unique())
    # Calcula el porcentaje de recomendaciones realizadas por el usuario de interés
    porcentaje_recomendaciones = (total_recomendaciones / total_reviews) * 100
    
    return {
        'cantidad_dinero': int(cantidad_dinero),
        'porcentaje_recomendacion': round(float(porcentaje_recomendaciones), 2),
        'total_items': int(count_items)
    }

def countreviews(fecha_inicio, fecha_fin):
    '''
    Esta función devuelve estadísticas sobre las reviews realizadas por los usuarios entre dos fechas.
         
    Args:
        fecha_inicio (str): Fecha de inicio para filtrar la información en formato YYYY-MM-DD.
        fecha_fin (str): Fecha de fin para filtrar la información en formato YYYY-MM-DD.
    
    Returns:
        dict: Un diccionario que contiene estadísticas de las reviews entre las fechas especificadas.
            - 'total_usuarios_reviews' (int): Cantidad de usuarios que realizaron reviews entre las fechas.
            - 'porcentaje_recomendaciones' (float): Porcentaje de recomendaciones positivas (True) entre las reviews realizadas.
    '''
    # Filtra el dataframe entre las fechas de interés
    user_data_entre_fechas = df_reviews[(df_reviews['reviews_date'] >= fecha_inicio) & (df_reviews['reviews_date'] <= fecha_fin)]
    # Calcula la cantidad de usuarios que dieron reviews entre las fechas de interés
    total_usuarios = user_data_entre_fechas['user_id'].nunique()
    # Calcula el total de recomendaciones entre las fechas de interes (True + False)
    total_recomendacion = len(user_data_entre_fechas)
    # Calcula la cantidad de recomendaciones positivas que que hicieron entre las fechas de interés
    total_recomendaciones_True = user_data_entre_fechas['reviews_recommend'].sum()
    # Calcula el porcentaje de recomendación realizadas entre el total de usuarios
    porcentaje_recomendaciones = (total_recomendaciones_True / total_recomendacion) * 100
    
    return {
        'total_usuarios_reviews': int(total_usuarios),
        'porcentaje_recomendaciones': round(float(porcentaje_recomendaciones),2)
    }

def genre(genero):
    '''
    Esta función devuelve la posición de un género de videojuego en un ranking basado en la cantidad de horas jugadas.
         
    Args:
        genero (str): Género del videojuego.
    
    Returns:
        dict: Un diccionario que contiene la posición del género en el ranking.
            - 'rank' (int): Posición del género en el ranking basado en las horas jugadas.
    '''
    # Busca el ranking para el género de interés
    rank = df_genre_ranking[df_genre_ranking['genres'] == genero]['ranking'].iloc[0]
    return {
        'rank': int(rank)
    }

def userforgenre(genero):
    '''
    Esta función devuelve el top 5 de usuarios con más horas de juego en un género específico, junto con su URL de perfil y ID de usuario.
         
    Args:
        genero (str): Género del videojuego.
    
    Returns:
        dict: Un diccionario que contiene el top 5 de usuarios en un género.
            - 'usuarios' (list): Lista de diccionarios de usuarios en el top 5.
                Cada diccionario contiene:
                - 'user_id' (str): ID del usuario.
                - 'playtime_forever' (float): Horas jugadas en el género.
                - 'profile_url' (str): URL del perfil de Steam del usuario.
    '''
    # Filtra los datos de horas jugadas para el género de interés
    top_users = df_playtime_forever[df_playtime_forever['genre'] == genero].head(5)
    
    # Crea una lista de diccionarios para el top 5 de usuarios en el género
    usuarios = []
    for _, row in top_users.iterrows():
        user_id = row['user_id']
        playtime_forever = row['playtime_forever']
        profile_url = f'https://steamcommunity.com/profiles/{user_id}/'
        
        usuarios.append({
            'user_id': str(user_id),
            'playtime_forever': round(float(playtime_forever), 2),
            'profile_url': profile_url
        })
    
    return {
        'usuarios': usuarios
    }

@lru_cache(maxsize=128)
def recomendacion_juego(item_id):
    '''
    Esta función devuelve una lista de juegos recomendados basados en el juego con el ID 'item_id'.
         
    Args:
        item_id (str): ID del juego.
    
    Returns:
        dict: Un diccionario que contiene los juegos recomendados.
            - 'juegos_recomendados' (list): Lista de diccionarios de juegos recomendados.
                Cada diccionario contiene:
                - 'item_id' (str): ID del juego recomendado.
                - 'score' (float): Puntaje de similitud con el juego base.
    '''
    # Filtra la similitud del item de interés
    similar_items = item_sim_df[item_id].dropna()
    
    # Crea una lista de juegos recomendados con sus puntajes de similitud
    juegos_recomendados = []
    for item, score in similar_items.items():
        juegos_recomendados.append({
            'item_id': str(item),
            'score': round(float(score), 4)
        })
    
    # Ordena los juegos recomendados por puntaje de similitud
    juegos_recomendados = sorted(juegos_recomendados, key=lambda x: x['score'], reverse=True)
    
    return {
        'juegos_recomendados': juegos_recomendados
    }

@lru_cache(maxsize=128)
def recomendacion_usuario(user_id):
    '''
    Esta función devuelve una lista de juegos recomendados para un usuario específico basado en sus preferencias.
         
    Args:
        user_id (str): ID del usuario.
    
    Returns:
        dict: Un diccionario que contiene los juegos recomendados para el usuario.
            - 'juegos_recomendados' (list): Lista de diccionarios de juegos recomendados.
                Cada diccionario contiene:
                - 'item_id' (str): ID del juego recomendado.
                - 'score' (float): Puntaje de recomendación para el usuario.
    '''
    # Busca los juegos que el usuario ya ha comprado
    juegos_comprados = df_gastos_items[df_gastos_items['user_id'] == user_id]['item_id'].tolist()
    
    # Inicializa un diccionario para almacenar la suma de similitudes
    recomendaciones = {}
    
    # Itera sobre los juegos comprados por el usuario
    for juego in juegos_comprados:
        # Filtra los juegos similares al juego actual
        juegos_similares = item_sim_df[str(juego)].dropna()
        
        # Itera sobre los juegos similares y suma los puntajes de similitud
        for item, score in juegos_similares.items():
            if item not in juegos_comprados:
                if item in recomendaciones:
                    recomendaciones[item] += score
                else:
                    recomendaciones[item] = score
    
    # Ordena las recomendaciones por puntaje de similitud
    juegos_recomendados = sorted(recomendaciones.items(), key=operator.itemgetter(1), reverse=True)
    
    # Filtra los juegos recomendados para excluir los juegos que el usuario ya ha comprado
    juegos_recomendados = [{'item_id': str(item), 'score': round(float(score), 4)} for item, score in juegos_recomendados if item not in juegos_comprados]
    
    return {
        'juegos_recomendados': juegos_recomendados
    }

# Se puede ejecutar el código como una aplicación Flask
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return presentacion()

@app.route('/api/userdata/<user_id>')
def get_userdata(user_id):
    return jsonify(userdata(user_id))

@app.route('/api/countreviews')
def get_countreviews():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    return jsonify(countreviews(fecha_inicio, fecha_fin))

@app.route('/api/genre/<genero>')
def get_genre(genero):
    return jsonify(genre(genero))

@app.route('/api/userforgenre/<genero>')
def get_userforgenre(genero):
    return jsonify(userforgenre(genero))

@app.route('/api/recomendacionjuego/<item_id>')
def get_recomendacionjuego(item_id):
    return jsonify(recomendacion_juego(item_id))

@app.route('/api/recomendacionusuario/<user_id>')
def get_recomendacionusuario(user_id):
    return jsonify(recomendacion_usuario(user_id))

if __name__ == '__main__':
    app.run()