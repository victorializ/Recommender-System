from surprise import Reader, Dataset, SVD
from surprise.model_selection import cross_validate
import pandas

def filter():
    reader = Reader()
    df = pandas.read_csv('ratings_small.csv')
    data = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)
    svd = SVD()
    cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)
    trainset = data.build_full_trainset()
    svd.fit(trainset)
    print(df[df['userId'] == 1])
    print(svd.predict(1, 301, 3))
    print(svd.predict(1, 333, 3))
    print(svd.predict(1, 567, 3))
    return data