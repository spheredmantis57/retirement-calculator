from os import name, system

class InputHandler:
    """Class to handle user input
    """
    WARNING = "Warning: {}"

    def __init__(self, allow_cancel=False):
        """initializes an InputHandler object

        Args:
            bool:allow_cancel - True if there is an option to cancel input but
                not quit program; False if when trying to cancel input, the
                program will quit
        """
        self.allow_cancel = allow_cancel
        

    class CancelInput(Exception):
        """User wants to cancel input, but not quit program"""
        pass

    class QuitProgram(Exception):
        """User wants to quit program"""
        pass

    @staticmethod
    def clear():
        """clears the terminal
        """
        if name == 'nt':
            system("cls")
        else:
            system("clear")


    def _quit(self):
        """Handles the user wanting to cancel input or quit the program
        """
        self.clear()
        print("Press Ctrl+C to confirm QUIT.")
        print("Press ENTER to go back to input screen.")

        if self.allow_cancel is True:
            # allow a user to cancel the cancel, quit, or cancel the input but
            # not quit the program
            print("Press Ctrl+D to cancel input, but not quit program.")
            try:
                input()
            except KeyboardInterrupt:
                raise InputHandler.QuitProgram("User quitting")
            except EOFError:
                raise InputHandler.CancelInput("User does not want to enter input")

        else:
            # allow a user to quit the program, or cancel and go back to input
            try:
                input()
            except (KeyboardInterrupt, EOFError):
                raise InputHandler.QuitProgram("User quitting")


    def input_int(self, min=0, max=1000000, input_type="int"):
        """gets an integer from the user

        Args:
            int:min - minimum the input can be
            int:max - maximum the input can be
            string:input_type - what the int is for (eg: "years")

        Returns:
            int:value entered, within range (cannot be trusted if exception raised)

        Raises:
            InputHandler.QuitProgram:user wants to quit program
            InputHandler.CancelQuit:user wants to cancel input, but not quit program
        """
        # get the input
        prompt = f"Enter {input_type} (an int from {min} to {max}): "
        # try again till min and max are met
        while True:
            try:
                number = input(prompt)
                number = int(number)
                if min <= number <= max:
                    return number
                print(self.WARNING.format("Incorrect range. Try again."))  
            except TypeError:
                print(self.WARNING.format("Must be an int. Try again."))
            except (KeyboardInterrupt, EOFError):
                self._quit()
