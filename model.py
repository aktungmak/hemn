from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures

def model_with_price(model, df):
    predictors = ['living_area', 'price', 'rooms', 'dist_from_centre']
    response = 'selling_price'
    return train_and_score_model(model, df, predictors, response)

def model_with_price_lat_lon(model, df):
    predictors = ['living_area', 'price', 'rooms', 'lat', 'lon']
    response = 'selling_price'
    return train_and_score_model(model, df, predictors, response)

def model_without_price(model, df, degree):
    predictors = ['living_area', 'rooms', 'dist_from_centre']
    response = 'price'
    return train_and_score_model(model, df, predictors, response, degree=degree)

def model_without_price_lat_lon(model, df, degree):
    predictors = ['living_area', 'rooms', 'lat', 'lon']
    response = 'price'
    return train_and_score_model(model, df, predictors, response, degree=degree)

def train_and_score_model(model, df, predictors, response, random_state=1, degree=3):
    poly = PolynomialFeatures(degree)
    train, test = train_test_split(df, test_size=0.2, random_state=random_state)

    train_X = train.loc[:, predictors]
    train_X = poly.fit_transform(train_X)
    train_y = train[response]

    test_X = test.loc[:, predictors]
    test_X = poly.fit_transform(test_X)
    test_y = test[response]

    model.fit(train_X, train_y)
    return model.score(test_X, test_y)
