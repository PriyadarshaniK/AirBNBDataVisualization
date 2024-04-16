#For the GUI part
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import plotly.express as px
from wordcloud import WordCloud, STOPWORDS

import warnings
warnings.filterwarnings('ignore')

#Setting the page layout
st.set_page_config(
    page_title="Airbnb Data Visualization",
    page_icon="house_with_garden",
    layout="wide",
    initial_sidebar_state="expanded")

#for smaller text below each plot
st.markdown("""
<style>
.small-font {
    font-size:10px !important;
}
</style>
""", unsafe_allow_html=True)



# READING THE CLEANED DATAFRAME
airbnb_df = pd.read_csv(r'C:\Users\Acer\Desktop\PythonPrograms\AirbnbProject4\AirbnbCleanData.csv')


#Create the first screen of the streamlit application, to display few radio buttons on the sidebar and for user inputs on the right.
header = st.container()

sidebar1 = st.sidebar

with header:
    st.subheader("Airbnb Data Visualization and Exploration")

with sidebar1:
    selection = sidebar1.radio("What's your choice of task?",[":house: Home",":bar_chart:(Static-Data-Insights)",":chart_with_upwards_trend:(Dynamic-Data-Insights)"])

#Plain text information about the project and what it  intends to do
if selection == ":house: Home": 
    st.markdown("Airbnb, Inc. is an American company operating an online marketplace for short- and long-term homestays and experiences. The company acts as a broker and charges a commission from each booking. The company was founded in 2008 by Brian Chesky, Nathan Blecharczyk, and Joe Gebbia. Airbnb is a shortened version of its original name, AirBedandBreakfast.com. Airbnb is the most well-known company for short-term housing rentals")
    st.markdown("Airbnb has provided many travellers a great, easy and convenient place to stay during their travels. Similarly, it has also given an opportunity for many to earn extra revenue by listing their properties for residents to stay. However, with so many listings available with varying prices - ")
    st.markdown("- How can an aspiring host know what type of property to invest in if his main aim is to list it in Airbnb and earn rental revenue? ")
    st.markdown("- Additionally, if a traveller wants to find the cheapest listing available but with certain features he prefers like 'free parking' etc, how does he know what aspects to look into, to find a suitable listing?")
    st.markdown(" There are many factors which influence the price of a listing. Which is why this project aims to find the most important factors that affect the price and more importantly the features that are common among the most expensive listings. This will allow an aspiring Airbnb host to ensure that his listing is equipped with those important features such that he will be able to charge a higher price without losing customers. Moreover, a traveller will also know the factors to look into to get the lowest price possible while having certain features he prefers. ")

#In this screen all the static data insights can be viewed. There are no user inputs taken here and different columns of the dataset have been analysed and interpreted here
if selection == ":bar_chart:(Static-Data-Insights)":

    col1,col2 = st.columns([3,3])
    with col1:
    
        fig = plt.figure(figsize=(10,8))
        ax = sns.countplot(data=airbnb_df,y=airbnb_df.property_type.values,order=airbnb_df.property_type.value_counts().index[:15],palette = "Set1")
        # ax.bar_label(ax.containers[0], fontsize=8)

        # Add labels to each bar
        for container in ax.containers:
            ax.bar_label(container, fontsize=8)
        plt.title('Top 15 Property Types available')
        plt.xlabel('Count')
        plt.ylabel('Property Type')
        st.pyplot(fig)

        st.markdown('<p class="small-font">From the above graph, we can see that maximum listings are of apartment and next comes full houses. Other property types in the dataset are very less. As we discover in the next graph, hosts prefer to list their full property than just a room or shared room, it can be inferred that most listings in this dataset are entire apartments or entire houses.</p>', unsafe_allow_html=True)
        

    with col2:
        fig = plt.figure(figsize=(10,8))
        ax = sns.countplot(data=airbnb_df,y=airbnb_df.room_type.values,order=airbnb_df.room_type.value_counts().index[:5],palette = "Set2")
        # Add labels to each bar
        for container in ax.containers:
            ax.bar_label(container, fontsize=8)
        plt.title('Top Room Types available')
        plt.xlabel('Count')
        plt.ylabel('Room Type')
        st.pyplot(fig)
        
        st.markdown('<p class="small-font">As can be seen from the countplot, most of the listings were the entire home/apartment. There are almost twice as many entire home/apartment listings as private room listings. This gives a small insight into the type of listings available and the number of each type.</p>', unsafe_allow_html=True)

    
    col4, col5 = st.columns([3,3])

    with col4:
        fig = plt.figure(figsize=(10,8))
        # Get the top 15 property types
        top_property_types = airbnb_df['property_type'].value_counts().index[:15]
    
        # Filter the DataFrame to include only the top 15 property types
        df_filtered = airbnb_df[airbnb_df['property_type'].isin(top_property_types)]
    
        # Create pivot table to calculate mean prices
        data_matrix = df_filtered.pivot_table(index="property_type", columns="room_type", values="price", aggfunc='mean')
        sns.heatmap(data_matrix, cmap="viridis", annot=True, fmt="0.0f")
        plt.title('Mean Prices by Room Type and Property Type(Top 15)')
        plt.xlabel('Room Type')
        plt.ylabel('Property Type')
        st.pyplot(fig)

        st.markdown('<p class="small-font">From the above heatmap, with lighter colour(yellow) representing higher price and darker(blue) representing lower price, we can see that shared rooms in a condominium have the lightest colour hence costliest. Private rooms have a slightly darker colour so they are in the middle, and entire houses in a "bed and breaksfast" are the next lightest thus they are next level expensive. It is also important to note that the highest number of listings which was house and apartments actually have higher costs for the "Entire home/apt" room_type category. All of this tells us that the room_type and property_type both play a very important role in the final price of the listing.</p>', unsafe_allow_html=True)

    with col5:
        fig = plt.figure(figsize=(10,8))
        sns.boxplot(data=airbnb_df, x="bedrooms", y="price",palette = 'plasma',whis = 1.5,showfliers=False)
        plt.title('Analyzing listings based on number of bedrooms')
        plt.xlabel('Number of bedrooms')
        plt.ylabel('Price')
        st.pyplot(fig)

        st.markdown('<p class="small-font">From the box plots above, it can be seen that listings have higher prices as the number of bedrooms increase.</p>', unsafe_allow_html=True)

    col6,col7 = st.columns([3,3])
    with col6:
        fig = plt.figure(figsize=(10,8))
        stopwords = set(STOPWORDS)
        # Sort DataFrame by price
        price_df = airbnb_df.sort_values(by='price', inplace=False)

        # Extract amenities from top 100 listings
        top_amenities = ', '.join(price_df.head(100)['amenities'])
        wordcloud = WordCloud(
                      background_color = 'black',
                      stopwords=stopwords,
                      max_words = 1000,
                      max_font_size = 120,
                      random_state = 42
                    ).generate(top_amenities)

        #Plotting the word cloud
        plt.axis('off')
        st.image(wordcloud.to_array(), caption='Word Cloud of Amenities from Top 100 Listings', use_column_width=True)

        st.markdown('<p class="small-font">The word cloud above was taken from the top 100 listings in terms of their price. We can see that the listings with the highest prices have amenities such as Hot water, Wifi, Kitchen, Laptop friendly, friendly workspace. So, an aspiring Airbnb host should ensure that his property contains these amenities so that he can charge a higher price. Similarly, if a traveller does not require any of these amenities, he can opt for a listing without them to save cost.</p>', unsafe_allow_html=True)

    with col7:
        fig = plt.figure(figsize=(10,8))
        g = sns.countplot(data=airbnb_df,x=airbnb_df.host_neighbourhood.values,order=airbnb_df.host_neighbourhood.value_counts().index[:25],palette = "Set3")
        g.set_xticklabels(g.get_xticklabels(),rotation=45, ha="right")
        # Add labels to each bar
        for container in g.containers:
            g.bar_label(container, fontsize=8)
        plt.title('Top Number of Listings for neighborhoods')
        plt.ylabel('Number of Listings')
        st.pyplot(fig)

    col8,col9 = st.columns([3,3])

    with col8:
        fig = plt.figure(figsize=(10,8))
        ax = sns.barplot(airbnb_df, x="host_neighbourhood", y="price", order=airbnb_df.host_neighbourhood.value_counts().index[:25], estimator="median", errorbar=None,palette='magma')
        # Add labels to each bar
        for container in ax.containers:
            ax.bar_label(container, fontsize=8)
        ax.set_xticklabels(ax.get_xticklabels(),rotation=45, ha="right")
        plt.title('Number of listings for each neighbourhood and the median price')
        plt.xlabel('Neighbourhood')
        plt.ylabel('Median Price')
        st.pyplot(fig)

        st.markdown('<p class="small-font">From the plots above, we can see that most of the listings appear in Copacabana, LePlateau, Mongkok, Waikiki etc. This gives us a good insight into the potential neighbourhoods where there are higher number of listings which we can tap into. By analyzing the number of listings and prices for each neighborhood, we can get a clearer understanding of which neighbourhoods have a lot of expensive listings. Looking at the analysis done so far, we can see that certain neighbourhoods are indeed more expensive than others. However, some of those neighbourhoods do not have as many listings as other expensive neighbourhoods.</p>', unsafe_allow_html=True)
    with col9:
        fig = plt.figure(figsize=(10,8))
        g = sns.barplot(airbnb_df, x="room_type", y="availability_365", estimator="median",errorbar=None,palette='inferno')
        # Add labels to each bar
        for container in g.containers:
            g.bar_label(container, fontsize=8)
        g.set_xticklabels(g.get_xticklabels(),rotation=45, ha="right")
        plt.title('Availability of Room Types')
        plt.xlabel('Room Type')
        plt.ylabel('Median Availability')
        st.pyplot(fig)

        st.markdown('<p class="small-font">From this plot we can observe that Shared Rooms listings tend to have more availability throughout the year whereas Private Rooms have lesser availability.</p>', unsafe_allow_html=True)

#Here user inputs for some columns of the dataset are taken and corresponding plots for the selected values can be viewed.
if selection == ":chart_with_upwards_trend:(Dynamic-Data-Insights)":
    col1,col2,col3,col4 = st.columns([4,3,3,3])
    with col1:
        country = st.multiselect('Select a Country',sorted(airbnb_df.country_name.unique()))
    with col2:
        roomtype = st.multiselect('Select a Room Type',sorted(airbnb_df.room_type.unique()))
    with col3:
        propertytype = st.multiselect('Select a Property Type',sorted(airbnb_df.property_type.unique()))
    with col4:
        price_sel = st.slider('Select Price',airbnb_df.price.min(),airbnb_df.price.max(),(airbnb_df.price.min(),airbnb_df.price.max()))

    
    col6, col7 = st.columns([8,8])

    with col6:
        ############################################

        # CONVERTING THE USER INPUT INTO QUERY
        query_s = f'country_name in {country} & room_type in {roomtype} & property_type in {propertytype} & price >= {price_sel[0]} & price <= {price_sel[1]}'
    
        # Group by host and count the number of occurrences
        grouped_df = airbnb_df.query(query_s).groupby(['host_name']).size()
    
        # Sort the groups in descending order
        sorted_hosts = grouped_df.sort_values(ascending=False)
        
        # Get the top 10 hosts
        top_10_hosts = sorted_hosts.head(10)
        
        # Convert Series to DataFrame using reset_index
        # This will create a DataFrame with two columns: 'host' and 0 (or the name of the Series if it had one)
        top_10_hosts_df = top_10_hosts.reset_index()
        
        # Rename the columns
        # Here we rename the columns to 'Host' and 'Count'
        top_10_hosts_df = top_10_hosts_df.rename(columns={'host_name': 'Host', 0: 'Total_Listings'})


        ############################################
        
        fig = px.bar(top_10_hosts_df,
                         title='Top 10 Hosts with Highest number of Listings',
                         x='Total_Listings',
                         y='Host',
                         orientation='h',
                         color='Host',
                         color_continuous_scale=px.colors.sequential.Agsunset)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig,use_container_width=True)

    with col7:
            # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
            country_df = airbnb_df.query(query_s).groupby(['country_name'],as_index=False)['_id'].size().rename(columns={'size' : 'Total_Listings'})
            fig = px.choropleth(country_df,
                                title='Total Listings in each selected Country',
                                locations='country_name',
                                locationmode='country names',
                                color='Total_Listings',
                                color_continuous_scale=px.colors.sequential.Plasma
                               )
            st.plotly_chart(fig,use_container_width=True)

    #option to view different column values as hover information.
    col8,col9 = st.columns([1,5])
    with col8:
        hoverInfo = st.selectbox('Select Hover Text',['Accomodates','Bedrooms','Beds','Bathrooms','Availability','Price'])

        if hoverInfo == 'Accomodates':
            country_df = airbnb_df.query(query_s).groupby('country_name',as_index=False)['accommodates'].mean()
            country_df.accommodates = country_df.accommodates.astype(int)
            fig = px.scatter_geo(data_frame=country_df,
                                           locations='country_name',
                                           color= 'accommodates', 
                                           hover_data=['accommodates'],
                                           locationmode='country names',
                                           size='accommodates',
                                           title= 'Avg number of people accomodated in each Country',
                                           color_continuous_scale='agsunset'
                                )
        elif hoverInfo == 'Bedrooms':
            country_df = airbnb_df.query(query_s).groupby('country_name',as_index=False)['bedrooms'].mean()
            country_df.bedrooms = country_df.bedrooms.astype(int)
            fig = px.scatter_geo(data_frame=country_df,
                                           locations='country_name',
                                           color= 'bedrooms', 
                                           hover_data=['bedrooms'],
                                           locationmode='country names',
                                           size='bedrooms',
                                           title= 'Avg number of bedrooms in each Country',
                                           color_continuous_scale='agsunset'
                                )
        elif hoverInfo == 'Beds':
            country_df = airbnb_df.query(query_s).groupby('country_name',as_index=False)['beds'].mean()
            country_df.beds = country_df.beds.astype(int)
            fig = px.scatter_geo(data_frame=country_df,
                                           locations='country_name',
                                           color= 'beds', 
                                           hover_data=['beds'],
                                           locationmode='country names',
                                           size='beds',
                                           title= 'Avg number of beds in each Country',
                                           color_continuous_scale='agsunset'
                                )
        elif hoverInfo == 'Bathrooms':
            country_df = airbnb_df.query(query_s).groupby('country_name',as_index=False)['bathrooms'].mean()
            country_df.bathrooms = country_df.bathrooms.astype(int)
            fig = px.scatter_geo(data_frame=country_df,
                                           locations='country_name',
                                           color= 'bathrooms', 
                                           hover_data=['bathrooms'],
                                           locationmode='country names',
                                           size='bathrooms',
                                           title= 'Avg number of bathrooms in each Country',
                                           color_continuous_scale='agsunset'
                                )
        elif hoverInfo == 'Availability':
            country_df = airbnb_df.query(query_s).groupby('country_name',as_index=False)['availability_365'].mean()
            country_df.availability_365 = country_df.availability_365.astype(int)
            fig = px.scatter_geo(data_frame=country_df,
                                           locations='country_name',
                                           color= 'availability_365', 
                                           hover_data=['availability_365'],
                                           locationmode='country names',
                                           size='availability_365',
                                           title= 'Avg availability in each Country',
                                           color_continuous_scale='agsunset'
                                )
        elif hoverInfo == 'Price':
            country_df = airbnb_df.query(query_s).groupby('country_name',as_index=False)['price'].mean()
            country_df.price = country_df.price.astype(int)
            fig = px.scatter_geo(data_frame=country_df,
                                           locations='country_name',
                                           color= 'price', 
                                           hover_data=['price'],
                                           locationmode='country names',
                                           size='price',
                                           title= 'Avg Price in each Country',
                                           color_continuous_scale='agsunset'
                                )

    with col9:    
        st.plotly_chart(fig,use_container_width=True)

    # Creating scatter map for a specific country and all listings in that country
    col10,col11 = st.columns([2,6])
    with col10:
        country_sel = st.selectbox('Select a Country to view all Airbnb listed',sorted(airbnb_df.country_name.unique()))
        country_df = airbnb_df.query("country_name == @country_sel")
    fig = px.scatter_geo(country_df, lat='latitude', lon='longitude', color='price',
                             hover_name='name',
                             title='Airbnbs listed in specific country')
       
    st.plotly_chart(fig,use_container_width=True)
    #displaying costliest and cheapest listings in the selected country
    col12,col13 = st.columns([3,3])
    with col12:
        fig = plt.figure(figsize=(10,8))
        # Sort DataFrame by price for top 15 costliest listings
        price_df = country_df.sort_values(by='price', inplace=False)

        ax = sns.barplot(price_df.head(15), x="name", y="price",palette = "bright")
        for container in ax.containers:
            ax.bar_label(container, fontsize=8)
        ax.set_xticklabels(ax.get_xticklabels(),rotation=45, ha="right")
        plt.title('Top 15 cheapest Listings')
        plt.xlabel('Name of Listing')
        plt.ylabel('Price')
        st.pyplot(fig)

    with col13:
        fig = plt.figure(figsize=(10,8))
        # Sort DataFrame by price for top 15 cheapest listings
        price_df = country_df.sort_values(by='price', ascending = False, inplace=False)


        ax = sns.barplot(price_df.head(15), x="name", y="price",palette = "dark")
        for container in ax.containers:
            ax.bar_label(container, fontsize=8)
        ax.set_xticklabels(ax.get_xticklabels(),rotation=45, ha="right")
        plt.title('Top 15 costliest Listings')
        plt.xlabel('Name of Listing')
        plt.ylabel('Price')
        st.pyplot(fig)
        
        
