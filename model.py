from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures


def with_list_price(model, df):
    predictors = ["livingArea", "listPrice", "rooms", "floor", "dist_from_centre"]
    response = "soldPrice"
    return train_and_score_model(model, df, predictors, response)


def with_list_price_lat_lon(model, df):
    predictors = ["livingArea", "listPrice", "rooms", "floor", "latitude", "longitude"]
    response = "soldPrice"
    return train_and_score_model(model, df, predictors, response)


def without_list_price(model, df, degree):
    predictors = ["livingArea", "rooms", "dist_from_centre"]
    response = "price"
    return train_and_score_model(model, df, predictors, response, degree=degree)


def without_list_price_lat_lon(model, df, degree):
    predictors = ["livingArea", "rooms", "latitude", "longitude"]
    response = "price"
    return train_and_score_model(model, df, predictors, response, degree=degree)


def without_list_price_all(model, df, degree):
    predictors = [
        "daysActive",
        "dist_from_centre",
        "floor",
        "latitude",
        "livingArea",
        "longitude",
        "rooms",
    ]
    response = "price"
    return train_and_score_model(model, df, predictors, response, degree=degree)


def train_and_score_model(model, df, predictors, response, random_state=5, degree=3):
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


def predict(model, X, degree=3):
    poly = PolynomialFeatures(degree)
    X = poly.fit_transform(X)
    return model.predict(X)
