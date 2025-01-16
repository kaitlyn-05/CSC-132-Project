import random

class Goal:
    # Initializes goal object with a name aswell as the description
    def __init__(self,goal_name, description):
        self.goal_name = goal_name
        self.description = description
        self.milestones = []
        self.completed_milestones = 0
        self.total_milestones = 0
    # This function adds a new milestone to the list of milestones specifically
    def new_milestone(self, milestone_name):
        self.milestones.append({"milestone_name": milestone_name, "completed": False})
        self.total_milestones += 1
    # This function checks if all lessons are completed before the final project can be completed
    def milestone_completion(self, milestone_name):
        # once it gets to 'Complete Final Project' this make sure all lessons are completed beforehand
        if milestone_name == "Complete Final Project":
            if not self.can_complete_final_project():
                print(f"\nYou Cannot Complete '{milestone_name}'. All lessons must be completed first. \n")
                return
        # This checks if the milestone is already completed
        for milestone in self.milestones:
            if milestone["milestone_name"] == milestone_name:
                if milestone["completed"]:
                    print(f"\nMilestone '{milestone_name}' is already completed.\n")
                    return
                milestone["completed"] = True
                self.completed_milestones += 1  
                print(f"\nMilestone '{milestone_name}' completed!\n")
                self.motivational_quotes()
                break
            else:
                print(f"\nMilestone'{milestone_name}' not found.")

    def can_complete_final_project(self):
        # making sure the prior lessons are completed before allowing the final project to be completed
        for milestone in self.milestones:
            if "Lesson" in milestone["milestone_name"] and not milestone["completed"]:
                print(f"\nCannot complete Final Project. '{milestone['milestone_name']}' is not completed yet.")
                return False
        return True 
    # Returns the current progress as a percentage of the completed milestones
    def Progress_Tracker(self):
        progress_percentage = (self.completed_milestones / self.total_milestones) * 100
        return f"Progress: {self.completed_milestones}/{self.total_milestones} milestones completed ({progress_percentage:.2f}%)"
    # Displays all the milestones aswell as their completion status    
    def goal_display(self):
        print(f"\nGoal: {self.goal_name}")
        print(f"Description: {self.description}")
        print("Milestones:")
        for milestone in self.milestones:
            status = "Completed" if milestone["completed"] else "Not Completed"
            print(f"- {milestone['milestone_name']} ({status})")

    def motivational_quotes(self):
        quotes = [
            "Education is the passport to the future, for tomorrow belongs to those who prepare for it today.-Malcolm X"
            "A person who never made a mistake never tried anything new. - Albert Einstein"
            "Procrastination makes easy things hard and hard things harder. - Mason Cooley"
            "I find that the harder I work, the more luck I seem to have. - Thomas Jefferson"
            "The best way to predict your future is to create it. - Abraham Lincoln"
            "Don't let what you cannot do interfere with what you can do. - John Wooden"
            "The way to get started is to quit talking and begin doing. - Walt Disney"]
        print(random.choice(quotes))

def main():

    my_goal = Goal("Finish Python Course", "Complete all lessons and practice exercises")

    my_goal.new_milestone("Lesson 1")
    my_goal.new_milestone("Lesson 2")
    my_goal.new_milestone("Lesson 3")
    my_goal.new_milestone("Complete Final Project")

    my_goal.goal_display()

    milestones = ["Complete Lesson 1", "Complete Lesson 2", "Complete Lesson 3", "Complete Final Project"]

    for milestone in milestones:
        my_goal.milestone_completion(milestone)

    print(my_goal.Progress_Tracker())

                

    my_goal.goal_display()

main()

