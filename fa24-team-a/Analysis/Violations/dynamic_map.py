import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

data_path = 'Overall_Boston_violations.csv'
geojson_path = 'boston_neighborhoods.geojson'
data = pd.read_csv(data_path, low_memory=False)
geo_data = gpd.read_file(geojson_path)

data['count'] = pd.to_numeric(data['count'], errors='coerce')
data['year'] = data['year'].astype(str)

st.sidebar.title("Year Selection")
years = sorted(data['year'].dropna().unique())
selected_years = st.sidebar.multiselect("Select Year(s)", years, default=years[:1])

if selected_years:
    filtered_data = data[data['year'].isin(selected_years)]
    aggregated_data = (
        filtered_data.groupby(['Neighbourhood', 'description'], as_index=False)
        .agg({'count': 'sum'})
    )
    total_violations = (
        aggregated_data.groupby('Neighbourhood', as_index=False)
        .agg({'count': 'sum'})
        .rename(columns={'count': 'total_count'})
    )
    
    merged_data = geo_data.merge(total_violations, left_on='neighborhood', right_on='Neighbourhood', how='left')
    merged_data['total_count'] = merged_data['total_count'].fillna(0)

    category_summary = (
        aggregated_data.groupby('Neighbourhood')[['description', 'count']]
        .apply(lambda x: x.sort_values('count', ascending=False).set_index('description').to_dict(orient='index'))
    )
    
    multiplier = len(selected_years)
    red_threshold = 150 * multiplier
    orange_threshold = 50 * multiplier

    def get_color_scale(value):
        if value > red_threshold:
            return '#FF0000'
        elif value > orange_threshold:
            return '#FFA500'
        elif value > 25 * multiplier:
            return '#FFFF00'
        else:
            return '#00FF00'

    boston_map = folium.Map(location=[42.3601, -71.0589], zoom_start=12, tiles='CartoDB positron')
    for _, row in merged_data.iterrows():
        if row['total_count'] == 0:
            continue
        neighborhood_name = row['neighborhood']
        categories = category_summary.get(neighborhood_name, {})
        top_categories = list(categories.items())[:5]
        category_text = '<ul>' + ''.join([f"<li>{cat}: {data['count']} violations</li>" for cat, data in top_categories]) + '</ul>'

        folium.GeoJson(
            row['geometry'],
            style_function=lambda feature, row=row: {
                'fillColor': get_color_scale(row['total_count']),
                'color': 'black',
                'weight': 0.5,
                'fillOpacity': 0.7,
            },
            tooltip=folium.Tooltip(
                f"""
                <strong>{row['neighborhood']}: {row['total_count']} total violations</strong><br><br>
                <strong>Top 5 violations are:</strong><br>
                {category_text}
                """,
                sticky=True
            ),
        ).add_to(boston_map)

    st.title("Boston Neighborhood Violations")
    st.write(f"Selected Years: {', '.join(selected_years)}")
    #st.write(f"Color Thresholds: Red > {red_threshold}, Orange > {orange_threshold}, Yellow > {10 * multiplier}")
    st_folium(boston_map, width=700, height=500)
else:
    st.write("Please select at least one year to display the map.")
