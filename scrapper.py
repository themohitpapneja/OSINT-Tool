import pyfiglet
import twitter as ta
class Scrapper:
    def view():
        ascii_banner = pyfiglet.figlet_format("Scrapper - An OSINT Tool")
        print(ascii_banner)
        print("\n Enter 1: For Instagram Scrapper  >>>>>>>>\n")
        print("\n Enter 2: For Twitter Scrapper    >>>>>>>>\n")
        i = input(">>>")
        if int(i) == 1:
            print("\n!!!!!!!   The User_ID To Be Scraped Should Be Either Public Or Is Your Connect\n")
            from insta import Instagram
            
        elif int(i) == 2:
            ta.main()
        else:
            print(" Invalid Option ")
Scrapper.view()
