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
    while True:
        city = str(input("Would you like to explore bike data from chicago, new york city, or washington?\n")).lower()

        if city.lower() not in ('chicago', 'new york city', 'washington'):
            print("Not one of the cities listed!")
            continue

        else:
            print ("Awesome Choice!")
            #correctly typed in chicago, new york city, or washington
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Any specific month or all? Please type the full month name or type all\n").lower()

        if month.lower() not in ('january','february','march','april','may','june','all'):
            print("Not a valid month!")
            continue

        else:
            print ("OK!")
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Any specific days or all? Please type the full day name or type all\n").lower()

        if day.lower() not in ('monday','tuesday','wednesday','thursday','friday','saturday','sunday','all'):
            print("Not a valid day!")
            continue
        else:
            print ("Done!")
            break

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
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

    # display the most common month
    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    popular_month = months[int(popular_month) - 1]
    print ('The most common month is:' + ' ' + str(popular_month).title())

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print ('The most common day is:' + ' ' + str(popular_day))
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most common hour is:' + ' ' + str(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start = df['Start Station'].mode()[0]
    print ('The most commonly used start station is:' + ' ' + str(popular_start))

    # display most commonly used end station
    popular_end = df['End Station'].mode()[0]
    print ('The most commonly used end station is:' + ' ' + str(popular_end))

    # display most frequent combination of start station and end station trip
    frequent = df.groupby(['Start Station', 'End Station']).size()
    frequent = df.groupby(["Start Station", "End Station"]).size().reset_index(name="Count")
    sorted_values = frequent.sort_values(by=['Count']).iloc[-1:]

    print ('The most frequent combination of start station and end station with the count:\n')
    print (sorted_values)

    #how do i do this in a better way?
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum(axis=0)
    print ('The total travel time is:' + ' ' + str(total_time))
    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print ('The total mean time is:' + ' ' + str(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    while True:
        try:
    # Display counts of user types
            user_types = df['User Type'].value_counts()
            print (user_types)
        except KeyError:
            print ('Oops! No user data found!')
        try:
    # Display counts of gender
            gender = df['Gender'].value_counts()
            print (gender)
        except KeyError:
            print ('Oops! No gender data found!')
        try:
    # Display earliest, most recent, and most common year of birth
            earliest_years = df['Birth Year'].min()
            print ('Earliest Birthday Year:' + ' ' + str(earliest_years))
            most_recent = df['Birth Year'].max()
            print ('Most Recent Birthday Year:' + ' ' + str(most_recent))
            most_common = df['Birth Year'].mode()[0]
            print ('Most Common Birthday Years:' + ' ' + str(most_common))
            break
        except KeyError:
            print ("Oops! No birthday data found!")
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
        answer = str(input("Do you want to see the raw data? Yes or No? \n")).lower()
        if answer == "no":
            return
        elif answer == "yes":
            print (df.iloc[0:5])
            x = 0
            while True:
                repeat = str(input("Do you want to see 5 more lines of raw data? Yes or No? \n")).lower()
                if repeat == "yes":
                    print (df.iloc[(5 + x):(10 + x)])
                    x += 5
                elif repeat == "no":
                    break
                else:
                    print ("Please type yes or no!")
        else:
            print ("Please type yes or no!")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
