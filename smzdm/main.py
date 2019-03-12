import checkin
from log import logger
import config

def main():
    users = config.getUsers()
    for user in users:
        checkin.checkin(user)


if __name__ == '__main__':
    main()