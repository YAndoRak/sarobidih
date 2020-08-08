def help():
    help = ('Help : Bienvenue sur le HooLLa BoT 🤩👋\n'
          'Ici vous pouvez faire des recherche sur google et youtube en utilisant les syntaxes suivantes 🤳:\n\n'
          '\t🔑 Recherche par youtube \t==> \t ytb <video rechercher> 🎞️\n'
          '\t🔑 Recherche par google \t==> \t gg <mot cle  à rechercher> 🔍\n\n'
          "Si malgrès tous cela ne marche pas 😧 , je vous invite à envoyer un message aux responsables directement par MP 😎\n"
          "J'espère vous être utile. 👨‍🔧\n"
          "Profiter au maximum 💯")
    return help

def other():
    other = ("🤩👋 Bienvenue sur le HooLLa BoT 🤩👋\n"
             "On est heureux de pouvoir vous aider,\n\n"
             "entrer le message 🆘'HELP'🆘 si vous avez besoin d'aide")
    return other



if __name__ == "__main__":
    help = help()
    print(help)
    print('========================')
    other = other()
    print(other)
    print('========================')
    test = 'test'
    print(test.upper())