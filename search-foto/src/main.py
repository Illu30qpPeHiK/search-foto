import os
import logging
from testBase import sites
from searchMultiSites import SearchMultiSites

logging.basicConfig(level=logging.INFO)

def main():
    username = os.getenv('username')
    password = os.getenv('password')

    try:
        choice = input("Do you want to login? (y/n): ").lower()
        if choice == 'y':
            if not username or not password:
                logging.error("Username and password must be set in the environment variables for login.")
                return
            login_required = True
        elif choice == 'n':
            login_required = False
        else:
            logging.error("Invalid choice. Please enter 'y' or 'n'.")
            return

        username_to_search = input('Enter the username that needs to be found: ')
        search_multi_sites = SearchMultiSites(username, password, sites, username_to_search, login_required)
        search_multi_sites.search_on_multiple_sites()

    except Exception as e:
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    main()
