from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Movie, Rating
import requests
from .services import get_similar_movies, get_user_ratings, user_based, item_based, svd_recommendations


def fill_poster_link(movies):
    for movie in movies:
        if not movie.poster_link:
            data = requests.get(f"http://www.omdbapi.com/?i={movie.movie_id}&apikey=9ec4e126").json()
            movie.poster_link = data["Poster"]
            movie.save()


# Create your views here.
def home_redirect(request):
    # popularity based рекомендация
    popular_movies = Movie.objects.filter(rating__gt=7).order_by('?')[:4]
    
    user = request.user
    user_ratings = Rating.objects.filter(user=user)
    ratings, watched, user_watched = get_user_ratings(
        [(int(x.user_rating), x.movie.name) for x in user_ratings])
    
    # svd++ рекомендация
    svd_movies = [Movie.objects.filter(name=item[0])[0] for item in svd_recommendations(ratings, watched, 4, user.pk)]
    # user_bsed рекомендация
    user_based_movies = [Movie.objects.filter(name=item[0])[0] for item in user_based(ratings, 15, watched)]
    # item_based рекомендации
    item_based_movies = [Movie.objects.filter(name=item[0])[0] for item in item_based(ratings, user_watched, 4)]
    
    max_rating = max(int(x.user_rating) for x in user_ratings)
    
    # content-based рекомендация
    if len(user_ratings) > 0:
        content_based_movie = Rating.objects.filter(user=user, user_rating=max_rating).order_by("?")[0].movie.name # один из высоко оценненных фильмов
        content_based_movies = [Movie.objects.filter(name=name)[0] for name in
                                get_similar_movies(content_based_movie, 4)]
    else:
        content_based_movies = []
    
    fill_poster_link(content_based_movies)
    fill_poster_link(popular_movies)
    fill_poster_link(user_based_movies)
    fill_poster_link(item_based_movies)
    fill_poster_link(svd_movies)

    context = {
        "popular_movies": popular_movies,
        "content_based_movies": content_based_movies, # список рекомендованных фильмов
        "content_based_title": content_based_movie, # фильм, на основе которого была построена рекомендация
        "user_based_movies": user_based_movies,
        "item_based_movies": item_based_movies,
        "svd_movies": svd_movies
    }
    return render(request, 'index.html', context=context)


def set_rating(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user = request.user
            movie_pk, new_rating = request.POST.get("rating").split("_")
            movie = Movie.objects.get(pk=movie_pk)

            try:
                rating = Rating.object.get(user=user, movie=movie)
                rating.user_rating = float(new_rating)
                rating.save()
            except:
                rating = Rating(user=user, user_rating=new_rating, movie=movie)
                rating.save()

    return render(request, 'index.html')


class Search(ListView):
    """Поиск фильмов"""
    context_object_name = "movies"
    template_name = "movies_list.html"

    def get_queryset(self):
        movies = Movie.objects.filter(name__icontains=self.request.GET.get("query"))
        fill_poster_link(movies)
        return movies

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["query"] = self.request.GET.get("query")
        return context


class MovieDetailView(DetailView):
    """Вывод кинофильма"""
    model = Movie
    template_name = "movie_detail.html"
    context_object_name = "movie"

    def get_context_data(self, **kwargs):
        context = super(MovieDetailView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')

        movie_title = Movie.objects.get(pk=pk).name

        recommend_movies = [Movie.objects.filter(name=name)[0] for name in
                            get_similar_movies(movie_title, 5)]
        fill_poster_link(recommend_movies)

        context['recommend_movies'] = recommend_movies
        return context
