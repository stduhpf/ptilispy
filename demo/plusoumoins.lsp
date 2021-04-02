;un "plus ou moins" classique
(noret
	;"load new" permet de créer un nouvel environement de vraiables et fonctions qui seront innaccessibles a moins de le recharger explicitement 
	(load new inputs
		(noret
			(defun inputInt (text)
				(retlast
					(define n "")
					(while (= n "")
						(try
							(set n (intcast (input text)))
							(set n "")
						)
					)
					n
				)
			)
			(defun inputFloat (text)
				(retlast
					(define n nil)
					(while (= n nil)
						(try
							(set n (floatcast (input text)))
							(set n nil)
						)
					)
					n
				)
			)
		)
	)
	;on peut inclure les variables et fonctions venant d'autres fichiers
	(load file "demo/include.lsp" rec)
	(defun main (args)
		(retlast
			(define attempts 0)
			;on peut définir des fonctions locales
			(defun hautbas (h t)
				(if (< h t) 
					(
						print "Trop haut"
					)
					(
						if(> h t)
						(
							print "trop bas"
						)
					)
				)
			)
			;on peut charger des environements pour un bloc de code
			(load inputs
				(noret
					(define upperBound (inputInt "Borne maximale:"))
					;on peut charger des environements pour une seule instruction
					(define hiddenNumber (load random (randInt 0 upperBound)))
					(define test -1)
					(while (/= hiddenNumber test)
						(set test (inputInt "Votre supposition:"))
						(hautbas hiddenNumber test)
						(inc attempts)
					)
					(print "bravo")
				)
			)
			attempts
		)
	)
)
