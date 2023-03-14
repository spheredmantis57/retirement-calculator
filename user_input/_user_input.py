from os import name, system

class InputHandler:
    WARNING = "Warning: {}"

    def __init__(self, allow_cancel=False):
        self.allow_cancel = allow_cancel
        

    class CancelInput(Exception):
        """User wants to cancel input, but not quit program"""
        pass

    class QuitProgram(Exception):
        """User wants to quit program"""
        pass

    @staticmethod
    def clear():
        if name == 'nt':
            system("cls")
        else:
            system("clear")


    def _quit(self):
        self.clear()
        print("Press Ctrl+C to confirm QUIT.")
        print("Press ENTER to go back to input screen.")
        if self.allow_cancel is True:
            print("Press Ctrl+D to cancel input, but not quit program.")
            try:
                input()
            except KeyboardInterrupt:
                raise InputHandler.QuitProgram("User quitting")
            except EOFError:
                raise InputHandler.CancelInput("User does not want to enter input")
        else:
            try:
                input()
            except (KeyboardInterrupt, EOFError):
                raise InputHandler.QuitProgram("User quitting")

        

    def input_int(self, min=0, max=1000000, input_type="int"):
        """
        todo: finish this doc string
        RETURNS:
        int:value entered, within range (cannot be trusted if exception raised)

        RAISES:
        InputHandler.QuitProgram:user wants to quit program
        InputHandler.CancelQuit:user wants to cancel input, but not quit program
        """
        prompt = f"Enter {input_type} (an int from {min} to {max}): "
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
