import csv
import os
import time
import platform
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from rich.style import Style
import pandas as pd
import click


def resize_terminal(columns, lines):
    current_os = platform.system()
    if current_os == 'Windows':
        os.system(f'mode con: cols={columns} lines={lines}')
    elif current_os in ['Linux', 'Darwin']:  # Darwin est le nom de base de macOS
        os.system(f'printf "\\e[8;{lines};{columns}t"')
    else:
        print(f"Redimensionnement du terminal non supporté pour l'OS: {current_os}")
def ReadCsv():
    with open("datas.csv", "r") as file:
        reader = csv.DictReader(file, delimiter=",")
        data = list(reader)
    return data

def CreateCsv():
    with open('datas.csv', 'w', newline='') as csvfile:
        fieldnames = ["Nom", "Type", "Catégorie", "Description", "URL", "Fonctionnalités", "Prix", "Évaluation", "Commentaires", "Développeur/Éditeur"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def CheckCsvFile():
    if not os.path.exists('datas.csv'):
        CreateCsv()
    return ReadCsv()

# Affichage d'une ligne de trait
# def AfficherCsv(datas):
#     if not datas:
#         print("Le fichier CSV est vide...")
#         return

#     space = ''
#     print(f'{space:-^150}')
#     # affichage de la première ligne # celle qui contient les clés 
#     print("|", end="")
#     for cle in datas[0]:
#         print(f'{cle:^15}|', end="")
#     print()
#     print(f'|{space:-^150}|')
#     # affichage des lignes du tableau
#     for dict in datas:
#         a = dict['Nom']
#         b = dict['Type']
#         c = dict['Catégorie']
#         d = dict['Description']
#         e = dict['URL']
#         f = dict['Fonctionnalités']
#         g = dict['Prix']
#         h = dict['Évaluation']
#         i = dict['Commentaires']
#         j = dict['Développeur/Éditeur']
#         print(f"|{a:^50}|{b:^50}|{c:^50}|")
#         print(f"|{d:^50}|{e:^50}|{f:^50}|")
#         print(f"|{g:^50}|{h:^50}|{i:^50}|")
#         print(f"|{j:^50}|")
        
#         print(f'|{space:-^212}|')

def Main():
    # resize_terminal(222,50)
    # content = CheckCsvFile()
    # AfficherCsv(content)
    resize_terminal(222,50)
    content = CheckCsvFile()
    ShowCsv(content)

        
def ShowCsv(datas):

    console = Console()
    table = Table(title="Liste des Sites et Applications", style="bold yellow")

    # Ajout des colonnes
    table.add_column("Nom", style="cyan", no_wrap=True,overflow="fold")
    table.add_column("Type", style="yellow",overflow="fold")
    table.add_column("Catégorie", style="green",overflow="fold")
    table.add_column("Description", style="blue",overflow="fold")
    table.add_column("URL", style="magenta", overflow="fold")
    table.add_column("Fonctionnalités", style="white",overflow="fold")
    table.add_column("Prix", style="red",overflow="fold")
    table.add_column("Évaluation", style="bold white",overflow="fold")
    table.add_column("Commentaires", style="dim",overflow="fold")
    table.add_column("Développeur/Éditeur", style="bold cyan",overflow="fold")


    for dict in datas:
        table.add_row(
            dict['Nom'], 
            dict['Type'], 
            dict['Catégorie'], 
            dict['Description'], 
            dict['URL'], 
            dict['Fonctionnalités'], 
            dict['Prix'], 
            f"{dict['Évaluation']} / 5", 
            dict['Commentaires'], 
            dict['Développeur/Éditeur']
        )
        num_columns = 10  # Par exemple, ajustez selon le nombre de colonnes dans votre table

        # Créer une ligne remplie de tirets pour toute la largeur de la table
        divider_row = ["--" * 9] * num_columns

        # Ajouter la ligne de séparation à la table
        table.add_row(*divider_row,style="blue")

        # Affichage de la table
    console.print(table)
    
def FilterCsvSafe(csv_file, category, value):
    filtered_data = []
    
    try:
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Lire les en-têtes de colonnes
            
            if category not in headers:
                raise ValueError(f"La valeur n'a pas été trouvé dans la catégorie {category}")
            
            for row in reader:
                row_dict = dict(zip(headers, row))
                if row_dict[category] == value:
                    filtered_data.append(row_dict)
    
    except FileNotFoundError:
        print(f"Le fichier '{csv_file}' n'a pas été trouvé.")
    
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV : {str(e)}")
    
    return filtered_data

def ShowFilteredResult(category,value):
    filtered_data = FilterCsvSafe('datas.csv', category, value)
    ShowCsv(filtered_data)

  
def Menu():
    ascci_menu = r"""
  _____       _        _____ _ _                         
 |  __ \     | |      / ____(_) |                        
 | |__) |__ _| |_ ___| (___  _| |_ ___       _ __  _   _ 
 |  _  // _` | __/ _ \\___ \| | __/ _ \     | '_ \| | | |
 | | \ \ (_| | ||  __/____) | | ||  __/  _  | |_) | |_| |
 |_|  \_\__,_|\__\___|_____/|_|\__\___| (_) | .__/ \__, |
                                            | |     __/ |
                                            |_|    |___/ 
"""
    resize_terminal(222,50)

    print(ascci_menu)
    console = Console()

    panel = Panel.fit("[bold green]1) Afficher tout le contenu de la base de donnée [/bold green]\n[bold green]2) Trier et afficher le contenu de la base de donnée [/bold green]\n[bold green]3) Ajouter un site/app à la base de donnée [/bold green]", title="Choix possibles :", style="on white")
    console.print(panel)
    console.print()
    
    valid_input = False
    user_input = "0"
    while valid_input != True:
        choice = input("Entrez votre choix : ")
        if choice in ['1', '2', '3']:
            valid_input = True
            user_input = choice
        else:
            console.print("Erreur : Veuillez entrer un choix valide.", style="bold red")
    
    # Maintenant user_input est une chaîne de caractères '1', '2' ou '3'
    if user_input == '1':
        panel = Panel.fit("[bold red]Vous allez maintenant consulter l'entièreté de la base de donnée ! \n[/bold red]", style="on white")
        console.print(panel)
        console.print()
        contenu_csv = CheckCsvFile()
      
        ShowCsv(contenu_csv)
    elif user_input == '2':
        panel = Panel.fit("[bold red]Vous pouvez trier suivant ces différents filtres, faites attention la recherches est précise sur ce que vous entrez :  \n Nom,Type,Catégorie,Description,URL,Fonctionnalités,Prix,Évaluation,Commentaires,Développeur/Éditeur [/bold red]", title="Choix possibles :", style="on white")
        console.print(panel)
        console.print()

        InputValid = False
        category = ""
        while InputValid != True:
            choice = input("Entrez votre choix : ")
            #fautes d'orthographe comprise dans l'input, si ça c'est pas du professionnalisme !  
            if choice in ["Nom","nom","TYPE","type","Type","Catégorie","catégorie","Categorie","categorie","Catégore","catégore","Categore","categore","Description","description","Desciption","desciption","URL","url","URl","uRL","Fonctionnalités","fonctionnalités","Fonctionnalites","fonctionnalites","Fonctionalités","fonctionalités","Fonctionsalités","fonctionsalités","Prix","prix","Pris","pris","Évaluation","évaluation","Evaluation","evaluation","Ealuation","ealuation","Commentaires","commentaires","Comentaires","comentaires","Développeur","développeur","Developpeur","developpeur","Dévlopper","dévlopper","Editeur","éditeur","Editeurr","éditeurr"]:
                InputValid = True
                category = choice
            else:
                console.print("Erreur : Veuillez entrer un choix valide.", style="bold red")

        panel_content = (
            "[bold green] Vous avez sélectionné une catégorie, maintenant choisissez un terme à rechercher : \n"
            "[yellow]Nom : //[/yellow] \n"
            "[yellow]Type :[/yellow] [blue]IA[/blue], [blue]Application[/blue], [blue]Site web[/blue] \n"
            "[yellow]Catégorie :[/yellow] [blue]Productivité[/blue], [blue]Développement[/blue], [blue]Communication[/blue], [blue]Divertissement[/blue], [blue]Éducation[/blue] \n"
            "[yellow]Description : //[/yellow] \n"
            "[yellow]URL : //[/yellow] \n"
            "[yellow]Fonctionnalités : //[/yellow] \n"
            "[yellow]Prix :[/yellow] [blue]Gratuit avec options payantes[/blue], [blue]Gratuit[/blue], [blue]Payant[/blue] \n"
            "[yellow]Évaluation :[/yellow] ?? /5 \n"
            "[yellow]Commentaires : //[/yellow] \n"
            "[yellow]Développeur/Éditeur [/yellow]:[blue] // sauf si vous avez le nom précis[/blue] \n"
            "[red]Tout les // signifie que je ne vous conseille pas de rechercher par ce critère !\n\n Mais le plus simple c'ets que si vous avez un accès direct au fichier CSV regardez l'intitulé exact de la colone....[/red] \n"
            "[/bold green]"
        )

        panel = Panel.fit(panel_content, title="Par quoi devriez vous rechercher ? ", style="on white")
        console.print(panel)
        console.print()

        value = str(input(f"Quel mot clé souhaitez vous rechercher dans {category} : "))


        ShowFilteredResult(category,value)
    elif user_input == '3':
        ajouter_au_csv("datas.csv")        


def ajouter_au_csv(fichier_csv):
    console = Console()

    panel = Panel.fit("Vous allez maintenant pouvoir ajouter un site à la base de donnée ! ", style="on white")
    console.print(panel)
    console.print()

    nom = input("Nom : ")
    type_ = input("Type : ")
    categorie = input("Catégorie : ")
    description = input("Description : ")
    url = input("URL : ")
    fonctionnalites = input("Fonctionnalités : ")
    prix = input("Prix : ")
    evaluation = input("Évaluation : ")
    commentaires = input("Commentaires : ")
    developpeur_editeur = input("Développeur/Éditeur : ")

    # Écrire les entrées dans le fichier CSV
    with open(fichier_csv, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            nom,
            type_,
            categorie,
            description,
            url,
            fonctionnalites,
            prix,
            evaluation,
            commentaires,
            developpeur_editeur
        ])
# Utilisation de la fonction

############## MAIN ##############
Menu()