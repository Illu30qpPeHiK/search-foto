import logging
from testBase import sites
from searchMultiSites import SearchMultiSites
from config import username, password

logging.basicConfig(level=logging.INFO)

def main():
    try:
        choice = input("Do you want to login? (y/n): ").lower()
        if choice == 'y':
            login_required = True
        elif choice == 'n':
            login_required = False
        else:
            logging.error("Invalid choice. Please enter 'y' or 'n'.")
            return

        username_to_search = input('Enter the username that needs to be found: ')
        search_data = SearchMultiSites(sites, username_to_search, login_required, username, password)
        search_data.search_on_multiple_sites()

    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()
