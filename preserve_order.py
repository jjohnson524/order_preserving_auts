from math import gcd
import sys
from sage.all import *
import Ball, Braid, word_length

tree_dict={}
nodeUID = 0
tree_dict[str(nodeUID)]={'parent':'start','dvalue':'none','side':'none', 'name':'x1'}
extra_checks = 0

class ConeElement:

    def __init__(self,element, id = -1):
        self.id = id
        self.element = element
        self.type = 'Not Set'
        self.conj = 'None'
        self.dependencies = []

    def set_id(self,id):
        self.id=id

    def set_added_type(self):
        self.type = 'Added'
        self.conj = 'None'
        self.dependencies = []

    def set_image_type(self,id):
        self.type = 'Braid Image'
        self.conj = 'None'
        self.dependencies = [id]

    def set_inverse_type(self, id):
        self.type = 'Braid Inverse Image'
        self.conj = 'None'
        self.dependencies = [id]

    def set_conj_type(self,id,conj):
        self.type = 'Conjugate'
        self.conj = conj
        self.dependencies = [id]

    def set_prod_type(self,id1,id2):
        self.type = 'Product'
        self.conj = 'None'
        self.dependencies = [id1,id2]

    def print_element(self):
        if self.type == 'Not Set':
            type_data = 'WARNING: element has no type'
        elif self.type == 'Added':
            type_data = 'added to cone as a seed'
        elif self.type == 'Braid Image':
            type_data = 'braid image of ' + str(self.dependencies[0])
        elif self.type == 'Braid Inverse Image':
            type_data = 'inverse braid image of ' + str(self.dependencies[0])
        elif self.type == 'Conjugate':
            type_data = 'conjugate of ' + str(self.dependencies[0]) + ' by '+ str(self.conj)
        elif self.type == 'Product':
            type_data = 'product of ' + str(self.dependencies[0]) + ' and '+ str(self.dependencies[1])
        print('    ' + str(self.id) + ' ' + str(self.element) + ' ' + type_data)

class PositiveCone:

    def __init__(self,braid,ball_radius,braid_radius,conj_radius,prod_radius,order,track_extra_elements,add_extra_products):
        self.braid=braid
        self.ball_radius = ball_radius
        self.braid_radius = braid_radius
        self.conj_radius = conj_radius
        self.prod_radius = prod_radius
        self.order = order
        self.elements = []
        self.track_extra = track_extra_elements
        self.add_extra_products = add_extra_products
        self.extra = []
        self.prod_elements = set()
        self.total_element_set = set()
        self.num_elements = 0
        self.active_braid = []
        self.active_conj = []
        self.active_cyc = []
        self.active_prod = []
        self.begin_prod = {}
        self.end_prod = {}
        self.active_begin_prod = {}
        self.active_end_prod = {}
        G = braid.get_group_gens()
        for gen in G:
            self.begin_prod[str(gen)]=[]
            self.begin_prod[str(gen**-1)]=[]
            self.end_prod[str(gen)]=[]
            self.end_prod[str(gen**-1)]=[]
            self.active_begin_prod[str(gen)]=[]
            self.active_begin_prod[str(gen**-1)]=[]
            self.active_end_prod[str(gen)]=[]
            self.active_end_prod[str(gen**-1)]=[]
        self.contradiction_element = -1
        self.contradiction_inverse = -1
        self.contradiction = False

    def copy(self):
        new_cone=PositiveCone(self.braid,self.ball_radius,self.braid_radius,self.conj_radius,self.prod_radius,self.order,self.track_extra, self.add_extra_products)
        new_cone.elements = self.elements.copy()
        new_cone.extra = self.extra.copy()
        new_cone.prod_elements = self.prod_elements.copy()
        G = self.braid.get_group_gens()
        for gen in G:
            new_cone.begin_prod[str(gen)] = self.begin_prod[str(gen)].copy()
            new_cone.begin_prod[str(gen**-1)] = self.begin_prod[str(gen**-1)].copy()
            new_cone.end_prod[str(gen)] = self.end_prod[str(gen)].copy()
            new_cone.end_prod[str(gen**-1)] = self.end_prod[str(gen**-1)].copy()
        new_cone.total_element_set = self.total_element_set.copy()
        new_cone.contradiction = self.contradiction
        new_cone.contradiction_element = self.contradiction_element
        new_cone.contradiction_inverse = self.contradiction_inverse
        new_cone.num_elements = self.num_elements
        return new_cone

    def get_element_set(self):
        return self.total_element_set
    
    def get_element_with_id(self,id):
        for el in self.elements:
            if el.id==id:
                return el
        for el in self.extra:
            if el.id==id:
                return el

 #   def proof_info(self):
  #      proof_tuple=[]
  #      if self.contradiction:
   #         #self.print_cone()
   #         cont_id=self.contradiction_element
    #        dep_list=self.total_dependencies_id_list(cont_id)
     #       proof_tuple.append([cont_id,dep_list])
     #       cont_inv_id=self.contradiction_inverse
     #       print(cont_inv_id)
     #       dep_list_inv=self.total_dependencies_id_list(cont_inv_id)
     #       proof_tuple.append([cont_inv_id,dep_list_inv])
     #       return str(proof_tuple)
     #   else:
     #       return "no contradiction"

    def proof_info(self):
        proof_tuple=[]
        if self.contradiction:
            cont_id=self.contradiction_element
            #print(str(self.get_element_with_id(cont_id).element)+ '=' + self.get_equation(cont_id))
            #dep_list=self.total_dependencies_id_list(cont_id)
            proof_tuple.append(str(self.get_element_with_id(cont_id).element)+ '=' + self.get_equation(cont_id))
            cont_inv_id=self.contradiction_inverse
            #print(cont_inv_id)
            #dep_list_inv=self.total_dependencies_id_list(cont_inv_id)
            proof_tuple.append(str(self.get_element_with_id(cont_inv_id).element)+ '=' + self.get_equation(cont_inv_id))
            #proof_tuple.append([cont_inv_id,dep_list_inv])
            return str(proof_tuple)
        else:
            return "no contradiction"

    def get_equation(self,id):
        current_elt=self.get_element_with_id(id)
        elt_type=current_elt.type
        if elt_type=="Added":
            return str(current_elt.element)
        elif elt_type=='Product':
            return str(self.get_equation(current_elt.dependencies[0])) + ' * '+ str(self.get_equation(current_elt.dependencies[1]))
        elif elt_type == 'Braid Image':
            return  'b(' + str(self.get_equation(current_elt.dependencies[0]))+')'
        elif elt_type == 'Braid Inverse Image':
            return  'b^{-1}(' + str(self.get_equation(current_elt.dependencies[0]))+')'
        elif elt_type == 'Conjugate':
            return 'conj(['+ str(self.get_equation(current_elt.dependencies[0])) + '] by '+str(current_elt.conj)+')'
        #conj(b,by a)=aba^-1


    def total_dependencies_id_list(self, id):
        D_final=[id]
        D_active=self.get_element_with_id(id).dependencies
        D_interim=[]
        while len(D_active)>0:
            D_final=D_final+D_active
            #print(D_active)
            for x in D_active:
               D_interim=D_interim+self.get_element_with_id(x).dependencies
            D_active=D_interim
            D_interim=[]
        D_final.sort()
        return D_final

    def size(self):
        return self.num_elements
    
    def has_element(self,x):
        return x in self.total_element_set

    def saturate(self,element,Print):
        global nodeUID
        if self.size()>0:
            nodeUID+=1

        b = self.braid
        f=b.action(optimize=True)
        f_inv=b.inverse_action(optimize=True)
        G=b.get_group_gens()

        self.active_braid = []
        self.active_conj = []
        self.active_cyc = []
        self.active_prod = []
        for gen in G:
            self.active_begin_prod[str(gen)]=[]
            self.active_begin_prod[str(gen**-1)]=[]
            self.active_end_prod[str(gen)]=[]
            self.active_end_prod[str(gen**-1)]=[]

        added_elt = ConeElement(element)
        added_elt.set_added_type()
        was_added = self.add_element(added_elt)
        if was_added:
            if Print:
                print('Adding ' + str(element))
        else:
            if Print:
                print('Element ' + str(element) + ' already in cone.')
            return True
        if self.contradiction:
            if Print:
                print('    Contradiction, ' + str(element) + ' in both cone and inverse cone!')
            return False

        A_begin = {}
        A_end = {}
        while len(self.active_braid) > 0 or len(self.active_conj) > 0 or len(self.active_cyc) > 0 or len(self.active_prod) > 0:
            A_braid = self.active_braid.copy()
            A_conj = self.active_conj.copy()
            A_cyc = self.active_cyc.copy()
            A_prod = self.active_prod.copy()
            for gen in G:
                A_begin[str(gen)] = self.active_begin_prod[str(gen)].copy()
                A_begin[str(gen**-1)] = self.active_begin_prod[str(gen**-1)].copy()
                A_end[str(gen)] = self.active_end_prod[str(gen)].copy()
                A_end[str(gen**-1)] = self.active_end_prod[str(gen**-1)].copy()
            self.active_braid = []
            self.active_conj = []
            self.active_cyc = []
            self.active_prod = []
            for gen in G:
                self.active_begin_prod[str(gen)]=[]
                self.active_begin_prod[str(gen**-1)]=[]
                self.active_end_prod[str(gen)]=[]
                self.active_end_prod[str(gen**-1)]=[]

            for a_elt in A_braid:
                y_elt = a_elt                
                i = 0
                was_added = True                
                while i < self.order and was_added:
                    y = y_elt.element
                    z=f(y)
                    z_elt = ConeElement(z)
#                    print(str(y)+ ' ' + str(y_elt.id))
                    z_elt.set_image_type(y_elt.id)
                    was_added = self.add_element(z_elt)
                    if self.contradiction:
                        if Print:
                            print('    Contradiction, ' + str(z) + ' in both cone and inverse cone!')
                        return False
                    y_elt = z_elt
                    i = i + 1

                y_elt = a_elt
                i = 1
                was_added = True                
                while i <self.order and was_added:
                    y = y_elt.element
                    z=f_inv(y)
                    z_elt = ConeElement(z)
 #                   print(str(y)+ ' ' + str(y_elt.id))
                    z_elt.set_inverse_type(y_elt.id)
                    was_added = self.add_element(z_elt)
                    if self.contradiction:
                        if Print:
                            print('    Contradiction, ' + str(z) + ' in both cone and inverse cone!')
                        return False
                    y_elt = z_elt
                    i = i + 1
                
            for a_elt in A_conj:
                a = a_elt.element
                for g in G:
                    z=g*a*g**-1
                    z_elt = ConeElement(z)
                    z_elt.set_conj_type(a_elt.id,str(g))
                    was_added = self.add_element(z_elt)
                    if self.contradiction:
                        if Print:
                            print('    Contradiction, ' + str(z) + ' in both cone and inverse cone!')
                        return False

                    z=g**-1*a*g
                    z_elt = ConeElement(z)
                    z_elt.set_conj_type(a_elt.id,str(g**-1))
                    was_added = self.add_element(z_elt)
                    if self.contradiction:
                        if Print:
                            print('    Contradiction, ' + str(z) + ' in both cone and inverse cone!')
                        return False

            for a_elt in A_cyc:
                a = a_elt.element
                g = a.syllables()[0][0]
                s = -1*sign(a.syllables()[0][1])
                z = g**s*a*g**(-s)
                z_elt = ConeElement(z)
                z_elt.set_conj_type(a_elt.id,str(g**s))
                was_added = self.add_element(z_elt,False,True)
                if self.contradiction:
                    if Print:
                        print('    Contradiction, ' + str(z) + ' in both cone and inverse cone!')
                    return False

            for a_elt in A_prod:
                a = a_elt.element
                prod_elts = self.prod_elements.copy()
                for g_elt in prod_elts:
                    g = g_elt.element
                    z=a*g
                    z_elt = ConeElement(z)
                    z_elt.set_prod_type(a_elt.id,g_elt.id)
                    was_added = self.add_element(z_elt)
                    if self.contradiction:
                        if Print:
                            print('    Contradiction, ' + str(z) + ' in both cone and inverse cone!')
                        return False

                    z=g*a
                    z_elt = ConeElement(z)
                    z_elt.set_prod_type(g_elt.id,a_elt.id)
                    was_added = self.add_element(z_elt)
                    if self.contradiction:
                        if Print:
                            print('    Contradiction, ' + str(z) + ' in both cone and inverse cone!')
                        return False
            for gen in G:
                for x_elt in self.begin_prod[str(gen)]:
                    x = x_elt.element
                    for y_elt in A_end[str(gen**-1)]:
                        y = y_elt.element
                        z=y*x
                        too_long = word_length.word_length(z) >= word_length.word_length(y)
                        z_elt = ConeElement(z)
                        z_elt.set_prod_type(y_elt.id,x_elt.id)
                        was_added = self.add_element(z_elt, too_long)
                        if self.contradiction:
                            if Print:
                                print('    Contradiction, ' + str(z) + ' in both cone and inverse cone!')
                            return False

                for x_elt in self.end_prod[str(gen)]:
                    x = x_elt.element
                    for y_elt in A_begin[str(gen**-1)]:
                        y = y_elt.element
                        z=x*y
                        too_long = word_length.word_length(z) >= word_length.word_length(y)
                        z_elt = ConeElement(z)
                        z_elt.set_prod_type(x_elt.id,y_elt.id)
                        was_added = self.add_element(z_elt, too_long)
                        if self.contradiction:
                            if Print:
                                print('    Contradiction, ' + str(z) + ' in both cone and inverse cone!')
                            return False
            
#            print('    Cone has ' + str(self.size()) + ' elements.')

        if Print:
            print('    No contradictions. Cone has '+str(self.size())+' elements.')
        return True

    def add_element(self,element:ConeElement,special = False,cyc=False):
        global extra_checks
        cone_elts = self.get_element_set()
        add_type = element.type
        if add_type == 'Not Set':
            k = 0
        elif add_type == 'Added':
            k = self.ball_radius
        elif add_type == 'Braid Image' or add_type == 'Braid Inverse Image':
            k = self.braid_radius
        elif add_type == 'Conjugate':
            k = self.conj_radius
        elif add_type == 'Product':
            k = self.prod_radius
        z=element.element
#        print(str(word_length.word_length(z)))
        if word_length.word_length(z) <= k:
            if z not in cone_elts:
                element.set_id(self.num_elements)
                self.num_elements = self.num_elements + 1
                self.elements.append(element)
                #element.print_element()
                self.total_element_set.add(z)
                self.active_braid.append(element)
                #print('        Element added of braid list.')
                self.active_conj.append(element)
                #print('        Element added of conj list.')
                self.active_prod.append(element)
                #print('        Element added of prod list.')
                if add_type != 'Product':
                    self.prod_elements.add(element)
                g = z.syllables()[0][0]
                s = sign(z.syllables()[0][1])
                self.begin_prod[str(g**s)].append(element)
                l = len(z.syllables())
                g = z.syllables()[l-1][0]
                s = sign(z.syllables()[l-1][1])
                self.end_prod[str(g**s)].append(element)
                self.check_contradiction(element)
                return True
        else:
            if self.track_extra:
                if z not in cone_elts:
                    element.set_id(self.num_elements)
                    self.num_elements = self.num_elements + 1
                    self.extra.append(element)
                    #element.print_element()
                    self.total_element_set.add(z)
                    if self.add_extra_products:
                        g1 = z.syllables()[0][0]
                        s1 = sign(z.syllables()[0][1])
                        l = len(z.syllables())
                        g2 = z.syllables()[l-1][0]
                        s2 = sign(z.syllables()[l-1][1])
                    if add_type == 'Braid Image' or add_type == 'Braid Inverse Image' or cyc:
                        self.active_cyc.append(element)
                    #print('        Element added of cyc list.')
                    if not special and self.add_extra_products:
                        g = z.syllables()[0][0]
                        s = sign(z.syllables()[0][1])
                        self.active_begin_prod[str(g**s)].append(element)
                        l = len(z.syllables())
                        g = z.syllables()[l-1][0]
                        s = sign(z.syllables()[l-1][1])
                        self.active_end_prod[str(g**s)].append(element)
                    self.check_contradiction(element)
                    return True
        extra_checks = extra_checks + 1
        return False

    def check_contradiction(self,element:ConeElement):
        cone_elts = self.get_element_set()
        if element.element**-1 in cone_elts:
            self.contradiction_element = element.id
            inv = element.element**-1
            if inv in cone_elts:
                self.contradiction = True
                for elt in self.elements:
                    if elt.element == inv:
                        self.contradiction_inverse = elt.id
                        return
                if self.track_extra:
                    for elt in self.extra:
                        if elt.element == inv:
                            self.contradiction_inverse = elt.id
                            return
 
    def print_cone(self):
        print('Cone elements:')
        for elt in self.elements:
            elt.print_element()
        if self.track_extra:
            for elt in self.extra:
                elt.print_element()
        if self.contradiction:
            print('    Contradiction found: see elements ' + str(self.contradiction_element) + ' and ' + str(self.contradiction_inverse))
        else:
            print('    No contradictions in positive cone.')



'''
Enter a braid as an array of signed indices and a maximum word length k.
This function returns True if for every k-precone P, there is an obstruction to the braid preserving P.
This function returns False if there is at least one k-precone preserved by the braid.
'''

def preserve_order_obstruct(gens,k,kact=-1,kconj=-1,kprod=-1,order=1,track_extra_elements = False,add_extra_products= False,count=False,Print=False, tree=False, zero_exp_sum=True, diagnostic = False):
    global extra_checks
    extra_checks = 0
    if kact==-1:
        kact=k
    if kconj==-1:
        kconj=k
    if kprod==-1:
        kprod=k
    braid=Braid.Braid(gens)
    F = Braid.FreeGroup1(braid.strands)
    if Print:
        print('Input Braid: '+str(gens))
        f=braid.action(optimize=True)
        f_inv=braid.inverse_action(optimize=True)
        G=braid.get_group_gens()
        action_out = 'Optimized Braid Action: ['
        for i in range(braid.strands):
            action_out = action_out + 'beta(' + str(G[i]) + ')=' + str(f(G[i]))
            if i < braid.strands-1:
                action_out = action_out + ', '
        action_out = action_out + ']'
        print(action_out)

        action_out = 'Optimized Braid Inverse: ['
        for i in range(braid.strands):
            action_out = action_out + 'beta^-1(' + str(G[i]) + ')=' + str(f_inv(G[i]))
            if i < braid.strands-1:
                action_out = action_out + ', '
        action_out = action_out + ']'
        print(action_out)
    B = Ball.Ball(F,k)
    D = Ball.PairsinBall(B)
    pairs = []
    #print(gens)
    global nodeUID
    for i in range(len(D)):
        pairs.append(D[len(D)-i-1])

    P = PositiveCone(braid,k,kact,kconj,kprod,order,track_extra_elements,add_extra_products)
    if zero_exp_sum:
        start_elt = F([1])**-1*F([2])
    else:
        start_elt = F([1])
    starting_extra_checks = extra_checks
    easy_check = P.saturate(start_elt,Print)
    if diagnostic:
        print('    Saturation performed ' + str(extra_checks - starting_extra_checks) + ' extra checks. Total extra checks: ' + str(extra_checks))
#    P.print_cone()
    if easy_check or count:
        cancone , num_cones = CanCreateCone(P,pairs,Print,nodeUID,count,zero_exp_sum,diagnostic,0)
    else:
        return False
    nodeUID=0
    if tree:
        for key in tree_dict:
            print()
            print(key)
            for key2 in tree_dict[key]:
                print("    " + str(key2) + "\n         " + str(tree_dict[key][key2]))
            #f = open("tree " + str(gens), "a")
            #f.write(json.dumps(tree_dict, indent = 1))
            #f.close()
    tree_dict.clear()
    tree_dict[str(nodeUID)]={'parent':'start', 'name':'x1'}
    #tree_dict[str(nodeUID)]={'parent':'start','dvalue':'none','side':'none', 'name':'x1'}
    if count:
        return 2*num_cones
    else:
        return cancone

def CanCreateCone(P:PositiveCone,D,Print, itemID, count, zero_exp_sum, diagnostic, num_cones):
    global nodeUID
    thisUID=""
    thisUID=itemID

    global extra_checks

    i=0
    cone_elts = P.get_element_set()
    while i<len(D):
        if word_length.exponent_sum(D[i][0]) == 0 or not zero_exp_sum:
            if D[i][0] not in cone_elts and D[i][1] not in cone_elts:
                currentitem = D[i][0]
                Pnew = P.copy()
                starting_extra_checks = extra_checks
                contradict = Pnew.saturate(D[i][0],Print)
                if diagnostic:
                    print('    Saturation performed ' + str(extra_checks - starting_extra_checks) + ' extra checks. Total extra checks: ' + str(extra_checks))
                #cont_id=Pnew.contradiction_element
                #dep_list=Pnew.total_dependencies_id_list(cont_id)
                tree_dict[nodeUID] = {'parent':str(thisUID), 'name':str(currentitem), 'Proof info':Pnew.proof_info()}
                #tree_dict[nodeUID] = {'parent':str(thisUID),'dvalue':str(i),'side':str(0), 'name':str(currentitem), 'Proof info':Pnew.proof_info()}
                if contradict:
                    can_create, num_cones = CanCreateCone(Pnew,D,Print,nodeUID,count,zero_exp_sum, diagnostic, num_cones)
                    if not count and can_create:
                        return True, num_cones
                #else:
                #    Pnew.print_cone()
                # Don't need an if since this only runs when either Check(Pnew, b) or CanCreateCone(Pnew,D,b,k) is False
                currentitem= D[i][1]
                Pnew = P.copy()
                starting_extra_checks = extra_checks
                contradict = Pnew.saturate(D[i][1],Print)
                if diagnostic:
                    print('    Saturation performed ' + str(extra_checks - starting_extra_checks) + ' extra checks. Total extra checks: ' + str(extra_checks))
                tree_dict[nodeUID] = {'parent':str(thisUID), 'name':str(currentitem), 'Proof info':Pnew.proof_info()}
                #tree_dict[nodeUID] = {'parent':str(thisUID),'dvalue':str(i),'side':str(1), 'name':str(currentitem), 'Proof info':Pnew.proof_info()}
                if contradict:
                    return CanCreateCone(Pnew,D,Print,nodeUID,count,zero_exp_sum, diagnostic, num_cones)
                else:
                #    Pnew.print_cone()
                    return False, num_cones
        i+=1
    if Print:
        if count:
            print('Found cone! That\'s ' + str(num_cones + 1)+ ' cones so far.')
        else:            
            print('Found cone with ' + str(P.size())+ ' elements!')
            #P.print_cone()
    return True, num_cones + 1

def check_cycle_condition(gens, Print=False):
    braid=Braid.Braid(gens)
    G=braid.get_group_gens()
    f=braid.action()
    if Print:
        print('Input Braid: '+str(gens))
        action_out = 'Braid Action: ['
        for i in range(braid.strands):
            action_out = action_out + 'beta(' + str(G[i]) + ')=' + str(f(G[i]))
            if i < braid.strands-1:
                action_out = action_out + ', '
        action_out = action_out + ']'
        print(action_out)
    N = braid.strands
    perm = braid.permutation()
    if Print:
        print('Premutation Type: '+str(perm))
    conj_words=[]
    for g in G:
        image = f(g)
        l = word_length.word_length(image)
        new_word = G[0]*G[0]**-1
        for u in range((l-1)/2):
            s = sign(image.syllables()[0][1])
            x = image.syllables()[0][0]
            new_word = new_word * x**s
            image = x**(-s) * image
        conj_words.append(new_word)
        if Print:
            print(str(g) +' is conjugated by ' + str(new_word))
    cycles = []
    indeces = list(range(1,N+1))
    while len(indeces)>0:
        new_cycle = set()
        i=indeces[0]

        j=i
        cycle_complete = False
        while(not cycle_complete):
            indeces.remove(j)
            new_cycle.add(j)
            j=perm(j)
            if i==j:
                cycle_complete = True
        cycles.append(new_cycle)
    satisfied = False
    for i in range(1,N+1):
        if perm(i)==i:
            if Print:
                print(str(G[i-1]) + ' fixed in homology.')
            g=G[i-1]
            cyc_condition=True
            cycle_pairs = []
            for C in cycles:
                clay_const = 0
                for j in C:
                    clay_const=clay_const + word_length.exponent_gen_sum(conj_words[j-1],g)
                cycle_pairs.append([clay_const,len(C)])
                if gcd(clay_const,len(C))!=1:
                    cyc_condition=False

            if cyc_condition:
                satisfied = True
                if Print:
                    print('    Cycle Pairs: ' + str(cycle_pairs) + ' - cycle condition satisfied for ' + str(G[i-1]))
            elif Print:
                print('    Cycle Pairs: ' + str(cycle_pairs) + ' - cycle condition not satisfied for ' + str(G[i-1]))
        elif Print:
            print(str(G[i-1]) + ' not fixed in homology.')
    return satisfied
