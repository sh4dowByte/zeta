import argparse
import sys
from app.utils.helper import display_banner

from app.repository.crt import CRTScraper
from app.repository.subdomainfinder import SubdomainFinder

from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console

from app.utils.output import export

def main():
    """
    """
    display_banner()

    # Initialize objects for searching
    crt = CRTScraper()
    subdomainfinder = SubdomainFinder()

    # Create argument parser for handling command-line arguments
    parser = argparse.ArgumentParser(
        description="Zeta - A tool for find subdomains."
    )

    # Adding argument for ExploitDB search
    parser.add_argument(
        "-s", "--search",
        type=str,
        help="Search for a specific subdomain."  # Add explanation
    )

    parser.add_argument(
        "--output", "-o", type=str, 
        help="Output .txt"
    )

    # Parse arguments
    args = parser.parse_args()
    output_file = args.output

    try:
        # Check if a search term is provided
        if args.search:
            # Initialize Rich console
            console = Console()

            # List of searches to perform
            search_functions = [
                (crt.scan, "📂 Crt.sh"),
                (subdomainfinder.scan, "📂 Subdomainfinder.c99.nl"),
            ]

            # Display search message
            console.print(f"Searching for subdomain for: {args.search}\n\n")

            # Display loading progress
            subdomains = []
            for func, title in search_functions:
                title = f"[bold]{title}[/bold]"
                # Show loading for the current function
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                    console=console
                ) as progress:
                    task = progress.add_task(f"{title}", total=3)
                    
                    # Run the search
                    subdomain, tree = func(args.search, title=title)
                    subdomains += subdomain

                    console.print(tree)

                    print('\n')
                    
                    # Mark the task as completed
                    progress.update(task, advance=1)

            export(output_file, subdomains)

        else:
            print("No search term provided. Use -s or --search to specify a search term.")

    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
