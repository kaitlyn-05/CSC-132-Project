import random

class Goal:
    def __init__(self,goal_name, description):
        self.goal_name = goal_name
        self.description = description
        self.milestones = []
        self.completed_milestones = 0
        self.total_milestones = 0

    def new_milestone(self, milestone_name):
        self.milestones.append({"milestone_name": milestone_name, "completed": False})
        self.total_milestones += 1

    def milestone_completion(self, milestone_name):

        if milestone_name == "Complete Final Project":
            if not self.can_complete_final_project():
                print(f"\nYou Cannot Complete '{milestone_name}'. All lessons must be completed first. \n")
                return

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

    def Progress_Tracker(self):
        progress_percentage = (self.completed_milestones / self.total_milestones) * 100
        return f"Progress: {self.completed_milestones}/{self.total_milestones} milestones completed ({progress_percentage:.2f}%)"
            
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