from app.config import App
from app.utils.style import Colors, TextFormat

def display_banner():
    """
    Display a banner with a version number and random text.

    This function prints a stylized banner including a version number and a randomly chosen text
    in different colors.

    Returns:
        None
    """
    banner = rf"""
    {Colors.GREEN}
     _____        __       
    /__  /  ___  / /_____ _
      / /  / _ \/ __/ __ `/
     / /__/  __/ /_/ /_/ / 
    /____/\___/\__/\__,_/    v{App.version}
    {Colors.RESET}
            {TextFormat.text('Subdomain Discovery Tool')}
    
    """
    print(banner)
