import datetime 
# import datetime, timedelta  # type: ignore
from collections import defaultdict
from itertools import groupby

class habit:
    def __init__(self,name,category,frequency,description):
        self.name = name
        self.description = description
        self.category = category
        self.frequency = frequency
        self.logs = [] #list to store completion dates 
     
    def mark_completion(self,date=None):
        if date is None:
            date = datetime.now().date()
        #covert string data into datetime object if needed
        if isinstance(date,str):
            date = datetime.strptime(date, "%Y-%m-5d").date()

        #check if habit is already completed for this time 
        if date not in self.completion_dates:
            self.completion_dates.append(date)
            self.update_streak()
            self.update_streak()
            return True
        return False
    
    def update_streak(self):
        if not self.completion_dates:
            self.update_streak = 0
            return
        
        #sort dates to find consecutive days
        sorted_dates = sorted(self.completion_dates)
        current_streak = 1 
        best_streak = 1

        for i in range(1,len(sorted_dates)):
            #check if current date is consecutive to prevention date
            if (sorted_dates[i] - sorted_dates[i-1]).days ==1:
                current_streak +=1
                best_streak = max(best_streak, current_streak)
            else:
                current_streak = 1

            self.streak = current_streak
            self.best_streak = max(self.best_streak, current_streak)

    def get_completion_rate(self, days=7):
        """
        Method to calculate completion rate for last 'days' days
        Returns percentage of days the habit was completed
        """
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days-1)
        
        completed_days = 0
        for date in self.completion_dates:
            if start_date <= date <= end_date:
                completed_days += 1
        
        return (completed_days / days) * 100
    def __str__(self):
        """
        Special method that defines how the habit object is displayed as a string
        """
        return f"{self.name} ({self.category}): {self.description}"
class HabitTracker:
    def __init__(self):
        """
        Constructor for HabitTracker
        Initializes empty collections to store habits and user data
        """
        self.habits = {}  # Dictionary data type - stores habits with name as key
        self.user_name = ""  # String data type
        self.categories =  [ # List data type - predefined categories
              "Health & Fitness",
              "Learning & Education", 
              "Productivity",
              "Personal Development",
              "Social & Relationships",
              "Hobbies & Recreation"
        
        ]
    def set_user_name(self,name):
        self.user_name = name

    def add_habit(self, name, description, category, target_frequency):
        """
        Method to add a new habit to the tracker
        Demonstrates data validation and error handling
        """
        if name in self.habits:
            return False, "Habit already exists!"
        
        if target_frequency < 1 or target_frequency > 7:
            return False, "Target frequency must be between 1-7 days per week!"
        
        # Create new Habit object and add to dictionary
        new_habit = Habit(name, description, category, target_frequency)
        self.habits[name] = new_habit
        return True, "Habit added successfully!"

    def remove_habit(self, name):
        """
        Method to remove a habit from the tracker
        """
        if name in self.habits:
            del self.habits[name]
            return True, "Habit removed successfully!"
        return False, "Habit not found!"
    
    def mark_habit_complete(self, habit_name, date=None):
        """
        Method to mark a specific habit as completed
        """
        if habit_name not in self.habits:
            return False, "Habit not found!"
        
        success = self.habits[habit_name].mark_complete(date)
        if success:
            return True, f"Habit '{habit_name}' marked as complete!"
        return False, "Habit already completed for this date!"

    def get_habit_statistics(self, habit_name):
        """
        Method to get detailed statistics for a specific habit
        Returns a dictionary with various metrics
        """
        if habit_name not in self.habits:
            return None
        
        habit = self.habits[habit_name]
        stats = {
            "name": habit.name,
            "category": habit.category,
            "total_completions": habit.total_completions,
            "current_streak": habit.streak,
            "best_streak": habit.best_streak,
            "completion_rate_7_days": round(habit.get_completion_rate(7), 2),
            "completion_rate_30_days": round(habit.get_completion_rate(30), 2),
            "created_date": habit.created_date.strftime("%Y-%m-%d"),
            "target_frequency": habit.target_frequency
        }
        return stats
    
    def get_all_habits_summary(self):
        """
        Method to get a summary of all habits
        Demonstrates data processing and analysis
        """
        if not self.habits:
            return "No habits tracked yet!"
        
        summary = []
        for habit_name, habit in self.habits.items():
            stats = self.get_habit_statistics(habit_name)
            summary.append(stats)
        
        return summary

    def get_habits_by_category(self):
        """
        Method to group habits by category
        Demonstrates data organization using dictionaries
        """
        category_groups = defaultdict(list)
        
        for habit_name, habit in self.habits.items():
            category_groups[habit.category].append(habit_name)
        
        return dict(category_groups)
    
    def get_weekly_report(self):
        """
        Method to generate a weekly reportShows completion status for each habit over the last 7 days
        """
        if not self.habits:
            return "No habits to report!"
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=6)
        
        report = f"\n📊 Weekly Report ({start_date} to {end_date})\n"
        report += "=" * 50 + "\n"

        for habit_name, habit in self.habits.items():
            report += f"\n🎯 {habit_name}:\n"
            report += f"   Target: {habit.target_frequency} times/week\n"
            
            # Count completions in the last 7 days
            weekly_completions = 0
            for date in habit.completion_dates:
                if start_date <= date <= end_date:
                    weekly_completions += 1

            # Calculate if target was met
            target_met = "✅" if weekly_completions >= habit.target_frequency else "❌"
            report += f"   Completed: {weekly_completions} times {target_met}\n"
            report += f"   Current Streak: {habit.streak} days\n"
        
        return report
    
    def get_motivational_message(self):
        """
        Method to generate motivational messages based on progress
        Demonstrates conditional logic and user engagement
        """
        if not self.habits:
            return "🌟 Start your journey by adding your first habit!"


        total_habits = len(self.habits)
        total_completions = sum(habit.total_completions for habit in self.habits.values())
        active_streaks = sum(1 for habit in self.habits.values() if habit.streak > 0)
        
        if total_completions == 0:
            return "🚀 You've got this! Mark your first habit completion today!"
        elif total_completions < 10:
            return f"🎯 Great start! You've completed {total_completions} habits. Keep building momentum!"
        elif active_streaks == total_habits:
            return "🔥 Amazing! You're on a streak with ALL your habits! You're unstoppable!"
        else:
            return f"💪 You're doing fantastic! {total_completions} completions across {total_habits} habits!"

class HabitTrackerApp:
    """
    This is the main application class that provides the user interface
    It demonstrates composition (using other classes) and user interaction
    """

    def __init__(self):
        """
        Constructor for the main application
        Creates a HabitTracker instance and sets up the interface
        """
        self.tracker = HabitTracker()
        self.running = True
    
    def clear_screen(self):
        """
        Method to clear the terminal screen for better user experience
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """
        Method to display the main menu options
        """
        print("\n" + "="*60)
        print("🎯 SMART HABIT TRACKER")
        print("="*60)
        if self.tracker.user_name:
            print(f"Welcome back, {self.tracker.user_name}! 👋")
        print("\n📋 MAIN MENU:")
        print("1. 👤 Set User Name")
        print("2. ➕ Add New Habit")
        print("3. ❌ Remove Habit")
        print("4. ✅ Mark Habit Complete")
        print("5. 📊 View Habit Statistics")
        print("6. 📈 View All Habits Summary")
        print("7. 📝 Weekly Report")
        print("8. 🎨 View Habits by Category")
        print("9. 💬 Get Motivational Message")
        print("10. 🚪 Exit")
        print("="*60)
    def get_user_input(self, prompt, input_type=str):
        """
        Method to get user input with type conversion and error handling
        """
        while True:
            try:
                user_input = input(prompt)
                if input_type == int:
                    return int(user_input)
                elif input_type == float:
                    return float(user_input)
                else:
                    return user_input
            except ValueError:
                print(f"❌ Please enter a valid {input_type.__name__}!")
    
    def set_user_name(self):
        """
        Method to set the user's name
        """
        name = self.get_user_input("Enter your name: ")
        self.tracker.set_user_name(name)
        print(f"✅ Welcome, {name}!")

    def add_habit(self):
        """
        Method to add a new habit with user input validation
        """
        print("\n➕ ADD NEW HABIT")
        print("-" * 20)
        
        name = self.get_user_input("Habit name: ")
        description = self.get_user_input("Description: ")
        
        print("\n📁 Available Categories:")
        for i, category in enumerate(self.tracker.categories, 1):
            print(f"{i}. {category}")

        category_choice = self.get_user_input("Choose category (1-6): ", int)
        if 1 <= category_choice <= 6:
            category = self.tracker.categories[category_choice - 1]
        else:
            print("❌ Invalid category choice!")
            return
        
        target_frequency = self.get_user_input("Target frequency (1-7 times per week): ", int)
        
        success, message = self.tracker.add_habit(name, description, category, target_frequency)
        print(f"{'✅' if success else '❌'} {message}")
    
    def remove_habit(self):
        """
        Method to remove a habit
        """
        if not self.tracker.habits:
            print("❌ No habits to remove!")
            return
        
        print("\n❌ REMOVE HABIT")
        print("-" * 15)
        print("Current habits:")
        for name in self.tracker.habits.keys():
            print(f"•{name}")
        habit_name = self.get_user_input("Enter habit name to remove: ")
        success, message = self.tracker.remove_habit(habit_name)
        print(f"{'✅' if success else '❌'} {message}")  

    def mark_habit_complete(self):
        """
        Method to mark a habit as completed
        """
        if not self.tracker.habits:
            print("❌ No habits available!")
            return
        
        print("\n✅ MARK HABIT COMPLETE")
        print("-" * 22)
        print("Available habits:")
        for name in self.tracker.habits.keys():
            print(f"• {name}")
        
        habit_name = self.get_user_input("Enter habit name: ")
        
        # Option to specify date or use today
        use_today = self.get_user_input("Mark for today? (y/n): ").lower() == 'y'
        
        if use_today:
            success, message = self.tracker.mark_habit_complete(habit_name)
        else:
            date_str = self.get_user_input("Enter date (YYYY-MM-DD): ")
            success, message = self.tracker.mark_habit_complete(habit_name, date_str)
        
        print(f"{'✅' if success else '❌'} {message}")
    
    def view_habit_statistics(self):
        """
        Method to display detailed statistics for a specific habit
        """
        if not self.tracker.habits:
            print("❌ No habits available!")
            return
        
        print("\n📊 HABIT STATISTICS")
        print("-" * 18)
        print("Available habits:")
        for name in self.tracker.habits.keys():
            print(f"• {name}")
        
        habit_name = self.get_user_input("Enter habit name: ")
        stats = self.tracker.get_habit_statistics(habit_name)
        
        if stats:
            print(f"\n📈 Statistics for '{stats['name']}':")
            print(f"📁 Category: {stats['category']}")
            print(f"🎯 Target: {stats['target_frequency']} times/week")
            print(f"✅ Total Completions: {stats['total_completions']}")
            print(f"🔥 Current Streak: {stats['current_streak']} days")
            print(f"🏆 Best Streak: {stats['best_streak']} days")
            print(f"📊 7-Day Completion Rate: {stats['completion_rate_7_days']}%")
            print(f"📊 30-Day Completion Rate: {stats['completion_rate_30_days']}%")
            print(f"📅 Created: {stats['created_date']}")
        else:
            print("❌ Habit not found!")
    
    def view_all_habits_summary(self):
        """
        Method to display summary of all habits
        """
        summary = self.tracker.get_all_habits_summary()
        
        if isinstance(summary, str):
            print(f"❌ {summary}")
            return
        
        print("\n📈 ALL HABITS SUMMARY")
        print("=" * 25)
        
        for stats in summary:
            print(f"\n🎯 {stats['name']} ({stats['category']})")
            print(f"   ✅ Completions: {stats['total_completions']}")
            print(f"   🔥 Current Streak: {stats['current_streak']} days")
            print(f"   📊 Weekly Rate: {stats['completion_rate_7_days']}%")
    
    def view_weekly_report(self):
        """
        Method to display the weekly report
        """
        report = self.tracker.get_weekly_report()
        print(report)
    
    def view_habits_by_category(self):
        """
        Method to display habits organized by category
        """
        categories = self.tracker.get_habits_by_category()
        
        if not categories:
            print("❌ No habits available!")
            return
        
        print("\n🎨 HABITS BY CATEGORY")
        print("=" * 22)
        
        for category, habits in categories.items():
            print(f"\n📁 {category}:")
            for habit in habits:
                print(f"   • {habit}")
    
    def show_motivational_message(self):
        """
        Method to display motivational message
        """
        message = self.tracker.get_motivational_message()
        print(f"\n💬 {message}")
    
    def run(self):
        """
        Main method to run the application
        Contains the main program loop
        """
        print("🎯 Welcome to Smart Habit Tracker!")
        print("Track your habits and build positive routines! 🚀")
        
        while self.running:
            self.display_menu()
            choice = self.get_user_input("Enter your choice (1-10): ", int)
            
            if choice == 1:
                self.set_user_name()
            elif choice == 2:
                self.add_habit()
            elif choice == 3:
                self.remove_habit()
            elif choice == 4:
                self.mark_habit_complete()
            elif choice == 5:
                self.view_habit_statistics()
            elif choice == 6:
                self.view_all_habits_summary()
            elif choice == 7:
                self.view_weekly_report()
            elif choice == 8:
                self.view_habits_by_category()
            elif choice == 9:
                self.show_motivational_message()
            elif choice == 10:
                print("👋 Thank you for using Smart Habit Tracker!")
                print("Keep building great habits! 🌟")
                self.running = False
            else:
                print("❌ Invalid choice! Please select 1-10.")
            
            if self.running:
                input("\nPress Enter to continue...")

# Example usage and demonstration
def demonstrate_features():
    """
    Function to demonstrate the key features of the habit tracker
    This shows how the classes work together
    """
    print("🎯 DEMONSTRATION MODE")
    print("=" * 30)
    
    # Create a tracker instance
    tracker = HabitTracker()
    tracker.set_user_name("Demo User")
    
    # Add some sample habits
    tracker.add_habit("Morning Exercise", "30 minutes of cardio", "Health & Fitness", 5)
    tracker.add_habit("Read Books", "Read for 30 minutes", "Learning & Education", 7)
    tracker.add_habit("Meditation", "10 minutes mindfulness", "Personal Development", 3)
    
    # Mark some habits as complete
    tracker.mark_habit_complete("Morning Exercise")
    tracker.mark_habit_complete("Read Books")
    tracker.mark_habit_complete("Meditation")
    
    # Show statistics
    print("\n📊 Sample Statistics:")
    stats = tracker.get_habit_statistics("Morning Exercise")
    print(f"Exercise completions: {stats['total_completions']}")
    
    # Show motivational message
    print(f"\n💬 {tracker.get_motivational_message()}")
    
    print("\n✅ Demo completed! You can now run the main application.")

# Main execution
if __name__ == "__main__":
    """
    This is the main entry point of the program
    It runs when the script is executed directly
    """
    print("🎯 SMART HABIT TRACKER - PYTHON PROJECT")
    print("=" * 45)
    
    choice = input("1. Run Demo\n2. Run Full Application\nChoice: ")
    
    if choice == "1":
        demonstrate_features()
    else:
        # Create and run the main application
        app = HabitTrackerApp()
        app.run()
  
