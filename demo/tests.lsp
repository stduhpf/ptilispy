(noret
	(define compareTo 750)
	(defun sqr (x)(retlast
		(print x "^2 = " (* x x))
		(* x x)
	))
	(defun fib (n) 
		(retlast
			(define k 1)
			(define kk k)
			(for (define i 2) (< i n) (incf i 1) 
				(define temp k)
				(set k (+ k kk))
				(set kk temp)
			)
			k
		)
	)
	(defun fact (n)
		(retlast
			(define ret)
			(if (<= n 1)
				(set ret 1)
				;else
				(set ret (* n (fact (- n 1))))
			)
			ret
		)
	)
	(defun ^ (a b) 
		(retlast
			(define p 1)
			(for (define i 0) (< i b) (incf i 1)
				(set p (* p a))
			)
			p
		)
	)
	(defun main (args)
		(load math
			(retlast
				(define r 0)
				(for (define i 0) (<= i 10) (incf i 1)
					(set r (+ r i))
					(define res (* pi (sqr r)))
					(print "Le resultat de " r "*" r "* pi est :" res)
;commentaire pour explique que je compare le
;résultat a la valeur de compareTo
					(print 
						(if (> res compareTo)
							"plus grand" 
							"plus petit"
						)
						"que" compareTo
					)
					(print)
				)
				(define l (list 1 2 3 5 9))
				(print l (elem l 3))
				(define a 10)
				(cond 
					((> a 5)
						(print " a >  5")
					)
					((> a 20)
						(print " a > 20")
					)
					(t 
						(print "a =" a)
					)
				)
				(^ 2 (fib (fact 3) ) )
				(load random 
					(randInt 0 100)
				)
			)
		)
	)
)