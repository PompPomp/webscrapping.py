# Credits: CySecure 2023 Lee Wee Kang

import requests
from bs4 import BeautifulSoup
import sys

extensions = ['.exe', '.deploy', '.inf', '.zip', '.dll', '.config']


def web_scrap(url):
    print("Current Directory: " + url)
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <a> elements and extract their href attributes
        link_elements = soup.find_all('a')

        # Initialize a list to store the URLs
        links = []

        # Extract the href attributes and create complete URLs
        for link_element in link_elements:
            if "[To Parent Directory]" not in link_element:
                href = link_element.get('href')
                complete_url = base_url + href

                if any(ext in href for ext in extensions):
                    print("Detected File: ", href)
                else:
                    # Append directories
                    links.append(complete_url)

    # Loop through the extracted links and fetch their content
    for link in links:
        try:
            response = requests.get(link)
            if response.status_code == 200:
                # soup = BeautifulSoup(response.text, 'html.parser')
                # print(soup)
                web_scrap(link.rstrip('/'))
            else:
                print(f"Failed to retrieve content from {link}. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while fetching content from {link}: {e}")


base_url = input("Enter base url: ")
with open('directoryList.txt', 'w') as file:
    sys.stdout = file

    # Send an HTTP GET request to the URL
    web_scrap(base_url)

    print("Output has been saved to directoryList.txt")

sys.stdout = sys.__stdout__
