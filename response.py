def help():
    help = ('Hello π€©π\n\n'
          'π Recherche par youtube ==> ytb <video rechercher> (exemple: ytb zezika) \n\n'
          'π Recherche sur google ==> gg <mot cle> (exemple: gg zavatra) \n\n'
          "J'espΓ¨re vous Γͺtre utile. π¨βπ§")
    return help

def other():
    other = ("π€©π Bienvenue sur le HooLLa BoT π€©π\n"
             "On est heureux de pouvoir vous aider,\n\n"
             "envoyer le message π'HELP'π si vous avez besoin d'aide")
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