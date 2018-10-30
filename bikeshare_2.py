import time
import pandas as pd
import numpy as np
from datetime import datetime
from pprint import pprint

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may':5, 'june':6,'all':0}
DAYS= ['sunday','monday','tuesday','wednesday','thursday','friday','all']

def get_filters():
    print('\nHello! Let\'s explore some US bikeshare data!\n')
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city='' 
    month=''
    day=''
    time_filter ='' 
    both=False
    
    # TODO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while (city not in CITY_DATA):
        city = input('Please enter one of the three cities you would like to analyze \n[Chicago , Washington, New york city] - ').lower()
           
    # TODO: get user input for filtering the data by month , day or none for no time filter
    while time_filter not in ['month','day','both','none']:
        time_filter = input('\nHow do you want to filter the data? \n Type \'both\' to filter by both month and day \'month\' to filter by month \'day\' to filter by day or \'none\' for no time filter -  ').lower() 
    
    # TODO: get user input for both month and day
    if time_filter == 'both':
        both = True
        while (month not in MONTHS):
            month = input('\n\nPlease enter a specific month or \'all\' for all months \n [january, february, ... , june] -').lower()
        while (day not in DAYS):
            day = input('\n\nPlease enter a specific day of the week or \'all\' for all days \n[monday, tuesday, ... sunday] - ').lower()
    
    # TODO: get user input for month (all, january, february, ... , june)
    elif time_filter == 'month':
        while (month not in MONTHS):
            month = input('\n\nPlease enter a specific month or \'all\' for all months \n [january, february, ... , june] -').lower()
            
    # TODO: get user input for day of week (all, monday, tuesday, ... sunday)
    elif time_filter == 'day':
        while (day not in DAYS):
            day = input('\n\nPlease enter a specific day of the week or \'all\' for all days \n[monday, tuesday, ... sunday] - ').lower()
    
    print('-'*80)
    print('Let\'s explore the bike share data of {} filtered by {} '.format(city,time_filter))
    print('-'*80)
    return city, month, day,both

def load_data(city, month, day, both):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # TODO: load data file into a dataframe
    print('Loading data ........')
    df = pd.read_csv(CITY_DATA[city])
    newcol=[]
    for column in df.columns:
        newcol.append(column.replace(' ', '_').lower())
    df.columns = newcol

    
    # TODO: convert the Start Time column to datetime
    df['start_time'] = pd.to_datetime(df['start_time'])

    # TODO: extract month and day of week from Start Time to create new columns
    df['month'] = df['start_time'].dt.month
    df['day_of_week'] = df['start_time'].dt.weekday_name

    if both == True:
        if month != 'all':
            # use the index of the months list to get the corresponding int
            months = MONTHS[month]
            # filter by month to create the new dataframe
            df = df[df['month']==months]
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]   
    
    # TODO: filter by month if applicable
    elif month != "":
        if month != 'all':
            # use the index of the months list to get the corresponding int
            months = MONTHS[month]
            # filter by month to create the new dataframe
            df = df[df['month']==months]
    
    # TODO: filter by day of week if applicable
    elif day != "":
        if day != 'all':
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'] == day.title()]
    
    return df

def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('Calculating User Stats...')
    start_time = time.time()

    # TODO: Display counts of user types
    subscriber= int(df[df['user_type'] == "Subscriber"].user_type.value_counts())
    customer = int(df[df['user_type'] == "Customer"].user_type.value_counts())
    print('\nNo of Subscribers - {}'.format(subscriber))
    print('No of Customers - {}'.format(customer))

    # TODO: Display counts of gender
    while (city!='washington'):
        male= int(df[df['gender'] == "Male"].gender.value_counts())
        female= int(df[df['gender'] == "Female"].gender.value_counts())
        
        print('No of male users - {}'.format(male))
        print('No of female users - {}'.format(female))
        break
        
    # TODO: Display earliest, most recent, and most common year of birth
    while (city!='washington'):
        try:
            oldest_person_age = int(df['birth_year'].min())
            print('Oldest user was born in {}'.format(oldest_person_age))
        except:
            break
            
        youngest_person_age = int(df['birth_year'].max())
        print('Youngest user was born in {}'.format(youngest_person_age))
        common_age= int(df['birth_year'].mode())
        print('Users born in the year {} are the most common users'.format(common_age))
        break
    
    # TODO: calculating the time taken to process this statistics
    print("\nThis calculation took %s seconds to complete." % (time.time() - start_time))
    print('-'*60)
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #TODO: display the most common month
    common_m =int(df['month'].mode()[0])
    common_month = [k for k,v in MONTHS.items() if v == common_m]
    common_month= common_month[0].title()
    print('Biker\'s frequency increases during the monthe of ',common_month)


    # TODO: display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    common_day = common_day.title()
    print('Biker\'s frequency increases on {}\'s'.format(common_day))

    
    # TODO: display the most common start hour
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['hour'] = df['start_time'].dt.hour
    popular_start_hour = df['hour'].mode()[0]
   
    # TODO: converting the popular_start_hour from 24-hr clock to 12-hr clock with AM/PM
    if ((popular_start_hour >=0)&(popular_start_hour<=12)):
        meridiem = "A.M"
    elif ((popular_start_hour >=12)&(popular_start_hour <=24)):
        popular_start_hour = (popular_start_hour-12)
        meridiem = "P.M"
        
    
    print('Most Frequent Start Hour: {} {}'.format(popular_start_hour,meridiem))

    # TODO: calculating the time taken to process this statistics
    print("\nThis calculation took %s seconds to complete." % (time.time() - start_time))
    print('-'*60)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])

    # TODO: display total travel time
    df['duration'] = (df['end_time'] - df['start_time'])
    total_time = df['duration'].sum()
    print('Total trip time is {} '.format(total_time))

    # TODO: display mean travel time
    total_duration = df['trip_duration'].sum()
    row_count= len(df.index)
    mean_min= (total_duration/row_count) / 60
    print('Average time for a trip is {} min  '.format(mean_min))
    
    # TODO: display the longest ride and shortest ride time
    longest_ride= df['trip_duration'].max() / (60*60)
    print('longest ride taken is {} hrs'.format(longest_ride))
    shortest_ride= df['trip_duration'].min() / 60
    print('shortest ride taken is {} min'.format(shortest_ride))
    
    # TODO: calculating the time taken to process this statistics
    print("\nThis calculation took %s seconds to complete." % (time.time() - start_time))
    print('-'*60)
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = str(df['start_station'].mode()[0])
    print('Popular start station is {}'.format(popular_start_station))

    # display most commonly used end station
    popular_end_station = str(df['end_station'].mode()[0])
    print('Popular end station is {}'.format(popular_end_station))

    # display most frequent combination of start station and end station trip
    popular_trip = ('[ ' + df['start_station'] + ' ] & [ ' + df['end_station'] +']').mode()[0]
    print('Most Popular trips are between {} '.format(popular_trip))
    
    
    # TODO: calculating the time taken to process this statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)
    
    
def detail_stats(df,city):
    """Displays detailed statistics on the most popular trips taken."""

    print('\nCalculating detail statistics...\n')
    start_time = time.time()

    # display user stats of the longest ride taken and shortest ride taken
    longest_ride= df['trip_duration'].max() / (60*60)
    user_type_long_ride= df.user_type[df['trip_duration'].idxmax()]
    print('Longest Ride of {} hrs was made by a {}'.format(longest_ride,user_type_long_ride))
    shortest_ride= df['trip_duration'].min() / 60
    user_type_short_ride= df.user_type[df['trip_duration'].idxmin()]
    print('Shortest Ride of {} min was made by a {}'.format(shortest_ride,user_type_short_ride))
    
    # display yongest and the oldest subscriber and customer   
    while (city!='washington'):
        
        subscriber_young= int(df[df['user_type'] == "Subscriber"].birth_year.max())
        customerr_young= int(df[df['user_type'] == "Customer"].birth_year.max())
        print('\nYoungest Subscriber was born in {}'.format(subscriber_young))
        print('Youngest Customer was born in {}'.format(customerr_young))
        
        try:
            subscriber_old= int(df[df['user_type'] == "Subscriber"].birth_year.min())
            customerr_old= int(df[df['user_type'] == "Customerr"].birth_year.min())
            print('Old Subscriber was born in {}'.format(subscriber_old))
            print('Old Customer was born in {}'.format(customer_old))
        except:
            break
            
        break
        
    # display user stats referenced with gender
    while (city!='washington'):
        group_user_stats = df.groupby(['user_type','gender']).size()
        print('\nUser Type divided into Male and female\n',group_user_stats )
        break
   
    # display the longest ride taken from the most popular start station 
    popular_start_station = str(df['start_station'].mode()[0])
    longest_ride = df[df['start_station'] == popular_start_station ].trip_duration.max()
    longest_ride=  longest_ride / 60
    print('\nLongest ride from popular start station \'{}\' is {} min '.format(popular_start_station,longest_ride))
    
    
    # display total travel time of men and women
    while (city!='washington'):
        group_trip_gender_stats = df.groupby('gender').trip_duration.sum()
        print('\nTotal trip duration of Male and female users\n',group_trip_gender_stats)
        break
    
    # TODO: calculating the time taken to process this statistics
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)
    
def display_rawdata(df):
    """Displays raw data from the dataset."""
    for x in range(0,len(df),5):
        continue_display = ''
        five_records = df.iloc[x:x+5]
        print ("\nRecord : {} - {}".format(x+1,x+5))
        for y in range(0,len(five_records)):
            record = five_records.iloc[y]
            print('\n')
            pprint(record)
        
        
        while continue_display not in ['yes','no']:
            continue_display= input('\nShall we continue \'Yes\' or \'No\' ? ').lower()
                                  
        if (continue_display == "yes"):
            continue
        else:
            break
    
            
def main():
    while True:
        city, month, day, both = get_filters()
        df = load_data(city, month, day,both)
        raw_data=''
        restart=''

        # TODO: printing an overview of the data set 
        print(df.head(5))
        print("\n\nTotal no of rows and columns - ",df.shape )

        print('-'*50)
        print('User statistics of {}'.format(city))
        print('-'*50)
        user_stats(df,city)

        print('-'*50)
        print('Time statistics of {}'.format(city))
        print('-'*50)
        time_stats(df)

        print('-'*50)
        print('Trip Duration statistics of {}'.format(city))
        print('-'*50)
        trip_duration_stats(df)

        print('-'*50)
        print('Station statistics of {}'.format(city))
        print('-'*50)
        station_stats(df)
        
        print('-'*50)
        print('Detail statistics on popular rides of {}'.format(city))
        print('-'*50)
        detail_stats(df,city)
        
        while raw_data not in ['yes','no']:
            raw_data = input('\nWould you like to review some raw data ? \'Yes\' or \'No\'\n').lower()
        if raw_data == 'yes':
            display_rawdata(df)
                
        while restart not in ['yes','no']:
            restart = input('\nWould you like to restart? Enter \'yes\' or \'no\' - ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
