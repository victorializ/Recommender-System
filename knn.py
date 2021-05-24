import numpy as np
import scipy.spatial

class KNN:
    def __init__(self, k, similarity):
        self.k = k
        self.similarity = similarity
        
    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
        
    #def distance(self, X1, X2):
    #    distance = self.similarity[X1][X2]
    
    def predict(self, X_test):
        final_output = []
        for i in range(len(X_test)):
            d = []
            #votes = []
            for j in range(len(self.X_train)):
                dist = self.similarity[self.X_train[j]][X_test[i]]
                d.append([dist, j])
            d.sort()
            d = d[0:self.k]
            '''
            for d, j in d:
                votes.append(y_train[j])
            ans = Counter(votes).most_common(1)[0][0]
            final_output.append(ans)
            '''
        return final_output
    
    def score(self, X_test, y_test):
        predictions = self.predict(X_test)
        return (predictions == y_test).sum() / len(y_test)

'''

class KNNSimilarityBased:
    def __init__(self, similarity, k=5):
        self.k = k
        self.similarity = similarity
    
    def fit(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

    def test(self, X_test):
        predictions = []
        for i in range(len(X_test)):
            neighbours = []
            test_id = X_test.iat[i, 1]
            test_index = ids.index(test_id)
            for j in range(len(self.X_train)):
                train_id = self.X_train.iat[j, 1]
                train_index = ids.index(train_id)
                distance = self.similarity[test_index][train_index]
                neighbours.append((distance, j))
            neighbours.sort(key = lambda value: value[0], reverse=True)
            neighbours = neighbours[0:k]
            rating = 0
            sim_sum = 0
            for n in range(k):
                sim, neighbour_id = neighbours[n]
                rating += sim * self.y_train.iat[neighbour_id]
                sim_sum += sim
            y_pred = rating / sim_sum
            predictions.append(y_pred)
        return predictions
    
    def predict(uid, iid):
        neighbours = []
        test_index = ids.index(iid) 
        user = df_ratings.loc[df_ratings['userId'] == uid]
        for i in range(len(user)):
            train_id = user.iat[j, 1]
            train_index = ids.index(train_id)
            distance = similarity[test_index][train_index]
            neighbours.append((distance, j))
        neighbours.sort(key = lambda value: value[0], reverse=True)
        neighbours = neighbours[0:self.k]
        rating = 0
        sim_sum = 0
        for n in range(k):
            sim, neighbour_id = neighbours[n]
            rating += sim * user.iat[neighbour_id]
            sim_sum += sim
        y_pred = rating / sim_sum
        return y_pred

'''