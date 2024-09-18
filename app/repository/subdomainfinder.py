import json
from playwright.sync_api import sync_playwright
from lxml import html
from rich.tree import Tree

class SubdomainFinder:
    """
    A class to perform subdomain scanning using a web-based tool.

    Methods:
    - scan(domain: str, title: str = '') -> tuple:
        Performs a scan for subdomains of the given domain and returns a tuple containing:
        1. A list of extracted subdomain names.
        2. A Rich Tree object representing the scanned data, including subdomains, IP addresses, and Cloudflare information.
    """

    def scan(self, domain, title=''):
        """
        Scan for subdomains of the specified domain and display the results.

        Parameters:
        - domain (str): The domain to scan for subdomains.
        - title (str): The title to display in the tree structure. Default is an empty string.

        Returns:
        - tuple: A tuple containing:
            1. A list of extracted subdomain names.
            2. A Rich Tree object showing the scanned data including subdomain names, IP addresses, and Cloudflare information.

        Process:
        1. Launches a headless browser using Playwright.
        2. Navigates to the Subdomain Finder tool website.
        3. Inputs the domain into the search field and initiates the scan.
        4. Waits for the scan results to be loaded.
        5. Parses the HTML content to extract subdomain names, IP addresses, and Cloudflare attributes.
        6. Constructs a Rich Tree structure to display the results.
        7. Handles exceptions and adds error messages to the tree if any occur.
        """
        tree = Tree(title)

        try:
            with sync_playwright() as p:
                # Launch headless browser
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()

                # Navigate to the target page
                page.goto("https://subdomainfinder.c99.nl/")

                # Fill in the domain input field
                page.fill("#domain", domain)

                # Click the scan button
                page.click("#scan_subdomains")

                # Wait for the scan results to appear
                page.wait_for_selector(".well")
                
                # Retrieve the page content
                html_content = page.content()

                # Close the browser
                browser.close()

                # Parse HTML using lxml
                path = html.fromstring(html_content)

                # Extract subdomains, IP addresses, and Cloudflare data
                links = path.xpath('/html/body/div/div[2]/div[1]/center/div[3]/table/tbody/tr/td[2]/a/text()')
                ip_addresses = path.xpath('/html/body/div/div[2]/div[1]/center/div[3]/table/tbody/tr/td[3]/a/text()')
                cloudflaredPath = path.xpath('/html/body/div/div[2]/div[1]/center/div[3]/table/tbody/tr/td[4]/img')
                
                cloudflared = []
                for element in cloudflaredPath:
                    cf_attributes = {attr: element.attrib[attr] for attr in element.attrib if attr.startswith('data-cf')}
                    if cf_attributes:
                        cloudflared.append(cf_attributes['data-cf'])

                # Combine the data into a structured format
                datas = [{'subdomain': link, 'ip': ip, 'cloudflared': cf} for link, ip, cf in zip(links, ip_addresses, cloudflared) if ip.lower() != "none"]

                # Add results to the Rich Tree
                for data in datas:
                    data_node = tree.add(f'[green]{data["subdomain"]}[/green]')
                    data_node.add(f'IP Address   : {data["ip"]}')
                    data_node.add(f'Cloudflared  : {data["cloudflared"]}')

        except Exception as e:
            tree.add(f"[yellow]{e}[/yellow]")

        return links, tree
