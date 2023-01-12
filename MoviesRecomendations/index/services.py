import numpy as np
import pandas as pd
import json
import pickle
from .classes import SVD_pp


def _get_interact_matrix() -> pd.DataFrame:
    """Возвращает матрицу взаимодействия user-item, с обнуленным средним значением"""
    return pd.read_csv("/Users/Denis/Python/MovieRecomendations/interact_matrix.csv")


def _get_movie_df() -> pd.DataFrame:
    """Возвращает датафрейм отобранных фильмов"""
    return pd.read_csv("/Users/Denis/Python/MovieRecomendations/recomend_df")


def _get_movies_similarity() -> np.array:
    """Возвращает матрицу схожести фильмов. Метрика: косинус угла между тегами фильмамов"""
    with open('/Users/Denis/Python/MovieRecomendations/similarity.npy', 'rb') as f:
        similarity = np.load(f)

    return similarity


def _get_id_to_movie() -> dict:
    """Возвращает словарь, где ключ  - индекс фильма в таблице, а значение индекс фильма в датасете"""
    interact_matrix = _get_interact_matrix()
    columns = interact_matrix.columns
    id_to_movie = {i: columns[i] for i in range(len(columns))}
    return id_to_movie


def get_similar_movies(movie_title: str, n: int) -> list[str]:
    df = _get_movie_df()
    similarity = _get_movies_similarity()
    id_of_movie = df[df['name'] == movie_title].index[0]
    distances = similarity[id_of_movie]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:n + 1]

    return [df.iloc[i[0]]["name"] for i in movie_list]


def get_user_ratings(user_data: list[tuple]):
    """
    user_data - cписок кортежей вида (rating, movie_title), функция возвращает numpy.array с
    рейтингами пользователя
     """
    interact_matrix = _get_interact_matrix()
    recommend_df = _get_movie_df()
    # Здесь стоит запарится о том, чтобы переделать id-фильмов, вместо imdb_id взять id фильма из датасета
    # или добавить новое поле. Пока оставлю так
    ratings = [(x[0], recommend_df[recommend_df["name"] == x[1]]["id"].values[0]) for x in user_data]
    columns = interact_matrix.columns
    movie_to_id = {columns[i]: i for i in range(len(columns))}

    user_ratings = np.zeros((len(movie_to_id)))
    user_ratings.fill(np.nan)

    for rating in ratings:
        if str(rating[1]) in movie_to_id:
            user_ratings[movie_to_id[str(rating[1])]] = rating[0]

    user_watched = np.zeros((len(movie_to_id)))
    user_watched[~np.isnan(user_ratings)] = 1

    return user_ratings, ratings, user_watched



def item_based(user_ratings: np.array, user_watched: np.array, top_n: int) -> list[tuple]:
    """Построение рекмоендаций для пользователя на основе item-based фильтрации"""
    user_ratings = user_ratings[1:]
    user_ratings[np.isnan(user_ratings)] = np.nanmean(user_ratings)
    user_watched = user_watched[1:]
    movies = _get_movie_df()
    id_to_movie = _get_id_to_movie()
    with open('/Users/Denis/Python/MovieRecomendations/item_based_sim.npy', 'rb') as f:
        item_based_sim = np.load(f)

    recommendations = []

    if user_watched.sum() + 1 >= 10:
        pred = np.zeros(1410)
        for i in range(len(pred)):
            s = (item_based_sim[i].dot(user_ratings - user_ratings.mean()) / abs(item_based_sim[i]).dot(
                user_watched).sum())
            if np.isnan(s):
                s = 0
            else:
                s = user_ratings.mean()

            pred[i] = s
        for i in np.argsort(pred)[::-1][:top_n]:
            recommendations.append((movies[movies['id'] == int(id_to_movie[i])]['name'].values[0], pred[i]))

    return recommendations


def user_based(user_ratings: np.array, n_neighbors: int, watched: list[tuple]) -> list[tuple]:
    """Построение рекмоендаций для пользователя на основе user-based фильтрации"""
    interact_matrix = _get_interact_matrix()
    movies = _get_movie_df()
    user_ratings[np.isnan(user_ratings)] = np.nanmean(user_ratings)
    recommendations = []

    if len(watched) >= 10:
        # Создадим вектор "похожести" пользоветелей
        sim = np.zeros((interact_matrix.shape[0]))
        for i in range(interact_matrix.shape[0]):
            s = (user_ratings - user_ratings.mean()).dot(interact_matrix.iloc[i]) / sum(
                (user_ratings - user_ratings.mean()) ** 2) ** 0.5 / sum(
                interact_matrix.iloc[i] ** 2) ** 0.5
            if np.isnan(s):
                s = 0
            sim[i] = s

        # Обнулим всех соседей, начиная с n_neighbors + 1
        sim[np.argsort(sim)[::-1][n_neighbors + 1::]] = 0

        # Построим вектор предсказанных оценок для пользователя
        pred = user_ratings.mean() + interact_matrix.T.dot(sim) / abs(sim).sum()

        # Обнулим рейтинги на те фильмы, которые пользователь уже оценил
        for item in watched:
            pred.loc[str(item[1])] = 0

        # Выведем топ-10 фильмов, которые пользователь может высоко оценить
        recommendations = []
        for i in pred.sort_values(ascending=False).index[1:5]:
            recommendations.append((movies[movies['id'] == int(i)]['name'].values[0], pred.loc[i]))
    return recommendations


def svd_recommendations(user_ratings: np.array, user_watched: np.array, top_n: int, user_pk: int) -> list[tuple]:
    """Возвращает рекомендации фильмов для пользователя"""
    with open('/Users/Denis/Python/MovieRecomendations/svd_users.json', 'rb') as inp:
        users = json.load(inp)

    with open('/Users/Denis/Python/MovieRecomendations/my_svd.pkl', 'rb') as inp:
        model = pickle.load(inp)
    user_ratings = user_ratings[1:]
    movies = _get_movie_df()
    recommendations = []
    if len(user_watched) >= 10:
        if str(user_pk) in users:
            user_id = users[str(user_pk)]
            model.update_user(user_id, user_ratings)
        else:
            user_id = model.u.shape[0]
            users[str(user_pk)] = user_id
            model.add_new_user(user_ratings)

        id_to_movie = _get_id_to_movie()
        pred = []
        for key, value in id_to_movie.items():
            pred.append((value, model.predict(user_id=user_id, item_id=key - 1)))

        pred.sort(key=lambda x: -x[1])

        for item in pred[:top_n]:
            recommendations.append((movies[movies['id'] == int(item[0])]['name'].values[0], item[1]))
        with open('/Users/Denis/Python/MovieRecomendations/my_svd.pkl', 'wb') as outp:
            pickle.dump(model, outp, pickle.HIGHEST_PROTOCOL)

        with open('/Users/Denis/Python/MovieRecomendations/svd_users.json', 'w', encoding='utf-8') as outp:
            json.dump(users, outp)

        return recommendations

    return []
