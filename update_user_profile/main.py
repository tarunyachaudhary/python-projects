# Create a function with positional and keyword arguments to format a user profile.


from abc import ABC, abstractmethod


class UserUpdateAbstractClass(ABC):

    @abstractmethod
    def login_user(self) -> bool:
        pass

    @abstractmethod
    def profile_update_options(self) -> dict:
        pass

    @abstractmethod
    def take_input(self) -> int:
        pass

    @abstractmethod
    def update_username(self):
        pass

    @abstractmethod
    def forgot_password(self):
        pass

    @abstractmethod
    def update_email(self):
        pass

    @abstractmethod
    def update_phone(self):
        pass

    @abstractmethod
    def delete_account(self):
        pass


class UserUpdateConcreteClass(UserUpdateAbstractClass):

    # User data: username -> password
    user_data = {"Tarun": "12345", "Abhishek": "23456", "Prajjwal": "34567"}

    # Store additional profile information
    profile_data = {
        "Tarun": {"email": "tarun@gmail.com", "phone": "9876543210"},
        "Abhishek": {"email": "abhishek@gmail.com", "phone": "9876543211"},
        "Prajjwal": {"email": "prajjwal@gmail.com", "phone": "9876543212"},
    }

    def __init__(self):
        self.current_username = None

    # Login user
    def login_user(self):
        print("\n--- User Login ---")

        username = input("Username ---> ").strip()
        password = input("Password ---> ")

        if self.user_data.get(username) == password:
            self.current_username = username
            print("Login successful!")
            return True

        print("Invalid username or password!")
        return False

    # Display profile update options
    def profile_update_options(self) -> dict:
        return {
            1: "Update username",
            2: "Forgot password",
            3: "Update email",
            4: "Update phone",
            5: "Delete account",
            6: "View profile",
            7: "Logout",
        }

    # Take menu input
    def take_input(self) -> int:
        try:
            return int(input("\nEnter your choice ---> "))
        except ValueError:
            print("Please enter a valid number!")
            return -1

    # Update username
    def update_username(self):
        old_username = self.current_username

        if old_username not in self.user_data:
            print("User not found!")
            return

        new_username = input("New username ---> ").strip()

        if not new_username:
            print("Username cannot be empty!")
            return

        if new_username in self.user_data:
            print("Username already exists!")
            return

        # Preserve the existing password
        self.user_data[new_username] = self.user_data.pop(old_username)

        # Preserve and move the profile information
        self.profile_data[new_username] = self.profile_data.pop(old_username)

        self.current_username = new_username

        print(f"Username updated successfully to {new_username}!")

    # Reset password
    def forgot_password(self):
        username = self.current_username

        new_password = input("Enter new password ---> ")
        confirm_password = input("Confirm new password ---> ")

        if len(new_password) < 5:
            print("Password must contain at least 5 characters!")
            return

        if new_password != confirm_password:
            print("Passwords do not match!")
            return

        self.user_data[username] = new_password  # type: ignore
        print("Password updated successfully!")

    # Update email
    def update_email(self):
        email = input("Enter new email ---> ").strip()

        if "@" not in email or "." not in email.split("@")[-1]:
            print("Please enter a valid email address!")
            return

        self.profile_data[self.current_username]["email"] = email  # type: ignore
        print("Email updated successfully!")

    # Update phone number
    def update_phone(self):
        phone = input("Enter new 10-digit phone number ---> ").strip()

        if not phone.isdigit() or len(phone) != 10:
            print("Please enter a valid 10-digit phone number!")
            return

        self.profile_data[self.current_username]["phone"] = phone  # type: ignore
        print("Phone number updated successfully!")

    # Delete account
    def delete_account(self):
        confirmation = (
            input("Are you sure you want to delete your account? (yes/no) ---> ")
            .strip()
            .lower()
        )

        if confirmation == "yes":
            username = self.current_username

            self.user_data.pop(username, None)  # type: ignore
            self.profile_data.pop(username, None)  # type: ignore
            self.current_username = None

            print("Account deleted successfully!")
        else:
            print("Account deletion cancelled.")

    # View profile
    def view_profile(self):
        username = self.current_username
        profile = self.profile_data[username]  # type: ignore

        print("\n--- User Profile ---")
        print(f"Username: {username}")
        print(f"Email: {profile['email']}")
        print(f"Phone: {profile['phone']}")

    # Main menu
    def user_profile_update(self):
        if not self.login_user():
            return

        while self.current_username is not None:
            options = self.profile_update_options()

            print("\n--- Profile Management ---")
            for key, value in options.items():
                print(f"{key}. {value}")

            user_choice = self.take_input()

            match user_choice:
                case 1:
                    self.update_username()
                case 2:
                    self.forgot_password()
                case 3:
                    self.update_email()
                case 4:
                    self.update_phone()
                case 5:
                    self.delete_account()
                case 6:
                    self.view_profile()
                case 7:
                    print("Logged out successfully!")
                    self.current_username = None
                case _:
                    print("Invalid choice! Please try again.")


# Run program
if __name__ == "__main__":
    obj = UserUpdateConcreteClass()
    obj.user_profile_update()
