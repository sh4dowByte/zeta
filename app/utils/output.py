import os

def export(output_file, output):
    """
    Export a list of strings to a specified file.

    Parameters:
    - output_file (str): The path to the output file where the data will be saved. If the path contains directories that do not exist, they will be created.
    - output (list of str): A list of strings to be written to the output file. Each string will be written to a new line in the file.

    This function performs the following steps:
    1. Retrieves the current working directory.
    2. Constructs the full path for the output file, including any necessary directories.
    3. Creates the directories if they do not already exist.
    4. Writes each string from the `output` list to the specified file, each on a new line.
    """
    if output_file:
        # Get the current directory
        current_dir = os.getcwd()

        # Define the output file path including its folder
        output_file = os.path.join(current_dir, output_file)

        # Create the directory if it does not exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Write each string from the output list to the file
        with open(output_file, "w") as file:
            for out in output:
                file.write(out + '\n')
