from textnode import TextType, TextNode


def main():
    myobj = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(myobj)


if __name__ == '__main__':
    main()
