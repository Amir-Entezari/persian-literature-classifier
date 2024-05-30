import csv
import os

import requests
from bs4 import BeautifulSoup


def get_poem(url):
    """
    This function takes a URL of a webpage containing a poem, extracts the verses, and calculates the number of verses
    and words in the poem.

    Parameters:
        url (str): The URL of the webpage containing the poem.

    Returns:
        tuple: A tuple containing the poem text, number of verses, and number of words in the poem.
    """

    # Send a GET request to the provided URL
    r = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content of the webpage
    soup = BeautifulSoup(r.content)

    # Find all <div> elements with class 'b' which typically contain the verses of the poem
    verses = soup.findAll('div', attrs={'class': 'b'})

    # Extract the text of each verse and join them with newline characters to form the poem text
    poem = "\n".join([b.text for b in verses])

    # Calculate the number of verses in the poem
    verse_num = len(verses)

    # Calculate the total number of words in the poem
    word_num = sum([len(verse.text.split()) or 0 for verse in verses])

    # Return a tuple containing the poem text, number of verses, and number of words
    return (poem, verse_num, word_num)


def get_book_urls(url, prefix="https://ganjoor.net"):
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    parts = soup.findAll('div', attrs={'class': 'part-title-block'})
    parts = [f'{prefix}/{b.find("a")["href"]}' for b in parts]
    return parts


def get_part_urls(url, prefix="https://ganjoor.net"):
    """
    This function takes a URL of a webpage containing a collection of poem excerpts and extracts the URLs of each
    poem's full version. It then appends them with a given prefix to form complete URLs.

    Parameters:
        url (str): The URL of the webpage containing the poem excerpts.
        prefix (str, optional): The prefix to be added to the extracted URLs. Default is "https://ganjoor.net".

    Returns:
        list: A list containing the complete URLs of each poem's full version.
    """

    # Send a GET request to the provided URL
    r = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content of the webpage
    soup = BeautifulSoup(r.content)

    # Find all <p> elements with class 'poem-excerpt' which typically contain links to poem excerpts
    parts = soup.findAll('p', attrs={'class': 'poem-excerpt'})

    # Extract the URLs from each <a> tag found within <p> elements and append them with the prefix
    parts = [f'{prefix}/{b.find("a")["href"]}' for b in parts]

    # Return the list of complete URLs
    return parts


def get_poet(poet, directory="./result", number_of_doc_words=700, print_details=False):
    """
    This function takes a list of URLs of poet pages, extracts their poems, and saves them in CSV files according to
    specified criteria.

    Parameters:
        poet (list): A dictionary contain name of author and its books with URLs of poet pages.
        directory (str, optional): The directory where the CSV files will be saved. Default is "./result".
        number_of_doc_words (int, optional): The maximum number of words per document. Default is 700.
        print_details (bool, optional): Whether to print details during processing. Default is False.

    Returns:
        list: A list of dictionaries containing details about the processed documents.
    """

    # Define the author name
    a_name = poet["name"]

    # Define the file name for the CSV file
    f_name = f"{directory}/{a_name}.csv"

    book_list = [book for book in poet["books"]]
    # Create the result directory if it doesn't exist
    try:
        os.mkdir(directory)
    except:
        pass

    # Open the CSV file for writing
    with open(f_name, 'w', newline='') as f_all:
        # Create a CSV writer object
        w = csv.DictWriter(f_all, ['author', 'book', 'text'])
        # Write the header row
        w.writeheader()

        # Initialize variables for document word count and details
        n_doc = 0
        n_doc_words = 0
        doc = ""
        details = []

        # Iterate over each poet link
        for book in book_list:
            # Get the URLs of books written by the poet
            book_urls = get_book_urls(book["url"])

            # Iterate over each book URL
            for b_url in book_urls:
                n_doc_words = 0
                doc = ""

                # Get the URLs of parts (poem excerpts) in the book
                part_urls = get_part_urls(b_url)

                # Iterate over each part URL
                for url in part_urls:
                    # Get the poem text, number of verses, and number of words
                    poem, verse_num, word_num = get_poem(url)

                    # Append poem text to the document and update word count
                    doc += f"\n{poem}"
                    n_doc_words += word_num

                    # Check if document word count exceeds the threshold
                    if n_doc_words > number_of_doc_words:
                        # Optionally print details
                        print_details and print(f"{url} : {n_doc_words}")

                        # Write the document details to the CSV file
                        w.writerow({
                            "author": poet["name"],
                            "book": book["name"],
                            "text": doc
                        })

                        # Append details to the list
                        details.append({
                            "author": url[20:].split("/")[0],
                            "book": url[20:].split("/")[1],
                            "n_doc_words": n_doc_words,
                            "n_doc": n_doc
                        })

                        # Reset document word count and content
                        n_doc_words = 0
                        doc = ""
                        n_doc += 1

                        # Check if the maximum number of documents has been reached
                        if n_doc > 30:
                            return details

        return details


# Example usage
if __name__ == "__main__":
    poets = [
        {
            "name": "attar",
            "books": [
                {
                    "name": "asrarname",
                    "url": "https://ganjoor.net/attar/asrarname"
                },
                {
                    "name": "",
                    "url": "https://ganjoor.net/attar/manteghotteyr/naat"
                }
            ]
        },
        {
            "name": "saadi",
            "books": [
                {
                    "name": "golestan",
                    "url": "https://ganjoor.net/saadi/golestan"
                }
            ]
        }
    ]
    for poet in poets:
        get_poet(poet, directory="../datasets/raw", print_details=True)
