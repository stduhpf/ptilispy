;exemples de fonctions récursives
;recursion_depth 10000
(noret
    (defun syracuse (n)
        (retlast
            (print n)
            (if (or(= n 0)(= n 1))
                (retfirst 1)
                (if (=(rem n 2)0)
                    (syracuse (intcast (/ n 2)))
                    (syracuse (+(* 3 n)1))
                )
            )
        )
    )
    (defun fact (n)
        (if (<= n 1)(retfirst 1)(* n (fact (- n 1))))
    )    
)