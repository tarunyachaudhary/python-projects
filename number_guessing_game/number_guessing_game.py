import random
from pathlib import Path
import json
from abc import ABC, abstractmethod

try:
    from generate_json_data import generate_user_json_data
except ModuleNotFoundError as error:
    if error.name != "reportlab":
        raise
    generate_user_json_data = None


class Play_game:
    # generate random number
    def generateRandomNumber(self):
        return random.randint(1, 100)

    def playGame(self):

        randomNumber = self.generateRandomNumber()
        attempt = 0

        print("Guess number between 1 to 100.")

        while True:
            try:
                userInput = int(input("Enter your guess --->  "))

                if not 1 <= userInput <= 100:
                    print("Guess a number between 1 and 100.")
                    continue

                attempt += 1

                if userInput == randomNumber:
                    print(f"🎉congrats!you guessed the number in {attempt} attempts.")
                    break
                elif userInput > randomNumber:
                    print("😞oops!Choose a lower number!")
                else:
                    print("😞oops!Choose a higher number!")
            except ValueError:
                print("Invalid input!Please enter a valid input.")

        return attempt


class Text_file_data(ABC):
    @abstractmethod
    def read_text_history(self) -> dict[str, int]:
        pass

    @abstractmethod
    def update_user_score_text_file(self) -> None:
        pass


class Text_concrete_class(Text_file_data):

    def __init__(self, game):
        self.game = game
        self.path_text_file = Path(__file__).resolve().parent / "game_history.txt"

    def read_text_history(self):
        data = {
            "previous_score": 0,
            "highest_score": 0,
            "lowest_score": 0,
            "games_played": 0,
        }
        if not self.path_text_file.exists():
            return data

        with open(self.path_text_file, "r") as file:
            for line in file:
                if ":" in line:
                    key, value = line.strip().split(":", 1)
                    key = key.strip().replace(" ", "_")

                    try:
                        data[key] = int(value.strip())
                    except ValueError:
                        continue

        return data

    def update_user_score_text_file(self):
        attempt = self.game.playGame()
        history = self.read_text_history()

        previous_score = attempt
        highest_score = history["highest_score"]
        lowest_score = history["lowest_score"]
        games_played = history["games_played"] + 1

        # Fewer attempts means a better score
        if highest_score == 0 or attempt < highest_score:
            highest_score = attempt

        # More attempts means a worse score
        if lowest_score == 0 or attempt > lowest_score:
            lowest_score = attempt

        # Save the updated history
        with open(self.path_text_file, "w") as file:
            file.write(f"previous_score: {previous_score}\n")
            file.write(f"highest_score: {highest_score}\n")
            file.write(f"lowest_score: {lowest_score}\n")
            file.write(f"games_played: {games_played}\n")

        print(f"🏆 Previous score: {previous_score} attempts")
        print(f"📊 Best score: {highest_score} attempts")
        print(f"📊 Lowest score: {lowest_score} attempts")
        print(f"🎮 Games played: {games_played}")


class Json_file_data(ABC):
    @abstractmethod
    def take_user_name(self)-> str | None:
        pass

    @abstractmethod
    def check_user_exists(self, user)->bool:
        pass

    @abstractmethod
    def read_all_history(self)->dict:
        pass

    @abstractmethod
    def read_user_json_history(self, user):
        pass

    @abstractmethod
    def save_json_history(self, data):
        pass

    @abstractmethod
    def update_user_score_json_file(self):
        pass


class Json_concrete_class(Json_file_data):

    def __init__(self, game):
        self.game = game
        self.path_json_file = Path(__file__).resolve().parent / "data.json"

    # take user name
    def take_user_name(self):
        user_name = input("Enter your username ---> ").strip()
        if not user_name:
            print("name can't be empty!")
            return None
        return user_name

    def check_user_exists(self, user):
        self.history = self.read_all_history()
        return user in self.history

    def read_all_history(self):
        if not self.path_json_file.exists():
            return {}

        try:
            with open(self.path_json_file, "r",encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return {}

    def read_user_json_history(self, user):
        return self.read_all_history().get(user)

    def save_json_history(self, data):
        with open(self.path_json_file, "w",encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def update_user_score_json_file(self):
        user = self.take_user_name()

        if user is None:
            return

        # Load all players' data
        all_history = self.read_all_history()

        # Get existing user data or initialize a new user
        user_history = all_history.get(
            user,
            {
                "previous score": 0,
                "highest score": 0,
                "lowest score": 0,
                "games played": 0,
            },
        )

        # Play the game
        attempt = self.game.playGame()

        # Update previous score
        user_history["previous score"] = attempt

        highest_score = user_history["highest score"]
        lowest_score = user_history["lowest score"]

        # Fewer attempts means a better score
        if highest_score == 0 or attempt < highest_score:
            user_history["highest score"] = attempt

        # More attempts means a worse score
        if lowest_score == 0 or attempt > lowest_score:
            user_history["lowest score"] = attempt

        # Update total games
        user_history["games played"] += 1

        # Update only this player's entry
        all_history[user] = user_history

        # Save all players to JSON
        self.save_json_history(all_history)

        print(f"\n🏆 Player: {user}")
        print(f"Previous score: {user_history['previous score']} attempts")
        print(f"Best score: {user_history['highest score']} attempts")
        print(f"Worst score: {user_history['lowest score']} attempts")
        print(f"Games played: {user_history['games played']}")

        if generate_user_json_data is not None:
            generate_user_json_data()
        else:
            print("PDF generation skipped: install reportlab to enable it.")

if __name__=="__main__":
    game=Play_game()
    
    json_handler = Json_concrete_class(game)
    json_handler.update_user_score_json_file()

    # To use text-file storage instead, uncomment:
    # text_handler = Text_concrete_class(game)
    # text_handler.update_user_score_text_file()
