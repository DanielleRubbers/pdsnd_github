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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities=["chicago", "new york city", "washington"]
    
    city = input("Enter a city from the list {}, {}, or {}: ".format(cities[0], cities[1], cities[2])).lower()
    
    while city not in cities:
        city = input("Please make sure to enter a city from the list {}, {}, or {}: ".format(cities[0], cities[1], cities[2])).lower()

    # get user input for month (all, january, february, ... , june)
    months = ["all", "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    
    month = input("Enter a month eg january, or all to select all months: ").lower()
    
    while month not in months:
        month = input("Please check your spelling and enter a month eg january, or all to select all months: ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
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
    #find the file name
    file= CITY_DATA.get(city)
    
    #get the csv file
    df=pd.read_csv(file)
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    #get the month and the day of the week from Start Time
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    #convert dates in table to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]
    print("\nThe most common month is: ", popular_month)

    # display the most common day of week
    df['day'] = df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0]
    print("\nThe most common day is: ", popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("\nThe most common hour is: ", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("\nMost commonly used start station: ", start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("\nMost commonly used end station: ", end_station)


    # display most frequent combination of start station and end station trip
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
    
    #travel time
    df['Travel Time'] = df['End Time'] - df['Start Time']
    
    # display total travel time
    total_time = df['Travel Time'].sum()
    print("\nTotal travel time: ", total_time)

    # display mean travel time
    mean_time = df['Travel Time'].mean()
    print("\nMean travel time: ", mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("\nCounts of user types: ", user_types)

    # Display counts of gender
    if 'Gender' in df:
        gender = df['Gender'].value_counts()
        print("\nCounts of gender: ", gender)
    else:
        print("\nGender stats cannot be calculated because Gender does not appear in the dataframe")

    # Display earliest, most recent, and most common year of birth
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
    
    #while the last requested column is less than or equal to the number of rows in the dataframe
    while end<=data_length:
        
        view_data = input("Would you like to view 10 rows of trip data? Enter yes or no").lower()
        
        #make sure response is valid
        if view_data != 'yes' and view_data != 'no':
            view_data = input("Would you like to view another 10 rows of trip data? Please make sure to only enter yes or no").lower()
            
        #if the user wants to see data, print the rows between the start row number and end row number-1
        elif view_data == 'yes':
            print(df.iloc[start:end])
            start+=5
            
            #in case the number of rows in total isn't divisible by 5, set the end value to the number of the last row
            if (data_length-start)<5:
                end=data_length
            #in all other cases, just increment the value by 5
            else:
                end+=5
                
        #if no is selected break out of the loop          
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
