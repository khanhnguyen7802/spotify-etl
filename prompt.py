import os
import platform

def main():
    # Clear screen based on OS
    os.system('cls' if platform.system() == 'Windows' else 'clear')
    
    print("Welcome to my command line program!")
    print("----------------------------------")
    print(
        """
███████╗██████╗  ██████╗ ████████╗██╗███████╗██╗   ██╗     ██████╗ ██████╗ ███╗   ██╗███╗   ██╗███████╗ ██████╗████████╗
██╔════╝██╔══██╗██╔═══██╗╚══██╔══╝██║██╔════╝╚██╗ ██╔╝    ██╔════╝██╔═══██╗████╗  ██║████╗  ██║██╔════╝██╔════╝╚══██╔══╝
███████╗██████╔╝██║   ██║   ██║   ██║█████╗   ╚████╔╝     ██║     ██║   ██║██╔██╗ ██║██╔██╗ ██║█████╗  ██║        ██║   
╚════██║██╔═══╝ ██║   ██║   ██║   ██║██╔══╝    ╚██╔╝      ██║     ██║   ██║██║╚██╗██║██║╚██╗██║██╔══╝  ██║        ██║   
███████║██║     ╚██████╔╝   ██║   ██║██║        ██║       ╚██████╗╚██████╔╝██║ ╚████║██║ ╚████║███████╗╚██████╗   ██║   
╚══════╝╚═╝      ╚═════╝    ╚═╝   ╚═╝╚═╝        ╚═╝        ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═╝                                                                                                                           
      """
    )
    # Get user inputs
    input1 = input("Enter your client ID: ")
    input2 = input("Enter your client secret: ")
    input3 = input("Enter your redirect URI: ")
    
    # Process inputs
    print(f"\nYou entered: {input1}, {input2}, {input3}")
    print("Processing...")
    
    # Push the user input to dev app 

    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()