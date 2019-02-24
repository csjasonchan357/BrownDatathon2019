#This is my code utilizing the TripAdvisor data. In particular, I wanted to use the data to give hotel recommendations to users.
#My program is for users that would like hotel recommendations that specifically people from their own country have booked and have rated highly.
#Specifically, my program asks the user where they are from, what city they are looking for a hotel in (among the available in the TripAdvisor dataset), and what type of hotel they are looking for. The program looks through the dataset and filters according to several factors. 1) It only displays hotels where previous users from the same country have booked the hotel, 2) the hotels must match the city desired, and 3) the hotels must match the hotel type desired. The program returns a list of #the top five Trip-Advisor user-rated locations.
import pandas as pd
import sqlite3

#df = pd.read_csv('full_data.csv')
hotel = pd.read_csv('hotel_data.csv')
activity = pd.read_csv('activity_data.csv')

user_loc = ""
hotel_type = ""
city = ""

def hotel_rec():
    user_loc = input("Where are you from? ")
    if not(user_loc in activity["user_country"].unique()):
        print("Sorry, you there have been no TripAdvisor hotel reviews by people from your country.")
        return

    print("The available hotel city locations you may choose from are: ")
    for typ in hotel["city_name"].unique():
        print(typ, end=', ')
    city = input("Which city are you looking for a hotel in? ")
    if not(city in hotel["city_name"].unique()):
        print("Sorry, you did not enter a valid city!")
        return

    print("The available hotel types are: ")
    for typ in hotel["hotel_type"].unique():
        print(typ, end=", ")
    hotel_type = input("What hotel type do you want?" )
    if not(hotel_type in hotel["hotel_type"].unique()):
        print("Sorry, you did not enter a valid hotel type!")
        return

    make_recommendation(user_loc, hotel_type, city)

def make_recommendation(location, hotel_type, city):
    print('')
    print('Hello, thank you for using our hotel recommendation service.')
    print('Below are the top hotels rated by users from your country, according to your criteria:')
    print('Results are listed as (Hotel Name, TripAdvisor Rating /50)')
    conn = sqlite3.connect("data.db")
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS "activity";')
    c.execute('DROP TABLE IF EXISTS "hotels";')
    conn.commit()

    hotel.to_sql("hotel_table", con = conn, if_exists = 'replace')
    activity.to_sql("activity_table", con = conn, if_exists = 'replace')

    t=(hotel_type, city, location)
    c.execute(
        "SELECT h.hotel_name, h.bubble_score\
        FROM activity_table AS a  \
        LEFT OUTER JOIN hotel_table AS h\
        ON h.hotel_id == a.hotel_id \
        WHERE a.user_action == 'booking' AND h.hotel_type = ? AND h.city_name = ? AND a.user_country = ?\
        GROUP BY h.hotel_name ORDER BY h.bubble_score DESC LIMIT 5",t)
    ans = c.fetchall()
    if len(ans) == 0:
        print("Sorry, there are no matching hotels.")
    else:
        for i in ans:
            print(i)
    print('END')

hotel_rec()
