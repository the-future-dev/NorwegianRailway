import os

from rich.console      import Console
from rich.text         import Text
from rich.prompt        import Prompt
from code.init          import create_tables, insert_tables                     #Opgave  A, B, F
from code.routeSearch   import get_train_routes, findRoutesDateTime             #Oppgave C, D
from code.customer      import register_customer, new_order, get_orders         #Oppgave E, G

console = Console()
db_path = 'database/railway.db'

def main(fileExists):
    if not fileExists: 
        create_tables(db_path)
        insert_tables(db_path)
    console.clear()
    text = [
        " _   _                               _               _____       _ _                     ",
        "| \ | |                             (_)             |  __ \     (_) |                    ",
        "|  \| | ___  _ ____      _____  __ _ _  __ _ _ __   | |__) |__ _ _| |_      ____ _ _   _ ",
        "| . ` |/ _ \| '__\ \ /\ / / _ \/ _` | |/ _` | '_ \  |  _  // _` | | \ \ /\ / / _` | | | |",
        "| |\  | (_) | |   \ V  V /  __/ (_| | | (_| | | | | | | \ \ (_| | | |\ V  V / (_| | |_| |",
        "|_| \_|\___/|_|    \_/\_/ \___|\__, |_|\__,_|_| |_| |_|  \_\__,_|_|_| \_/\_/ \__,_|\__, |",
        "                                __/ |                                               __/ |",
        "                               |___/                                               |___/ "
    ]

    for line in text:
        t = Text()
        for i, char in enumerate(line):
            t = Text(line[:51], style="red")
            t.append(line[51:], style="white")
        console.print(t)
        
    funcUser = '' 
    while funcUser != '0':
        funcUser = Prompt.ask('\n MENU \n [bold cyan]1[/bold cyan] Get all train routes that stop at a particular station on a given weekday \n [bold cyan]2[/bold cyan] Search Routes \n [bold cyan]3[/bold cyan] Signup \n [bold cyan]4[/bold cyan] Buy Tickets \n [bold cyan]5[/bold cyan] Retrieve orders\n [bold cyan]0[/bold cyan] Exit \n > ')
        if funcUser == '1':
            get_train_routes(db_path)
        elif funcUser == '2':
            findRoutesDateTime(db_path)
        elif funcUser == '3':
            register_customer(db_path)
        elif funcUser == '4':
            new_order(db_path)
        elif funcUser == '5':
            get_orders(db_path)
fileExists = True
if not os.path.exists(db_path):
    fileExists = False

main(fileExists)