import os
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
class Booking:
    def __init__(self, movie, screen, timeslot, booked_seats, user):
        self.movie = movie
        self.screen = screen
        self.timeslot = timeslot
        self.booked_seats = booked_seats
        self.user = user

    def available_seats(self):
        return 50 - len(self.booked_seats)


class Movie:
    def __init__(self, title, duration, screen_number, available_seats):
        self.title = title
        self.duration = duration
        self.screen_number = screen_number
        self.available_seats = available_seats

    def __str__(self):
        return f"{self.title} ({self.duration} mins) - Screen: {self.screen_number}, Available Seats: {self.available_seats}"

class Screen:
    def __init__(self, number):
        self.number = number

class BookingSystem:
    def __init__(self):
        self.logged_in_user = None
        self.movies = []
        self.screens = []
        self.bookings_file = "booking_details.txt"
        self.movies_file = "movies.txt"
        self.load_bookings()
        self.load_movies()
        self.bookings = []

    def load_movies(self):
        try:
            if not os.path.exists(self.movies_file):
                with open(self.movies_file, "w"):  # Create the file if it doesn't exist
                    pass
            with open(self.movies_file, "r") as file:
                for line in file:
                    parts = line.strip().split(", ")
                    # Process each line to load movie data
        except FileNotFoundError:
            print("Movies file not found. Starting with an empty movie list.")

    def save_movies(self):
        with open(self.movies_file, "w") as file:
            for movie in self.movies:
                file.write(f"{movie.title}, {movie.duration}, {movie.screen_number}, {movie.available_seats}\n")
    def add_movie(self):
        title = input("Enter the title of the movie: ")
        duration = int(input("Enter the duration of the movie (in minutes): "))
        screen_number = int(input("Enter the screen number: "))
        available_seats = int(input("Enter the number of available seats: "))

        new_movie = Movie(title, duration, screen_number, available_seats)
        self.movies.append(new_movie)
        self.save_movies()
        print(f"Movie '{title}' added successfully!")
    def remove_movie(self):
        title = input("Enter the title of the movie to remove: ")
        found_movie = None
        for movie in self.movies:
            if movie.title == title:
                found_movie = movie
                break
        if found_movie:
            self.movies.remove(found_movie)
            self.save_movies()
            print(f"Movie '{title}' removed successfully!")
        else:
            print("Movie not found.")

    def load_bookings(self):
        try:
            if not os.path.exists(self.bookings_file):
                with open(self.bookings_file, "w"):  # Create the file if it doesn't exist
                    pass
            with open(self.bookings_file, "r") as file:
                for line in file:
                    parts = line.strip().split(", ")
                    movie_title = parts[0].split(": ")[1]
                    screen_number = int(parts[1].split(": ")[1])
                    timeslot = parts[2].split(": ")[1]
                    booked_seats = list(map(int, parts[3].split(": ")[1].split(",")))
                    username = parts[4].split(": ")[1]
                    found_movie = None
                    for movie in self.movies:
                        if movie.title == movie_title:
                            found_movie = movie
                            break
                    if found_movie:
                        found_screen = None
                        for screen in self.screens:
                            if screen.number == screen_number:
                                found_screen = screen
                                break
                        if found_screen:
                            user = User(username, "")  # Placeholder for user, password not needed for booking
                            booking = Booking(found_movie, found_screen, timeslot, booked_seats, user)
                            self.bookings.append(booking)
        except FileNotFoundError:
            print("Booking details file not found. Starting with an empty booking list.")

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username == "admin" and password == "adminpass":
            self.logged_in_user = Admin(username, password)
            print("Logged in as admin.")
        else:
            self.logged_in_user = User(username, password)
            print("Logged in as user.")

    def load_movies(self):
        try:
            with open("movies.txt", "r") as file:
                for line in file:
                    parts = line.strip().split(", ")
                    title = parts[0]
                    duration = int(parts[1])
                    screen_number = int(parts[2])
                    available_seats = int(parts[3])
                    self.movies.append(Movie(title, duration, screen_number, available_seats))
        except FileNotFoundError:
            print("Movies file not found. Starting with an empty movie list.")

    def add_initial_data(self):
        initial_movies = [
            ("The Avengers", 150, 1, 50),
            ("Inception", 148, 2, 45),
            ("Pulp Fiction", 154, 3, 40),
            ("Interstellar", 169, 4, 55),
            ("The Godfather", 175, 5, 48)
        ]
        for data in initial_movies:
            self.movies.append(Movie(*data))
        
        self.save_movies()

    def book_ticket(self):
        print("\nAvailable Movies:")
        for movie in self.movies:
            print(movie)
        movie_title = input("\nEnter the title of the movie you want to book: ")
        found_movie = None
        for movie in self.movies:
            if movie.title == movie_title:
                found_movie = movie
                break
        if found_movie:
            print(f"Available screenings for {found_movie.title}:")
            print(f"Screen: {found_movie.screen_number}, Available Seats: {found_movie.available_seats}")
            screen_number = found_movie.screen_number
            num_seats = int(input("Enter the number of seats you want to book: "))
            if found_movie.available_seats >= num_seats:
                found_movie.available_seats -= num_seats
                username = input("Enter your username: ")  # Get username from the user
                booking = Booking(found_movie, Screen(screen_number), "", list(range(1, num_seats + 1)), User(username, ""))  # Create a new booking with the user's username
                self.bookings.append(booking)  # Add the booking to the list of bookings
                print("Tickets booked successfully!")
                self.save_movies()  # Save the updated movie data
            else:
                print("Not enough seats available.")
        else:
            print("Movie not found.")
    def save_bookings(self):
        with open(self.bookings_file, "w") as file:
            for booking in self.bookings:
                file.write(f"{booking.movie.title}, Screen: {booking.screen.number}, Time: {booking.timeslot}, Booked Seats: {booking.booked_seats}, User: {booking.user.username}\n")

    def cancel_booking(self):
        username = input("\nEnter your username: ")
        for booking in self.bookings:
            if booking.user.username == username:
                print(f"Booking found for {username}:")
                print(f"Movie: {booking.movie.title}, Screen: {booking.screen.number}, Time: {booking.timeslot}, Booked Seats: {booking.booked_seats}")
                cancel_confirmation = input("Do you want to cancel this booking? (yes/no): ")
                if cancel_confirmation.lower() == "yes":
                    self.bookings.remove(booking)  # Remove booking from in-memory list
                    self.save_bookings()  # Save updated bookings to file
                    print("Booking canceled successfully!")
                    return
                else:
                    print("Booking cancellation aborted.")
                    return
        print("No booking found for this user.")
    def admin_actions(self):
        while True:
            print("\nAdmin Actions:")
            print("1. Add Movie")
            print("2. Remove Movie")
            print("3. View Current Movies")
            print("4. Logout")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.add_movie()
            elif choice == "2":
                self.remove_movie()
            elif choice == "3":
                self.view_movies()
            elif choice == "4":
                print("Logging out.")
                break
            else:
                print("Invalid choice. Please try again.")

    def user_actions(self):
        while True:
            print("\nUser Actions:")
            print("1. Book Ticket")
            print("2. Cancel Booking")
            print("3. View Current Movies")
            print("4. Logout")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.book_ticket()
            elif choice == "2":
                self.cancel_booking()
            elif choice == "3":
                self.view_movies()
            elif choice == "4":
                print("Logging out.")
                break
            else:
                print("Invalid choice. Please try again.")

    def view_movies(self):
        print("\nAvailable Movies:")
        for movie in self.movies:
            print(movie)

    def run(self):
        self.load_movies()
        self.add_initial_data()
        print("Welcome to the Booking System!")
        while True:
            if not self.logged_in_user:
                self.login()  # Prompt for login if no user is logged in
            else:
                if isinstance(self.logged_in_user, Admin):
                    self.admin_actions()
                else:
                    self.user_actions()
            logout_choice = input("Do you want to logout? (yes/no): ")
            if logout_choice.lower() == "yes":
                print("Logging out.")
                self.logged_in_user = None 

if __name__ == "__main__":
    booking_system = BookingSystem()
    booking_system.run()
