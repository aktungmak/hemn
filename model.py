from sklearn import linear_model
from sklearn.model_selection import train_test_split

def train_and_test(model, df, random_state=1):
    train, test = train_test_split(df, test_size=0.2, random_state=random_state)
    train_X = train.loc[:, ['living_area', 'price', 'rooms', 'dist_from_centre']]
    train_y = train.selling_price
    test_X = test.loc[:, ['living_area', 'price', 'rooms', 'dist_from_centre']]
    test_y = test.selling_price

    model.fit(train_X, train_y)
    return model.score(test_X, test_y)
