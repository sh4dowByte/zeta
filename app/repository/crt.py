import re
import requests
from lxml import html
from rich.tree import Tree

class CRTScraper:
    """
    A class to scrape and extract subdomains from crt.sh based on a given domain.

    Attributes:
    - base_url (str): The base URL for querying crt.sh.

    Methods:
    - get_html(domain: str) -> bytes:
        Fetches the HTML content from crt.sh for the specified domain.

    - extract_subdomains(html_content: bytes) -> list:
        Extracts subdomains from the provided HTML content using XPath and regular expressions.

    - scan(domain: str, title: str = '') -> tuple:
        Performs a scan for subdomains of the given domain and returns a tuple containing:
        1. A list of extracted subdomains.
        2. A Rich Tree object representing the scanned data, including subdomain information and related metadata.
    """

    def __init__(self):
        """
        Initializes the CRTScraper with the base URL for querying crt.sh.
        """
        self.base_url = "https://crt.sh/?q="
    
    def get_html(self, domain):
        """
        Fetches the HTML content from crt.sh based on the specified domain.

        Parameters:
        - domain (str): The domain to query on crt.sh.

        Returns:
        - bytes: The HTML content of the page.

        Raises:
        - Exception: If the request to crt.sh fails or returns a non-200 status code.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        
        url = self.base_url + domain
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Failed to retrieve crt.sh page, status code: {response.status_code}")
    
    def extract_subdomains(self, html_content):
        """
        Extracts subdomains from the provided HTML content using XPath and regular expressions.

        Parameters:
        - html_content (bytes): The HTML content from crt.sh.

        Returns:
        - list: A list of subdomain entries where each entry is a list of details extracted from the table.
        """
        tree = html.fromstring(html_content)
        
        # XPath to extract data from the subdomain table
        subdomains = tree.xpath('/html/body/table[2]/tr/td/table/tr')
        datas = []
        for sub in subdomains:
            sub = re.sub(r'[^\S\r\n]+', '', sub.text_content())
            datas.append(sub.split("\n"))

        seen = set()
        filtered_data = []

        for entry in datas:
            if entry[5] == 'LoggedAt':
                continue

            subdomain = entry[5]  # Element at index 5
            if subdomain not in seen:
                filtered_data.append(entry)
                seen.add(subdomain)

        return filtered_data
      
    def scan(self, domain, title=''):
        """
        Scans for subdomains of the specified domain and constructs a Rich Tree for the results.

        Parameters:
        - domain (str): The domain to scan for subdomains.
        - title (str): The title to display in the tree structure. Default is an empty string.

        Returns:
        - tuple: A tuple containing:
            1. A list of extracted subdomain names.
            2. A Rich Tree object displaying the scanned data including subdomain names and associated metadata.

        Process:
        1. Retrieves the HTML content from crt.sh for the given domain.
        2. Extracts subdomain data from the HTML content.
        3. Constructs a Rich Tree structure to display the subdomain details.
        4. Handles exceptions and adds error messages to the tree if any occur.
        """
        tree = Tree(title)
        subdomain = []

        try:
            html_content = self.get_html(domain)
            datas = self.extract_subdomains(html_content)

            if isinstance(datas, list):
                subdomain = [entry[5] for entry in datas]

            for data in datas:
                data_node = tree.add(f'[green]{data[5]}[/green]')
                data_node.add(f'ID          : {data[1]}')
                data_node.add(f'Logged At   : {data[2]}')
                data_node.add(f'Not Before  : {data[3]}')
                data_node.add(f'Not After   : {data[4]}')
                data_node.add(f'Issuer      : {data[7]}')

            if not datas:
                tree.add(f"[yellow]Subdomain not detected[/yellow]")
    
        except Exception as e:
            tree.add(f"[yellow]{e}[/yellow]")

        return subdomain, tree
