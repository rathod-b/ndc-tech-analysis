# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 20:35:54 2021

@author: bhavrathod
"""
import pandas as pd
import geopandas
import folium
import matplotlib.pyplot as plt

def importBase():
    
    fp = 'worldCountries/World_Countries__Generalized_.shp'
    countries = geopandas.read_file(fp)
    countries.plot(figsize=(12,12))
    
    countries['lat'] = countries.centroid.y
    countries['lon'] = countries.centroid.x
    # print(countries.columns)
    
    return countries

def loadCategories():
    
    LDCs = ['Afghanistan','Angola','Bangladesh','Benin','Bhutan','Burkina Faso','Burundi',\
            'Cambodia','Central African Republic','Chad','Comoros','Congo DRC','Djibouti',\
            'Eritrea','Ethiopia','Gambia','Guinea','Guinea-Bissau','Haiti','Kiribati',\
            'Lao People’s Democratic Republic','Lesotho','Liberia','Madagascar','Malawi',\
            'Mali','Mauritania','Mozambique','Myanmar','Nepal','Niger','Rwanda',\
            'Sao Tome and Principe','Senegal','Sierra Leone','Solomon Islands','Somalia',\
            'South Sudan','Sudan','Timor-Leste','Togo','Tuvalu','Uganda','United Republic of Tanzania','Yemen','Zambia']

    SIDS = ['Antigua and Barbuda','Guyana','Singapore','Bahamas','Haiti ','StKitts and Nevis','Bahrain','Jamaica','StLucia',\
            'Barbados','Kiribati','StVincent and the Grenadines','Belize','Maldives','Seychelles','Cabo Verde','Marshall Islands',\
            'Solomon Islands','Comoros','Federated States of Micronesia','Suriname','Cuba','Mauritius','Timor-Leste ','Dominica',\
            'Nauru','Tonga','Dominican Republic','Palau','Trinidad and Tobago','Fiji','Papua New Guinea','Tuvalu','Grenada',\
            'Samoa','Vanuatu','Guinea-Bissau','Sao Tome and Principe']
    
    Afr = ['Algeria','Angola','Benin','Botswana','Burkina Faso','Burundi','Cameroon','Cabo Verde','Central African Republic',\
           'Chad','Comoros','Congo','Congo DRC','Cote d’Ivoire','Djibouti','Equatorial Guinea','Egypt',\
           'Eritrea','Ethiopia','Gabon','Gambia','Ghana','Guinea','Guinea-Bissau. Kenya','the Kingdom of Lesotho','Liberia',\
           'Libya','Madagascar','Malawi','Mali','Mauritania','Mauritius','Morocco','Mozambique','Namibia','Niger','Nigeria',\
           'Rwanda','Saharawi Arab Democratic Republic','Sao Tome and Principe','Senegal','Seychelles','Sierra Leone','Somalia',\
           'South Africa','South Sudan','Sudan','Kingdom of Swaziland','Tanzania','Togo','Tunisia','Uganda','Zambia','Zimbabwe']
    
    G77 = ['Afghanistan','Algeria','Angola','Antigua and Barbuda','Argentina','Azerbaijan','Bahamas','Bahrain','Bangladesh',\
           'Barbados','Belize','Benin','Bhutan','Bolivia','Botswana','Brazil','Brunei Darussalam',\
           'Burkina Faso','Burundi','Cabo Verde','Cambodia','Cameroon','Central African Republic','Chad','Chile','China',\
           'Colombia','Comoros','Congo','Costa Rica','Côte d\'Ivoire','Cuba','Democratic People\'s Republic of Korea',\
           'Congo DRC','Djibouti','Dominica','DominicanRepublic','Ecuador','Egypt','El Salvador',\
           'Equatorial Guinea','Eritrea','Eswatini','Ethiopia','Fiji','Gabon','Gambia','Ghana','Grenada','Guatemala','Guinea',\
           'Guinea-Bissau','Guyana','Haiti','Honduras','India','Indonesia','Iran','Iraq','Jamaica','Jordan',\
           'Kenya','Kiribati','Kuwait','Laos','Lebanon','Lesotho','Liberia','Libya','Madagascar',\
           'Malawi','Malaysia','Maldives','Mali','Marshall Islands','Mauritania','Mauritius','Micronesia (Federated States of)',\
           'Mongolia','Morocco','Mozambique','Myanmar','Namibia','Nauru','Nepal','Nicaragua','Niger','Nigeria','Oman','Pakistan',\
           'Panama','Papua New Guinea','Paraguay','Peru','Philippines','Qatar','Rwanda','Saint Kitts and Nevis','Saint Lucia',\
           'Saint Vincent and the Grenadines','Samoa','Sao Tome and Principe','Saudi Arabia','Senegal','Seychelles','Sierra Leone',\
           'Singapore','Solomon Islands','Somalia','South Africa','South Sudan','Sri Lanka','State of Palestine','Sudan',\
           'Suriname','Syrian Arab Republic','Tajikistan','Thailand','Timor-Leste','Togo','Tonga','Trinidad and Tobago','Tunisia',\
           'Turkmenistan','Uganda','United Arab Emirates','United Republic of Tanzania','Uruguay','Vanuatu',\
           'Venezuela','Vietnam','Yemen','Zambia','Zimbabwe']
    
    completed = ['Bangladesh', 'Seychelle', 'Malawi', 'Ethiopia', 'Kenya', 'Tuvalu', 'Kiribati', 'Uganda', 'Central African Republic',\
                 'Gambia', 'Palau', 'Tanzania', 'Zambia', 'Tonga', 'Cambodia', 'Nepal', 'Maldives', 'Eritrea', 'Jamaica', 'Saint Lucia']

    return LDCs,SIDS,Afr,G77,completed
        
# Add category columns to country
def processCategories(LDCs,SIDS,Afr,G77,completed,countries):
    
    countries['isLDC'] = 0
    countries['isSIDS'] = 0
    countries['isAfrica'] = 0
    countries['isG77'] = 0
    
    for i in range(countries.shape[0]):
        if countries.iloc[i,1] in LDCs:
            countries.loc[i,['isLDC']] = 1
        if countries.iloc[i,1] in SIDS:
            countries.loc[i,['isSIDS']] = 1
        if countries.iloc[i,1] in Afr:
            countries.loc[i,['isAfrica']] = 1
        if countries.iloc[i,1] in G77:
            countries.loc[i,['isG77']] = 1
    
    # Remove rows where none of the flags are set.
    c = countries[(countries.isLDC==1)|(countries.isSIDS==1)|(countries.isAfrica==1)|(countries.isG77==1)]
    # print(c.shape, countries.shape)
    countryDF = pd.DataFrame(c)
    
    return countryDF


# Creates Folium map to visualize information.
def createMap(countryDF,completed):
    
    m = folium.Map(location=[0,0], tiles="Stamen toner", zoom_start=2)

    ldcFG = folium.FeatureGroup(name='LDCs')
    sidsFG = folium.FeatureGroup(name='SIDS')
    africaFG = folium.FeatureGroup(name='Africa')
    g77FG = folium.FeatureGroup(name='G77',show=False)
    doneFG = folium.FeatureGroup(name='Completed',show=False)
    
    missCountries = []
    
    # example code from https://geopandas.readthedocs.io/en/latest/gallery/polygon_plotting_with_folium.html
    for _, r in countryDF.iterrows():
        sim_geo = geopandas.GeoSeries(r['geometry'])
        ctry = r['COUNTRY']
        geo_j = sim_geo.to_json()
        if r['isLDC']:
            geo_j = folium.GeoJson(data=geo_j,style_function=lambda x: {'weight':1,'fillColor': 'orange','fillOpacity':0.25})
            folium.Popup(ctry).add_to(geo_j)
            geo_j.add_to(ldcFG)
    
    for _, r in countryDF.iterrows():
        sim_geo = geopandas.GeoSeries(r['geometry'])
        ctry = r['COUNTRY']
        geo_j = sim_geo.to_json()
        if r['isSIDS']:
            geo_j = folium.GeoJson(data=geo_j,style_function=lambda x: {'weight':1,'fillColor': 'orange','fillOpacity':0.25})
            folium.Popup(ctry).add_to(geo_j)
            geo_j.add_to(sidsFG)
            folium.Marker(location=[r['lat'], r['lon']], popup='SIDS '+str(ctry)).add_to(sidsFG)
    
    for _, r in countryDF.iterrows():
        sim_geo = geopandas.GeoSeries(r['geometry'])
        ctry = r['COUNTRY']
        geo_j = sim_geo.to_json()
        if r['isAfrica']:
            geo_j = folium.GeoJson(data=geo_j,style_function=lambda x: {'weight':1,'fillColor': 'orange','fillOpacity':0.25})
            folium.Popup(ctry).add_to(geo_j)
            geo_j.add_to(africaFG)
    
    for _, r in countryDF.iterrows():
        sim_geo = geopandas.GeoSeries(r['geometry'])
        ctry = r['COUNTRY']
        geo_j = sim_geo.to_json()
        if r['isG77']:
            geo_j = folium.GeoJson(data=geo_j,style_function=lambda x: {'weight':1,'fillColor': 'orange','fillOpacity':0.25})
            folium.Popup(ctry).add_to(geo_j)
            geo_j.add_to(g77FG)
            
    for _, r in countryDF.iterrows():
        sim_geo = geopandas.GeoSeries(r['geometry'])
        ctry = r['COUNTRY']
        if ctry in completed:
            geo_j = sim_geo.to_json()
            geo_j = folium.GeoJson(data=geo_j,style_function=lambda x: {'weight':1,'fillColor': 'green','fillOpacity':1})
            folium.Popup(ctry).add_to(geo_j)
            geo_j.add_to(doneFG)
    
    ldcFG.add_to(m)
    sidsFG.add_to(m)
    africaFG.add_to(m)
    g77FG.add_to(m)
    doneFG.add_to(m)
    
    folium.LayerControl().add_to(m)
    m.save('countries.html')
    
def main():
    
    countries = importBase()
    LDCs,SIDS,Afr,G77,completed = loadCategories()
    countryDF = processCategories(LDCs,SIDS,Afr,G77,completed,countries)
    createMap(countryDF,completed)

main()