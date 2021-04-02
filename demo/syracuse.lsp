(noret
	;on peut inclure les variables et fonctions venant d'autres fichiers
	(load file inc "demo/include.lsp")
	(defun main (args)
		(retlast
            (print args)
			;one peut appeler des fonctions récursives
            (try
                (retlast
                    (define n (intcast(elem args 0)))
			        (load inc (syracuse n))
                )(
                    print "no arguments"
                )
            )
		)
	)
)