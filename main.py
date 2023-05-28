import tkinter
import bs4
import requests


def wiki(*args):
    argList = list(args)
    search = ""
    for i in argList:
        search += i
    print(search)
    url = 'https://en.wikipedia.org/w/api.php?action=opensearch&search=' + search + '&format=json'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    print(soup.prettify())


def main():
    root = tkinter.Tk()
    root.geometry("500x100")
    textarea = tkinter.Text(root, width=50, height=3)  # Set the width and height
    textarea.pack()

    def on_return(event):
        args = textarea.get("1.0", tkinter.END)
        args = args.replace('\n', '')
        args = args.split(' ')
        textarea.delete("1.0", tkinter.END)
        print(args)
        backend(args)

    textarea.bind('<Return>', on_return)

    root.mainloop()

def backend(args):
    print("Arguments received:", args)
    if args[0] != '':
        if args[0].lower() == 'wiki' or args[0].lower() == 'wikipedia' or args[0].lower() == 'w':
            print("ok")
            wiki(args[1::-1])
    else:
        print("No arguments received")

if __name__ == '__main__':
    main()
