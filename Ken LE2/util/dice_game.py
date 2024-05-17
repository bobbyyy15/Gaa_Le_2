import os
import time
import random
from util.score import Score

class DiceGame:
    def __init__(self, username):
        self.username = username
        self.score_folder = "scores"
        self.score_file = os.path.join(self.score_folder, "rankings.txt")
        self.create_score_folder()
        self.score = Score(self.username, "")

    def create_score_folder(self):
        if not os.path.exists(self.score_folder):
            os.makedirs(self.score_folder)

    def load_scores(self):
        try:
            with open(self.score_file, "r") as file:
                scores = []
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) == 4:
                        username, points, wins, game_id = parts
                        scores.append((username, int(points), int(wins), game_id))
                return scores
        except FileNotFoundError:
            return []

    def save_scores(self, scores):
        with open(self.score_file, "w") as file:
            for record in scores:
                file.write(",".join(map(str, record)) + "\n")

    def continue_game(self):
        while True:
            cont = input("\nDo you want to continue to the next stage? (1 for Yes, 0 for No): ")
            if cont in {"0", "1"}:
                return cont == "1"
            print("Invalid input. Please enter 1 for Yes or 0 for No")
            input("Press Enter to Continue...")

    def play_game(self):
        print(f"Starting game as {self.username}...")
        time.sleep(1)
        stage_wins = 0
        user_total_points = 0

        while stage_wins < 3:
            cpu_total_points = 0
            user_pts, cpu_pts = 0, 0

            print("\n--- Stage {} ---".format(stage_wins + 1))

            for _ in range(3):
                cpu_roll, user_roll = random.randint(1, 6), random.randint(1, 6)
                print(f"\n{self.username} rolled: {user_roll}")
                time.sleep(1)
                print(f"CPU rolled: {cpu_roll}")
                time.sleep(1)

                if cpu_roll < user_roll:
                    user_pts += 1
                    print(f"\nYou win this round, {self.username}!")
                elif cpu_roll > user_roll:
                    cpu_pts += 1
                    print("\nCPU wins this round!")
                else:
                    print("\nIt's a tie!")

                time.sleep(1)

            if user_pts > cpu_pts:
                stage_wins += 1
                user_total_points += 3 + user_pts
                print(f"\nOverall result: {self.username} wins stage {stage_wins}!")
                print(f"Total Points: {user_total_points}, Stages Won: {stage_wins}")
            elif cpu_pts > user_pts:
                print(f"\nOverall result: CPU wins stage {stage_wins + 1}.")
            else:
                print("\nOverall result: It's a tie! No winner for this stage.")
            
            if stage_wins == 3 or not self.continue_game():
                scores = self.load_scores()
                scores.append(self.score.to_record())
                scores = sorted(scores, key=lambda x: x[1], reverse=True)[:10]
                self.save_scores(scores)
                self.score.reset_overall_score()
                print(f"\nGame Over. You won {stage_wins} stage{'s' if stage_wins > 1 else ''}.")
                break
            
            time.sleep(1)


    def show_top_scores(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Top Scores:\n")
        scores = self.load_scores()
        if not scores:
            print("No games played yet. Play a game to see top scores.")
        else:
            for index, (username, points, wins, date) in enumerate(scores, start=1):
                print(f"{index}. {username}: Points - {points}, Wins - {wins} (Achieved on: {date})")
        input("\nPress Enter to Continue...")

    def logout(self): 
        print(f"\nGoodbye, {self.username}\nYou logged out successfully")
        time.sleep(1)
        return True

    def menu(self):
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print(f"Welcome, {self.username}\nMenu:\n1. Start Game\n2. Show Top Scores\n3. Log Out")
            choice = input("\nEnter the number of your choice: ")
            if choice == "1":
                self.play_game()
            elif choice == "2":
                self.show_top_scores()
            elif choice == "3":
                if self.logout() == True:
                    return
            else:
                print("\nInvalid choice. Please Try Again")
                time.sleep(1)
                continue
