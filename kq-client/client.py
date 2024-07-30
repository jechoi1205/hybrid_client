from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich import box
from kisti_clientpkg.job_mgmt import *
from kisti_clientpkg.submit_file import M_submit_file
from kisti_clientpkg.submit_hybrid_job import submit_hybrid_job
from kisti_clientpkg.resource_mgmt import *
from kisti_clientpkg.CHSH_ineq_RYU_test import CHSH_client_part

console = Console()

def display_menu():
    while True:
        console.clear()
        console.print(Panel("KISTI's client console for hybrid interface", style="bold magenta", width=50))
        
        table = Table(show_header=True, header_style="bold green", box=box.SQUARE_DOUBLE_HEAD)
        table.add_column("Option", justify="center", style="dim", width=8)
        table.add_column("Description", width=35, style="italic")
        
        table.add_row("[ 1 ]", "Get resource information")
        table.add_row("[ 2 ]", "Update resource status (on/off)")
        table.add_row("-", "-" * 20)
        table.add_row("[ 3 ]", "Submit files to API server", style="red")
        table.add_row("[ 4 ]", "Check job manager")
        table.add_row("[ 5 ]", "Submit hybrid job", style="red")
        table.add_row("[ 6 ]", "Check job information")
        table.add_row("[ 7 ]", "Delete job")
        table.add_row("[ 8 ]", "Get job status")
        table.add_row("[ 9 ]", "Get job result")
        table.add_row("-", "-" * 20)
        table.add_row("[ 0 ]", "Exit")
        
        console.print(table)
        
        num = Prompt.ask("[bold cyan]Enter the option")
        
        if num == '1':
            get_resource(True)
        elif num == '2':
            patch_resource()
        elif num == '3':
            M_submit_file()
        elif num == '4':
            check_job_manager()
        elif num == '5':
            #submit_hybrid_job()
            CHSH_client_part()
        elif num == '6':
            job_uuid = Prompt.ask("Enter job UUID")
            check_job_info(job_uuid)
        elif num == '7':
            job_uuid = Prompt.ask("Enter job UUID")
            delete_job(job_uuid)
        elif num == '8':
            job_uuid = Prompt.ask("Enter job UUID")
            get_job_status(job_uuid)
        elif num == '9':
            job_uuid = Prompt.ask("Enter job UUID")
            get_job_result(job_uuid)
        elif num == '0':
            console.print("Exiting the client program...", style="bold red")
            break
        else:
            console.print("Invalid choice. Please enter a number between 0 and 9.", style="bold yellow")
        
        console.print("")
        again = Confirm.ask("[bold cyan]Would you like to execute the menu again?[/]")
        if not again:
            console.print("Exiting...", style="bold red")
            break

if __name__ == "__main__":
    display_menu()
