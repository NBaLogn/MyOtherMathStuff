from GEB.Chapter8TNT.Properties import is_well_formed, get_free_vars
from GEB.Chapter8TNT.Rules import IMPLIES, AND, OR, specify, symmetry, existence, \
                                  successor, predecessor, transitivity, \
                                  induction, interchange_AE, interchange_EA, \
                                  generalize

PeanoAxioms = ["∀a:~Sa=0","∀a:(a+0)=a",
               "∀a:∀b:(a+Sb)=S(a+b)",
               "∀a:(a⋅0)=0","∀a:∀b:(a⋅Sb)=((a⋅b)+a)"]
AusterePeanoAxioms = ["∀a:~Sa=0","∀a:(a+0)=a",
                      "∀a:∀a':(a+Sa')=S(a+a')",
                      "∀a:(a⋅0)=0","∀a:∀a':(a⋅Sa')=((a⋅a')+a)"]

# Need to create a hierarchical structure
class Deduction:
    
    def __init__(self,title="Deduction"):
        
        # Simple traits
        # The user never needs to set depth or reality, they are derived from
        # the lower level
        self.depth = 0
        self.reality = None
        self.title = title
        self.theorems = []
        self.descriptions = []

    def __str__(self):
        return f"Deduction Object: {self.title}"

    def __repr__(self):
        return f"Deduction Object: {self.title}"

    def _pretty_theorems(self):
        """
        Write out the deduction with lines numbered from 1
        Fantasies are indented relative to their depth
        The fantasy will count its own steps and the reality below it only 
        counts one step in the form of implication
        """
        dent = ' '*self.depth*2
        
        if self.title == "":
            s = f"\n{dent}["
        else:
            s = f"\n{dent}{self.title}\n{dent}["
            
        for line,t in enumerate(self.theorems,1):
            line_number = f"({line})"
            if type(t) == Deduction:
                s += f"{t.pretty_theorems}"
            else:
                s += f"\n{dent}  {line_number:>4} {t}"
        
        s += f"\n{dent}]"
        return s


    def _theorems_and_descriptions(self):
        """
        Write out the theorems and their descriptions together otherwise the same as pretty_theorems
        """
        # Find the longest theorem and use that to space the theorems and descriptions
        
        dent = ' '*self.depth*2
        
        max_length = 0
        for t in self.theorems:
            if type(t) == Deduction:
                continue
            max_length = max(max_length,len(t))
            
        if self.depth == 0:
            s = f"{self.title}\n["
        else:
            s = f"\n{dent}["
        
        for line,(d,t) in enumerate(zip(self.descriptions,self.theorems),1):
            
            line_number = f"({line})"
            
            if type(t) == Deduction:
                s += f"{t.theorems_and_descriptions}"
            else:
                s += f"\n{dent}  {line_number:<4} {t:<{max_length}}  {d}"
        
        s += f"\n{dent}]"
        return s


    # Force one-based indexing since this make more sense when counting steps
    def __getitem__(self,n):
        if n > 0:
            return self.theorems[n-1]
        return self.theorems[n]


    ### Implement the actions allowed for inference in TNT ###

    def implication(self,comment=""):
        # Implication of a fantasy
        if self.reality == None:
            raise Exception("Implication rule only applies within a fantasy")
        else:
            self.reality.theorems.append(IMPLIES(self.theorems[0],self.theorems[-1]))
            self.reality.descriptions.append("implication"+comment)

    def fantasy(self,premise,title="Fantasy",comment=""):
        # Begin deduction on an arbitrary premise
        # It is one level higher than the Deduction that produces it and can
        # find that Deduction by checking for reality.
        d = Deduction(title)
        d.depth = self.depth+1
        d.reality = self
        d.add_premise(premise,comment)
        self.theorems.append(d)
        self.descriptions.append("fantasy")
        return d

    def add_premise(self,premise,comment=""):
        #At the lowest level we accept only axioms
        if self.depth == 0:
            if premise not in PeanoAxioms:
                raise Exception("Must begin with an axiom of TNT")
            self.theorems.append(premise)
            self.descriptions.append("axiom"+comment)
        else:
            # At all other levels we instead must filter hour misformed formulas
            if not is_well_formed(premise):
                raise Exception(f"The premise {premise} is not a well-formed formula")
                
            # Then we check if this is the first premise of a deduction
            # Any well-formed formula can be the first premise of a fantasy
            
            if len(self.theorems) == 0:
                self.theorems.append(premise)
                self.descriptions.append("fantasy premise"+comment)
            else:
                if premise not in self.reality.theorems:
                    raise Exception(f"{premise} does not exist at the level one step lower")
                self.theorems.append(premise)
                self.descriptions.append("premise"+comment)
                

    def specify(self,n,var,replacement=None,comment=""):
        if replacement == None:
            replacement = var
        T = specify(self.theorems[n-1],var,replacement)
        if is_well_formed(T):
            self.theorems.append(T)
            self.descriptions.append(f"specification of {n}"+comment)
        else:
            raise Exception(f"{T} is not well-formed")

    def symmetry(self,n,comment=""):
        T = symmetry(self.theorems[n-1])
        if is_well_formed(T):
            self.theorems.append(T)
            self.descriptions.append(f"symmetry of {n}"+comment)
        else:
            raise Exception(f"{T} is not well-formed")

    def existence(self,n,term,var,comment=""):
        T = existence(self.theorems[n-1],term,var)
        if is_well_formed(T):
            self.theorems.append(T)
            self.descriptions.append(f"existence of {n}"+comment)
        else:
            raise Exception(f"{T} is not well-formed")

    def generalize(self,n,var,comment=""):
        f_vars = get_free_vars(self.theorems[0])
        if var in f_vars:
            raise Exception("Cannot generalize on free variables of a fantasy premise")
        T = generalize(self.theorems[n-1],var)
        if is_well_formed(T):
            self.theorems.append(T)
            self.descriptions.append(f"generalization of {n}"+comment)
        else:
            raise Exception(f"{T} is not well-formed")

    def successor(self,n,comment=""):
        T = successor(self.theorems[n-1])
        if is_well_formed(T):
            self.theorems.append(T)
            self.descriptions.append(f"successor of {n}"+comment)
        else:
            raise Exception(f"{T} is not well-formed")

    def predecessor(self,n,comment=""):
        T = predecessor(self.theorems[n-1])
        if is_well_formed(T):
            self.theorems.append(T)
            self.descriptions.append(f"(predecessor of {n}"+comment)
        else:
            raise Exception(f"{T} is not well-formed")

    def transitivity(self,n1,n2,comment=""):
        T = transitivity(self.theorems[n1-1],self.theorems[n2-1])
        if is_well_formed(T):
            self.theorems.append(T)
            self.descriptions.append(f"transitivity of {n1} and {n2}"+comment)
        else:
            raise Exception(f"{T} is not well-formed")      

    def induction(self,theorem,var,n_base_case,n_general_case,comment=""):
        T = induction(theorem,var,self.theorems[n_base_case-1],self.theorems[n_general_case-1])
        if is_well_formed(T):
            self.theorems.append(T)
            self.descriptions.append(f"induction on {n_base_case} and {n_general_case}"+comment)
        else:
            raise Exception(f"{T} is not well-formed") 

    def interchange_AE(self,n,var,nth,comment=""):
        T = interchange_AE(self.theorems[n-1],var,nth=1)
        if is_well_formed(T):
            self.theorems.append(T)
            self.descriptions.append(f"change universal to existential in {n}"+comment)
        else:
            raise Exception(f"{T} is not well-formed") 

    def interchange_EA(self,n,var,nth,comment=""):
        T = interchange_EA(self.theorems[n-1],var,nth=1)
        if is_well_formed(T):
            self.theorems.append(T)
            self.descriptions.append(f"change existential to universal in {n}"+comment)
        else:
            raise Exception(f"{T} is not well-formed") 

    # Not one of Hofstader's rules of production but always produces a valid theorem
    def AND(self,n1,n2,comment=""):
        T = AND(self.theorems[n1-1],self.theorems[n2-1])
        if is_well_formed(T):
            self.theorems.append(T)
            self.descriptions.append(f"{n1} and {n2}"+comment)
        else:
            raise Exception(f"{T} is not well-formed") 

    # Not one of Hofstader's rules of production but always produces a valid theorem
    # Note that this is the logical inculsive OR
    def OR(self,n1,n2,comment=""):
        T = OR(self.theorems[n1-1],self.theorems[n2-1])
        if is_well_formed(T):
            self.theorems.append(T)
            self.descriptions.append(f"{n1} and {n2}"+comment)
        else:
            raise Exception(f"{T} is not well-formed") 

    pretty_theorems = property(_pretty_theorems)
    theorems_and_descriptions = property(_theorems_and_descriptions)

