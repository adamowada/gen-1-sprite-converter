import click
from PIL import Image
from rich.console import Console
from rich.prompt import Prompt


console = Console()


# Function to map image pixels to white, light gray, dark gray, and black
def map_colors(img):
    # Define thresholds for remapping colors
    white = 255
    light_gray = 170
    dark_gray = 85
    black = 0

    # Load image data for processing
    img_data = img.load()

    # Iterate over every pixel in the image
    for y in range(img.height):
        for x in range(img.width):
            pixel_value = img_data[x, y]
            if pixel_value >= 192:
                img_data[x, y] = white  # White
            elif pixel_value >= 128:
                img_data[x, y] = light_gray  # Light gray
            elif pixel_value >= 64:
                img_data[x, y] = dark_gray  # Dark gray
            else:
                img_data[x, y] = black  # Black

    return img


# Function to convert sprite to correct dimensions and format for Gen 1 games
def convert_sprite(input_path, output_path, sprite_type="front"):
    # Open the input image and ensure RGBA (with alpha channel)
    img = Image.open(input_path).convert("RGBA")

    # Create a white background image the same size as the input
    white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))  # Fully white background

    # Paste the input image on top of the white background, which fills transparent pixels with white
    img_with_white_bg = Image.alpha_composite(white_bg, img)

    # Convert the image to grayscale
    img_grayscale = img_with_white_bg.convert('L')

    # Determine dimensions based on the sprite type
    if sprite_type == "front":
        new_size = (56, 56)  # Front sprites are 56x56
    elif sprite_type == "back":
        new_size = (32, 32)  # Back sprites are 32x32
    else:
        raise ValueError("Invalid sprite_type. Choose 'front' or 'back'.")

    # Resize the image to the correct dimensions
    img_resized = img_grayscale.resize(new_size, Image.Resampling.LANCZOS)

    # Map pixels to the four colors: white, light gray, dark gray, and black
    img_mapped = map_colors(img_resized)

    # Save the resulting image as PNG
    img_mapped.save(output_path, "PNG")
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
