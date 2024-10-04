import click
from PIL import Image, ImageOps
from rich.console import Console
from rich.prompt import Prompt

console = Console()

# Function to convert sprite to correct dimensions and format for Gen 1 games
def convert_sprite(input_path, output_path, sprite_type="front"):
    # Open the input image
    img = Image.open(input_path)

    # Determine dimensions based on the sprite type
    if sprite_type == "front":
        new_size = (56, 56)  # Front sprites are 56x56
    elif sprite_type == "back":
        new_size = (32, 32)  # Back sprites are 48x48
    else:
        raise ValueError("Invalid sprite_type. Choose 'front' or 'back'.")

    # Resize the image to the correct dimensions (LANCZOS is the new equivalent of ANTIALIAS)
    img_resized = img.resize(new_size, Image.Resampling.LANCZOS)

    # Convert the image to grayscale
    img_grayscale = img_resized.convert('L')

    # Reduce the grayscale image to 4 shades
    img_posterized = ImageOps.posterize(img_grayscale, 2)  # 2 bits = 4 shades

    # Save the resulting image
    img_posterized.save(output_path)
    console.print(f"[bold green]Converted {sprite_type} sprite saved as {output_path}[/bold green]")

# CLI and menu using Click and Rich
@click.command()
def menu():
    console.print("[bold cyan]Welcome to the Pokémon Sprite Converter CLI![/bold cyan]")
    console.print("[bold yellow]Choose an option below:[/bold yellow]")
    
    # Displaying menu options
    console.print("1. Convert a front sprite")
    console.print("2. Convert a back sprite")
    console.print("3. Exit")

    # Getting user choice
    choice = Prompt.ask("[bold white]Enter your choice (1/2/3)[/bold white]")

    # Handling the choice
    if choice == "1":
        input_path = Prompt.ask("[bold white]Enter the path to the input image (e.g., pokemon_80x80.png)[/bold white]")
        output_path = Prompt.ask("[bold white]Enter the path to save the output image (e.g., pokemon_front_56x56_grayscale.png)[/bold white]")
        convert_sprite(input_path, output_path, sprite_type="front")
    elif choice == "2":
        input_path = Prompt.ask("[bold white]Enter the path to the input image (e.g., pokemon_80x80.png)[/bold white]")
        output_path = Prompt.ask("[bold white]Enter the path to save the output image (e.g., pokemon_back_32x32_grayscale.png)[/bold white]")
        convert_sprite(input_path, output_path, sprite_type="back")
    elif choice == "3":
        console.print("[bold red]Exiting...[/bold red]")
    else:
        console.print("[bold red]Invalid choice, please select 1, 2, or 3.[/bold red]")
        menu()

if __name__ == "__main__":
    menu()
