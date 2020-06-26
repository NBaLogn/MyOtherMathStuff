from GEB.Chapter8TNT.Properties import is_var, get_vars, get_free_vars, is_num, \
                                       get_bound_vars, is_term, is_atom, is_well_formed
from GEB.Chapter8TNT.StripSplit import split_eq, replace_var, replace_var_nth, \
                                       split


# Build abitrary statements in Typographical Number Theory
def EXISTS(x,a):
    if is_var(a):
        if a in get_free_vars(x):
            return f"∃{a}:{x}"
        else:
            if a in get_bound_vars(x):
                raise Exception(f"Quantification Error: {a} is already quantified in {x}")
            else:
                raise Exception(f"Quantification Error: {a} does not exist in {x}")
    else:
        raise Exception(f"Quantification Error: {a} is not a variable")
	
def FOR_ALL(x,a):
    if is_var(a):
        if a in get_free_vars(x):
            return f"∀{a}:{x}"
        else:
            if a in get_bound_vars(x):
                raise Exception(f"Quantification Error: {a} is already quantified in {x}")
            else:
                raise Exception(f"Quantification Error: {a} does not exist in {x}")
    else:
        raise Exception(f"Quantification Error: {a} is not a variable")

def AND(x,y):
    if not is_well_formed(x):
        raise Exception(f"Logical Error: {x} is not a well-formed formula")
    if not is_well_formed(y):
        raise Exception(f"Logical Error: {y} is not a well-formed formula")
    return f"<{x}∧{y}>"
	
def OR(x,y):
    if not is_well_formed(x):
        raise Exception(f"Logical Error: {x} is not a well-formed formula")
    if not is_well_formed(y):
        raise Exception(f"Logical Error: {y} is not a well-formed formula")
    return f"<{x}∨{y}>"
	
def IMPLIES(x,y):
    if not is_well_formed(x):
        raise Exception(f"Logical Error: {x} is not a well-formed formula")
    if not is_well_formed(y):
        raise Exception(f"Logical Error: {y} is not a well-formed formula")
    return f"<{x}⊃{y}>"
	
def NOT(x,):
	return f"~{x}"

def SUCC(x):
	if is_term(x):
		return f"S{x}"
	else:
		raise Exception(f"Cannot have successor of {x}")
  
def ADD(x,y):
	return f"({x}+{y})"

def MUL(x,y):
	return f"({x}⋅{y})"

def EQ(x,y):
	return f"{x}={y}"

###############################
##### Rules of Production #####
###############################

# Change a general statement into a specifice assertion
def specify(x,var,term):
    if not is_term(term):
        raise Exception(f"Specification Error: {term} is not a term")
    if f"∀{var}:" in x:
        # Eliminate the quantifer
        x = x.replace(f"∀{var}:","")
        
        # Check if replacement is allowed
        x_b_vars = get_bound_vars(x)
        term_vars = get_vars(term)
        for tv in term_vars:
            for xbv in x_b_vars:
                if tv in xbv:
                    raise Exception(f"Specification Error: {tv} is bound in {x}")
        
        x = replace_var(x,var,term)
        return x
    else:
        raise Exception(f"Specification Error: {var} is not universally quantified in {x}")


# Assert that a statement about a free variable is universally true
def generalize(x,u):
    if u in get_free_vars(x):
        return FOR_ALL(x,u)
    else:
        raise Exception(f"Generalization Error: {u} is not free in {x}")


# Rephrase the existential quantifier as a universal quantifer
def interchange_EA(x,variable,n):
    if is_var(variable):
        E = f"~∃{variable}:"
        A = f"∀{variable}:~"
        return replace_var_nth(x,E,A,n)
    else:
        raise Exception(f"Interchange Error: {variable} is not variable")


# Rephrase the universal quantifier as an existential quantifer
def interchange_AE(x,variable,n):
    if is_var(u):
        E = f"~∃{variable}:"
        A = f"∀{variable}:~"
        return replace_var_nth(x,A,E,n)
    else:
        raise Exception(f"Interchange Error: {variable} is not variable")


def successor(x):
    if is_atom(x):
        left, right = split_eq(x)
        return f"S{left}=S{right}"
    else:
        raise Exception(f"Successor Error: {x} is not an atom")


def predecessor(x):
    if is_atom(x):
        left, right = split_eq(x)
        if left[0] != "S":
            raise Exception(f"Predecessor Error: {left} has no predecessor")
        if right[0] != "S":
            raise Exception(f"Predecessor Error: {right} has no predecessor")
            
        return f"{left[1:]}={right[1:]}"
    else:
        raise Exception(f"Predecessor Error: {x} is not an atom")


def existence(x,term,var):
    if not is_var(var):
        raise Exception(f"Existence Error: {var} is not a valid variable")
    if is_term(term):
        if var in get_bound_vars(x):
            raise Exception(f"Existence Error: {var} is already bound in {x}")
        else:
            x = replace_var(x,term,var)
            return EXISTS(x,var)
    else:
        raise Exception(f"Existence Error: {term} is not a valid term")


def symmetry(x):
    if is_atom(x):
        left, right = split_eq(x)
        return f"{right}={left}"
    else:
        raise Exception(f"Symmetry Error: {x} is not an atom")


def transitivity(x,y):
    if not is_atom(x):
        raise Exception(f"Transitivity Error: {x} is not an atom")
    if not is_atom(y):
        raise Exception(f"Transitivity Error: {y} is not an atom")

    # Split and recombine
    leftx, rightx = split_eq(x)
    lefty, righty = split_eq(y)
    if rightx == lefty:
        return f"{leftx}={righty}"
    else:
        raise Exception(f"Transitivity Error: {x} and {y} do not form a transitive statement")
        
        
def induction(x,u,T):
    if u not in get_free_vars(x):
        raise Exception(f"Induction Error: {u} is not free in {x}")
    
    xS = replace_var(x,u,f"S{u}")
    x0 = replace_var(x,u,"0")
    
    if f"∀{u}:<{x}⊃{xS}>" in T and f"{x0}" in T:
        return f"∀{u}:{x}"
    else:
        raise Exception(f"Induction Error: Theorems do not allow induction on {x}")





if __name__ == '__main__':
    
    print("\n\nRule of Specification")
    print(f"{PeanoAxioms[1]} ⟹ {specify(PeanoAxioms[1],'a','(c+d)')}")
    print(f"{PeanoAxioms[3]} ⟹ {specify(PeanoAxioms[3],'a','(S0⋅0)')}")
    print(f"{PeanoAxioms[4]} ⟹ {specify(PeanoAxioms[4],'b','(S0+b)')}")
    
    
    print("\n\n\nRules of Successorship")
    succ_example = "SSS0=S(S0+S0)"
    print(f"{succ_example} ⟹ {successor(succ_example)}")
    print(f"{succ_example} ⟹ {predecessor(succ_example)}")
    
    
    print("\n\n\nRule of Generalization")
    gen_example = "~S(c+SS0)=0"
    print(f"{gen_example} ⟹ {generalize(gen_example,'c')}")

    
    print("\n\n\nRule of Existence")
    print(f"{PeanoAxioms[0]} ⟹ {existence(PeanoAxioms[0],'0','b')}")
    print(f"{PeanoAxioms[2]} ⟹ {existence(PeanoAxioms[2],'Sb','c')}")
    
    
#    print("\n\n\nRule of Transitivity")
#    trans_example1 = "(a+b)=(a+S0)"
#    trans_example2 = "(a+S0)=S(a+0)"
#    trans_example3 = AND(trans_example1,trans_example2)
#    print(f"{trans_example1}")
#    print(f"{trans_example2}")
#    print(f"{trans_example3}")
#    print(f"{transitivity(trans_example3)}")


    print("\n\n\nRule of Symmetry")
    symm_example1 = "∀a:(a+0)=a"
    print(f"{symm_example1}")
    print(f"{symmetry(symm_example1)}")
