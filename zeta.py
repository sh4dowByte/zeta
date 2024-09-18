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
    Main function to execute subdomain search using crt.sh and subdomainfinder.c99.nl.
    Handles command-line arguments and displays the results using the Rich library.
    """
    # Display the application banner
    display_banner()

    # Initialize objects for subdomain search using different sources
    crt = CRTScraper()
    subdomainfinder = SubdomainFinder()

    # Create argument parser to handle command-line input
    parser = argparse.ArgumentParser(
        description="Zeta - A tool for finding subdomains."
    )

    # Add an argument for specifying the subdomain to search
    parser.add_argument(
        "-s", "--search",
        type=str,
        help="Search for a specific subdomain."  # Add explanation for the search argument
    )

    # Add an argument to specify output file for saving results
    parser.add_argument(
        "--output", "-o", type=str, 
        help="Specify output .txt file for saving subdomains."
    )

    # Parse command-line arguments
    args = parser.parse_args()
    output_file = args.output

    try:
        # Check if a search term is provided
        if args.search:
            # Initialize Rich console for displaying output
            console = Console()

            # List of search functions to perform, each with its source title
            search_functions = [
                (crt.scan, "📂 Crt.sh"),
                (subdomainfinder.scan, "📂 Subdomainfinder.c99.nl"),
            ]

            # Display message about the subdomain being searched
            console.print(f"Searching for subdomain for: {args.search}\n\n")

            # Display progress indicator while performing search
            subdomains = []
            for func, title in search_functions:
                title = f"[bold]{title}[/bold]"
                
                # Use Rich's Progress to show a spinner during search
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True,
                    console=console
                ) as progress:
                    task = progress.add_task(f"{title}", total=3)
                    
                    # Run the search function and collect the results
                    subdomain, tree = func(args.search, title=title)
                    subdomains += subdomain

                    # Print the results in a tree structure
                    console.print(tree)

                    print('\n')
                    
                    # Mark the task as complete
                    progress.update(task, advance=1)

            # Export the results to a file if output is specified
            export(output_file, subdomains)

        else:
            # If no search term is provided, prompt the user to use -s or --search
            print("No search term provided. Use -s or --search to specify a search term.")

    except KeyboardInterrupt:
        # Handle user interruption (Ctrl + C)
        print("\nProcess interrupted by user. Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    # Entry point of the script
    main()
