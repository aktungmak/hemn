import pandas as pd
import sys

# the centre of stockholm
clat, clon = 59.329444, 18.068611

def clean_data(filename):
    df = pd.read_csv(filename)
    df = df.drop(columns=['locations.country', 'locations.city',
                          'broker_agency_id', 'locations.region',
                          'locations.street', 'locations.district'])

    df = df[df.selling_price < 8000000]

    df.price = df.price.fillna(df.selling_price)
    df = df.dropna()

    df.sold_at_date              = pd.to_datetime(df.sold_at_date)
    df.price                     = df.price.astype('int64')
    df['locations.municipality'] = df['locations.municipality'].astype('category')
    df['locations.postal_city']  = df['locations.postal_city'].astype('category')
    # clean up street name
    # get lat/lng again if seems incorrect
    df['dist_from_centre'] = np.sqrt(np.square(clat - df.lat) + np.square(clon - df.lon))

    df['sppm2']      = df.selling_price / df.living_area
    df['bid_factor'] = df.selling_price / df.price

    return df

if __name__ == '__main__':
    df = clean_data(sys.argv[1])
    df.to_csv(sys.argv[2], index=False)
