import ptilis
################################################################
### -----------------------  Tests  ------------------------ ###


if __name__ == "__main__":
    a = ptilis.parseAndRunFile("demo/syracuse.lsp", [27], repl=False)
    print("execution terminée avec valeur " + str(a))
    a = ptilis.parseAndRunFile("demo/plusoumoins.lsp", repl=False,
                               env=ptilis.default_environement())
    print("execution terminée avec valeur " + str(a))
    a = ptilis.parseAndRunFile("demo/tests.lsp", repl=False,
                               env=ptilis.default_environement())
    print("execution terminée avec valeur " + str(a))
