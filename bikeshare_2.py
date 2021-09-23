import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    cities=["chicago", "new york city", "washington"]
    
    city = input("Enter a city from the list {}, {}, or {}: ".format(cities[0], cities[1], cities[2])).lower()
    
    while city not in cities:
        city = input("Please make sure to enter a city from the list {}, {}, or {}: ".format(cities[0], cities[1], cities[2])).lower()

    
    months = ["all", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    
    month = input("Enter a month eg january, or all to select all months: ").lower()
    
    while month not in months:
        month = input("Please check your spelling and enter a month eg january, or all to select all months: ").lower()

    
    days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    
    day = input("Enter a day of the week eg tuesday, or all to select all days: ").lower()
    
    while day not in days:
        day = input("Please check your spelling and enter a day of the week eg tuesday, or all to select all days: ").lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    file= CITY_DATA.get(city)
    
    
    df=pd.read_csv(file)
    
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    
    if month != 'all':
        
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1

        
        df = df[df['month'] == month]

    
    if day != 'all':
        
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print("\nThe most common month is: ", popular_month)

    
    df['day'] = df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0]
    print("\nThe most common day is: ", popular_day)

    
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("\nThe most common hour is: ", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    
    start_station = df['Start Station'].mode()[0]
    print("\nMost commonly used start station: ", start_station)

    
    end_station = df['End Station'].mode()[0]
    print("\nMost commonly used end station: ", end_station)


    
    combo = df.groupby(['Start Station','End Station']).size().idxmax()
    print("\nMost frequent combination of start station and end station trip: ", combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    
    df['Travel Time'] = df['End Time'] - df['Start Time']
    
    
    total_time = df['Travel Time'].sum()
    print("\nTotal travel time: ", total_time)

    
    mean_time = df['Travel Time'].mean()
    print("\nMean travel time: ", mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    
    user_types = df['User Type'].value_counts()
    print("\nCounts of user types: ", user_types)

    
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print("\nCounts of gender: ", gender)
    else:
        print("\nGender stats cannot be calculated because Gender does not appear in the dataframe")

    
    if 'Birth Year' in df:
        common_year = df['Birth Year'].mode()[0]
        earliest_year = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        print("\nEarliest:{}, most recent: {}, and most common year of birth: {}".format(earliest_year, most_recent, common_year))
    else:
        print("\nBirth year stats cannot be calculated because Birth Year does not appear in the dataframe")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_data(df):
    """Prints Raw Data for bikeshare users."""
    
    data_length = len(df)
    end = 10
    start = 0
    
    
    while end<=data_length:
        
        view_data = input("Would you like to view 5 rows of trip data? Enter yes or no").lower()
        
        
        if view_data != 'yes' and view_data != 'no':
            view_data = input("Would you like to view 5 rows of trip data? Please make sure to only enter yes or no").lower()
            
        
        elif view_data == 'yes':
            print(df.iloc[start:end])
            start+=5
            
            
            if (data_length-start)<5:
                end=data_length
            
            else:
                end+=5
                
                 
        else:
            break
        
        print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()
