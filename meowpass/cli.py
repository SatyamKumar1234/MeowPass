import json
import os
import sys
import subprocess
import importlib.util

from rich.console import Console
from rich.panel import Panel
from art import tprint
from .core import load_data, generate_base_words, apply_mangling_rules, enhance_with_ai

console = Console()

def check_and_install_ai_deps():
    """Checks for AI libraries and prompts the user to install them if missing."""
    packages = {
        'google-generativeai': 'Google Gemini',
        'openai': 'OpenRouter'
    }
    missing_packages = [pkg for pkg in packages if importlib.util.find_spec(pkg) is None]
    
    if not missing_packages: return True

    console.print(Panel(
        f"[bold yellow]To use AI-Assisted Mode, the following are needed:[/bold yellow]\n- " + 
        "\n- ".join([f"[cyan]{pkg}[/cyan]" for pkg in missing_packages]),
        title="Optional Dependencies Missing", border_style="yellow"
    ))
    
    if console.input("[bold]Install them now? (y/n): [/bold]").lower() != 'y':
        console.print("[red]Installation declined. Cannot proceed with AI-Assisted Mode.[/red]")
        return False
        
    for pkg in missing_packages:
        with console.status(f"[bold green]Installing {pkg}...[/]"):
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", pkg], check=True, capture_output=True)
                console.print(f"-> [green]Successfully installed {pkg}.[/green]")
            except subprocess.CalledProcessError as e:
                console.print(Panel(f"[bold red]Failed to install {pkg}.[/bold red]", title="Installation Error", border_style="red"))
                return False
    console.print("[green]All AI dependencies are installed![/green]")
    return True

def is_sensitive_path(path):
    abs_path = os.path.abspath(path).lower()
    sensitive_paths = (
        [os.path.normpath(p).lower() for p in ['c:/windows', 'c:/program files', 'c:/users']] 
        if sys.platform == "win32" else 
        ['/etc', '/usr', '/bin', '/sbin', '/root', '/boot', '/dev', '/sys']
    )
    for sensitive in sensitive_paths:
        if abs_path.startswith(sensitive): return True
    return False

def save_wordlist(wordlist, base_filename):
    console.print(Panel(f"The wordlist contains [cyan]{len(wordlist)}[/cyan] passwords.", title="Ready to Save"))
    console.print("\n[bold]Save location?[/bold] (1) Current directory (default) (2) Custom directory")
    choice = console.input("[bold]Enter choice: [/bold]")
    save_path = ""
    if choice == '2':
        while True:
            custom_dir = console.input("[cyan]Enter full directory path: [/cyan]")
            if not os.path.isdir(custom_dir):
                console.print("[yellow]Directory does not exist.[/yellow]"); continue
            if is_sensitive_path(custom_dir):
                console.print(Panel("[bold red]SECURITY WARNING: Not allowed.[/bold red]", title="Warning", border_style="red")); continue
            save_path = os.path.join(custom_dir, base_filename)
            break
    else:
        save_path = os.path.join(os.getcwd(), base_filename)
    try:
        with open(save_path, 'w') as f: json.dump({"passwords": wordlist}, f, indent=4)
        summary = f"[bold]Total Passwords:[/bold] [cyan]{len(wordlist)}[/cyan]\n[bold]Location:[/bold] [cyan]{save_path}[/cyan]"
        console.print(Panel(summary, title="[bold green]Generation Complete[/bold green]", border_style="green"))
    except Exception as e:
        console.print(Panel(f"[bold red]Failed to save file:[/bold red] {e}", title="Error", border_style="red"))

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    tprint("MEOWPASS", font="block", chr_ignore=True)
    console.print("[bold cyan]                                by GgSatyam[/bold cyan]")
    console.print(Panel("A personalized wordlist generator for security research.", title="Welcome", border_style="green"))
    console.print("\n[bold]Choose a mode:[/bold]\n  [cyan](1) Normal[/cyan]\n  [magenta](2) AI-Assisted[/magenta]\n  (3) Quit")
    choice = console.input("[bold]Enter choice: [/bold]")

    if choice == '3':
        console.print("\n[bold yellow]Exiting MEOWPASS. Goodbye![/bold yellow]"); return
        
    if choice in ['1', '2']:
        # Hardcoded path to the data.json file as requested.
        data_path = "d:\\VS Code\\vs code codefiles\\meowpass-project\\data.json"

        user_data = load_data(data_path)
        if user_data is None: console.print(Panel(f"[bold red]ERROR: File not found at the hardcoded path '[cyan]{data_path}[/cyan]'. Please ensure the file exists.[/bold red]", title="File Error", border_style="red")); return
        if user_data == "JSON_ERROR": console.print(Panel(f"[bold red]ERROR: The file at '[cyan]{data_path}[/cyan]' is corrupt.[/bold red]", title="File Error", border_style="red")); return

        console.print("\n[bold yellow]Step 1: Generating base words...[/bold yellow]")
        base_words = generate_base_words(user_data)
        
        console.print("\n[bold yellow]Step 2 (Normal Mode): Applying systematic rules...[/bold yellow]")
        normal_wordlist = apply_mangling_rules(base_words)
        
        final_wordlist, output_filename = normal_wordlist, "meowpass_normal.json"
        
        if choice == '2':
            if check_and_install_ai_deps():
                console.print(Panel("[yellow]AI-Assisted mode may incur API costs.[/yellow]\n[bold]Continue? (y/n)[/bold]"))
                if console.input("> ").lower() == 'y':
                    num_passwords = 50
                    try:
                        req_count = console.input("[bold]How many new AI passwords? (default: 50): [/bold]")
                        if req_count.strip() and 1 <= int(req_count) <= 200: num_passwords = int(req_count)
                    except ValueError: pass
                    
                    console.print("[bold cyan]Select AI provider:[/bold cyan] (1) Google Gemini (2) OpenRouter")
                    provider_choice = console.input("[bold]Enter choice: [/bold]")
                    api_key = console.input("[bold]Please enter your API key: [/bold]")
                    
                    if api_key:
                        model_name = ""
                        if provider_choice == '2': model_name = console.input("[bold]Enter OpenRouter model (e.g., [cyan]mistralai/mistral-7b-instruct[/cyan]): [/bold]")
                        status, enhanced_list = enhance_with_ai(normal_wordlist, user_data, console, provider_choice, api_key, num_passwords, model_name)
                        
                        if status == "SUCCESS":
                            console.print(f"-> [green]AI enhancement successful.[/green]")
                            final_wordlist, output_filename = enhanced_list, "meowpass_ai_enhanced.json"
                        else:
                            console.print(Panel(f"[bold red]AI Failed:[/bold red] {status}", title="AI Error", border_style="red"))
        if final_wordlist:
            save_wordlist(final_wordlist, output_filename)
    else:
        console.print("\n[bold red]Invalid choice.[/bold red]"); return

if __name__ == "__main__":
    main()