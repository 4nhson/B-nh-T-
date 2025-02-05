import pandas as pd
from pytrends.request import TrendReq
import folium

def fetch_trends(keywords, timeframe='now 7-d'):
    pytrend = TrendReq(hl='en-US', tz=360)
    pytrend.build_payload(kw_list=keywords, geo='VN', timeframe=timeframe)
    df = pytrend.interest_by_region(resolution='province', inc_low_vol=True, inc_geo_code=True)
    df = df.reset_index().rename(columns={'geoName': 'province'})
    return df

def create_map(df, keyword):
    # If you have a CSV file "province_coords.csv" with columns: province, latitude, longitude
    coords = pd.read_csv('province_coords.csv')  # or define a dictionary if you have limited data

    # Merge the Trends data with coordinates
    # Each row in df has [province, <keyword>]
    df_merged = df.merge(coords, how='inner', on='province')

    # Create a Folium map
    m = folium.Map(location=[15.0, 108.0], zoom_start=5)
    
    for _, row in df_merged.iterrows():
        province = row['province']
        popularity = row[keyword]
        lat = row['latitude']
        lon = row['longitude']

        folium.Circle(
            location=[lat, lon],
            radius=popularity * 300,  # scale factor
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.5,
            tooltip=f"{province}: {popularity}"
        ).add_to(m)

    m.save("index.html")  # Save as index.html so GitHub Pages can serve it directly

if __name__ == "__main__":
    keywords = ["dảk"]  # or multiple ["dảk", "u là trời"], etc.
    df_trends = fetch_trends(keywords, timeframe='now 7-d')
    
    # For simplicity, handle one keyword here. If multiple, you'd loop or pick one.
    create_map(df_trends, keywords[0])
    print("Map updated successfully!")
