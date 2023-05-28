import wikipedia
from datetime import timedelta


def main():
    while True:
        args = input()
        args = args.split(' ')
        backend(args)

def backend(args):
    print("Arguments received:", args)
    if args[0] != '':


        if args[0].lower() == 'wiki' or args[0].lower() == 'wikipedia' or args[0].lower() == 'w':
            args.pop(0)
            wiki(args)


    else:
        print("No arguments received")

def wiki(args):
    args = " ".join(args)
    print(args)
    wikipedia.set_lang('en')
    wikipedia.set_rate_limiting(True, min_wait=timedelta(milliseconds=1000))
    print("Getting Info...")
    try:
        print(wikipedia.summary(args, sentences=2, auto_suggest=False))
    except wikipedia.DisambiguationError as e:
        print(f"There are multiple results for \"{args}\", Here are some suggestions:")
        ops = '\n'.join(e.options[0::5])
        print(ops)
    except wikipedia.exceptions.PageError as e:
        print("Invalid input, no page found matching the query. please cheack you spellings and try again.")


if __name__ == '__main__':
    main()
