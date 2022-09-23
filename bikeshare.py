import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months=["jan", "feb", "mar", "apr", "may", "jun"]
months_long=['January','February','March','April','May','June']
days=['mon','tue','wed','thu','fri','sat','sun']
days_long=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
yes_no_respnses=['y','n']
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = input('Please choose one of those cities to explore its data (Chicago, New York City, Washington): ' ).lower()
        if city in CITY_DATA:
            break
        else:
            print('Please choose a valid city.')
    # get user input for month (all, january, february, ... , june)
    while True:
        filter_bymonth = input('Do you wanna filter the data by month? (y/n)? ').lower()
        if filter_bymonth == "":
            print('Please choose a valid response.')
        elif filter_bymonth[0] in yes_no_respnses:
            break
        else:
            print('Please choose a valid response.')
    if  filter_bymonth[0] == 'y':
        while True:
            month=input('Please choose the month you wanna filter with (Jan, Feb, Mar, Apr, May, Jun): ' ).lower()
            if  month == "":
                print('Please choose a valid month.')
            elif month[:3] in months:
                break
            else:
                print('Please choose a valid month.')
    else:
        month='non'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        filter_byday=input('Do you wanna filter the data by day? (y/n)? ').lower()
        if filter_byday == "":
            print('Please choose a valid response.')
        elif filter_byday[0] in yes_no_respnses:
            break
        else:
            print('Please choose a valid response.')
    if  filter_byday[0] == 'y':
        while True:
            day=input('Please choose the month you wanna filter with (Sun, Mon, Tue, Wed, Thu, Fri, Sat): ' ).lower()
            if day == "":
                print('Please choose a valid day.')
            elif day[:3] in days:
                break
            else:
                print('Please choose a valid day.')
    else:
        day='non'
    print('-'*40)
    return city, month[:3], day[:3]


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
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['hour'] = df['Start Time'].dt.hour
    df['month'] = df['Start Time'].dt.month
    df['day'] = df['Start Time'].dt.dayofweek
    if month != 'non':
        month = months.index(month)+1
        df=df[df['month']==month]
    if day != 'non':
        day = days.index(day)
        df=df[df['day']==day]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if len(df['month'].unique()) > 1:
        mc_month = months_long[df['month'].mode().sum()-1]
        print(f"Most common month is: {mc_month}; {(df['month'].value_counts().loc[[df['month'].mode().sum()]].values[0]*100)//df['month'].count()}% of the rides was in {mc_month}\n")

    # display the most common day of week
    if len(df['day'].unique()) > 1:
        mc_day = days_long[df['day'].mode().sum()]
        print(f"Most common day is: {mc_day}, {(df['day'].value_counts().loc[[df['day'].mode().sum()]].values[0]*100)//df['day'].count()}% of the rides was in {mc_day}\n")

    # display the most common start hour
    mc_hour= df['hour'].mode()[0]
    print(f"Most common start hour is: {mc_hour}:00, {(df['hour'].value_counts().loc[[df['hour'].mode().sum()]].values[0]*100)//df['hour'].count()}% of the rides started around {mc_hour}:00")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mc_start_station = df['Start Station'].mode()[0]
    print(f"Most commonly used start station is {mc_start_station}, it got used {df['Start Station'].str.count(df['Start Station'].mode()[0]).sum()} times; {(df['Start Station'].str.count(df['Start Station'].mode()[0]).sum()*100)//df['Start Station'].count()}% of the trips started at {mc_start_station}\n")

    # display most commonly used end station
    mc_end_station = df['End Station'].mode()[0]
    print(f"Most commonly used end station is {mc_end_station}, it got used {df['End Station'].str.count(df['End Station'].mode()[0]).sum()} times; {(df['End Station'].str.count(df['End Station'].mode()[0]).sum()*100)//df['End Station'].count()}% of the trips ended at {mc_end_station}\n")

    # display most frequent combination of start station and end station trip
    comb_start_station, comb_end_station=((df['Start Station'] + ' , ' + df['End Station']).mode()[0].split(' , '))
    df_start=df[df['Start Station'] == comb_start_station]
    df_end=df[df['End Station'] == comb_end_station]
    df_start_end=df_start[df_start['End Station'] == comb_end_station]
    print(f'The most reoccuring trip starts from {comb_start_station} and ends at {comb_end_station}\n{((df_start_end.count()*100)//df_start.count())[4]}% of the trips started at {comb_start_station} ended at {comb_end_station}\n{((df_start_end.count()*100)//df_end.count())[5]}% of the trips ended at {comb_end_station} started at {comb_start_station}.')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time=df['Trip Duration'].sum()
    total_hours=total_time//3600
    remainder_min=(total_time%3600)//60
    remainder_sec=(total_time%3600)%60
    mean_time=df['Trip Duration'].mean()
    mean_hours=int(mean_time//3600)
    remainder_mean_min=int((mean_time%3600)//60)
    remainder_mean_sec=int((mean_time%3600)%60)
    print(f"Total travel time is {total_hours} hours, {remainder_min} minutes, and {remainder_sec} seconds.")

    # display mean travel time
    print(f"Total travel time is {mean_hours} hours, {remainder_mean_min} minutes, and {remainder_mean_sec} seconds.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types=""
    for i in range(len(df['User Type'].dropna(axis=0).unique())):
        user_types += f" {df['User Type'].dropna(axis=0).unique()[i]} count are {df['User Type'].dropna(axis=0).str.count(df['User Type'].dropna(axis=0).unique()[i]).sum()}.\n"
    print(user_types)

    # Display counts of gender
    if 'Gender' in df:
        user_gender=""
        for i in range(len(df['Gender'].dropna(axis=0).unique())):
            user_gender += f" {df['Gender'].dropna(axis=0).unique()[i]} count are {df['Gender'].dropna(axis=0).str.count(df['Gender'].dropna(axis=0).unique()[i]).sum()}.\n"
        print(user_gender)
    else:
        print("Gender data isn't avilable for this city")

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:

        earliest_year=int(df['Birth Year'].min().sum())
        recent_year=int(df['Birth Year'].max().sum())
        mc_year=int(df['Birth Year'].mode()[0])
        print(f"Earliest year is {earliest_year}.\nMost recent year is {recent_year}.\nMost common year is {mc_year}.")

    else:
        print("Birth year data isn't avilable for this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df  = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        while True:
            raw_data = input('Do you want to see a sample of the Raw data? (y/n)? ').lower()
            if raw_data == "":
                print('Please choose a valid response.')
            elif raw_data[0] in yes_no_respnses:
                break
            else:
                print('Please choose a valid response.')
        if raw_data[0] == 'y':
            i , j = 0 , 5
            while raw_data[0] == 'y':
                if j>len(df):
                    print(df[i:])
                    print('This is the last page.')
                    break
                else:
                    print(df[i:j])
                    i+=5
                    j+=5
                    while True:
                        raw_data = input('Do you want to see 5 more rows from the Raw data? (y/n)? ').lower()
                        if raw_data == "":
                            print('Please choose a valid response.')
                        elif raw_data[0] in yes_no_respnses:
                            break
                        else:
                         print('Please choose a valid response.')
        while True:
            restart=input('\nWould you like to restart? (y/n)? ').lower()
            if restart == "":
                print('Please choose a valid response.')
            elif restart[0] in yes_no_respnses:
                break
            else:
                print('Please choose a valid response.')
        if  restart[0] == 'n':
            break


if __name__ == "__main__":
	main()
