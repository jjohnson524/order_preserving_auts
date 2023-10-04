# order_preserving_braids Read Me file

copyright info

This project is companion to the research manuscript titled Algorithms for Order-Preservng Braids for  which can be found on ARXIV soon. All technical terminolgy is defined in the manuscript.

The authors of this project are Jonathan Johnson, Nancy Scherich and Hannah Turner.

To begin, download the following files from the github repoistory
Ball.py
Braid.py
preserve_order.py
run_preserve_order.py
word_length.py


All files need to be run through SageMath. 
To get SageMath on your device, go to [this link](https://doc.sagemath.org/html/en/installation/index.html) and install SageMath.



### Group element notation:

#### Braids: 
- Braids are stored as a list of integers describing the braid word in terms of the standard Artin generators. For example sigma\_1.sigma\_2^{-1}.sigma\_2^{-1}.sigma_5 is written as \[1,-2,-2,5\]. 

#### Free group elements:
- Generators of the of the free group are denoted x1, x2, x3 ... and their inverses are denoted by xi^{-1}.



## Instructions to run a single computation for a braid.

At the start of your SageMath file, import the preserve_order.py file with the following code:

sage: import("preserve\_order.py")

This will automatically import Ball.py, Braid.py, and word\_length.py.



#### The function preserve\_order\_obstruct. 

input: a braid *b* and an integer *k* 

output: 
- The function returns "True" if there exists a *k*-precone preserved by *b*. This is inconclusive as *b* could be order preserving or not.

- The function returns "False" if there does not exist a *k*-precone preserved by *b*. This conclusively tells you that *b* is not order preserving.

Optional parameters:

- Setting "track_extra_elements = True" will improve the efficiency of the program by looking for contradictions from outside of the *k*-precone. This setting can lead to finding condradictions at smaller values of *k*.

- Setting "tree=True", if the function returns False, will print enough information to construct a proof that *b* does not preserve an order. The information printed is a binary tree where each node of the tree has the following information: unique id of the node, parent node  unique id, element name that was added to the precone at that stage of the tree, and proof information at that node. If there is a contradiction at the node, the proof info will show two elements in the precone that are inverses of each other, and equations describing how those two elements were added to the cone. If there is no contradiction at that node, the proof info will say "no contradiction".

- Setting count=True will override other outputs and retun a number. 0 means false




#### Using the function preserve\_order\_obstruct.

Ordering the inputs: 

&nbsp;&nbsp;&nbsp; preserve\_order\_obstruct(braid,k)-- not using optional parameters

&nbsp;&nbsp;&nbsp; preserve\_order\_obstruct(braid,k,trac\k_extra\_elements = True, tree=True)-- using optional parameters

Example usage:

    sage: preserve\_order\_obstruct([-2,3],2)
    output: True   
        
    sage:    preserve\_order\_obstruct(\[1,-2,-2,-2\],4,track\_extra\_elements =True, tree=True)
    output: 
            0
                parent
                    start
                name
                    x1

            1
                parent
                     0
                name
                     x2^-1*x3
                Proof info
                    ['x3^-1*x2^-1*x1*x2=b(conj([x2^-1*x3] by x3^-1))', 'x2^-1*x1^-1*x2*x3=x2^-1*x3 * conj([x1^-1*x2] by x3^-1)']

            2
                parent
                    0
                name
                    x3^-1*x2
                Proof info
                    ['x2^-2*x1*x2*x3*x2^-1=conj([b(conj([conj([x1^-1*x2] by x3) * b(x3^-1*x2)] by x2))] by x2)', 'x2*x3^-1*x2^-1*x1^-1*x2^2=conj([x3^-1*x2] by x2) * conj([x1^-1*x2] by x2^-1)']
            False


    sage: preserve\_order\_obstruct([1,-2,-2,-2],4, tree=True)
    output: 
            0
                parent
                      start
                name
                       x1

            1
                parent
                      0
                name
                    x2^-1*x3
                Proof info
                    ['x3^-1*x2^-1*x1*x2=b(conj([x2^-1*x3] by x3^-1))', 'x2^-1*x1^-1*x2*x3=conj([x1^-1*x2] by x2^-1) * x2^-1*x3']

            2
                parent
                    0
                name
                    x3^-1*x2
                Proof info
                   no contradiction

            3
                parent
                    2
                name
                     x1^-1*x3
                Proof info
                    no contradiction

            4
                parent
                     3
                name
                     x2^-1*x3^-1*x2*x3
                Proof info
                     no contradiction

            5
                parent
                     4
                name
                     x2^-1*x1^-1*x3^2
                Proof info
                     no contradiction

            6
                parent
                     5
                name
                     x2^-1*x3*x1^-1*x3
                Proof info
                     no contradiction

            7
                parent
                     6
                name
                     x1^-1*x3^-1*x1*x2
                Proof info
                     no contradiction

            8
                parent
                     7
               name
                     x1^-1*x3^-1*x1*x3
                Proof info
                     no contradiction

            9
                parent
                     8
                name
                    x1^-1*x2^-1*x1*x2
             Proof info
                     no contradiction

            10
                parent
                     9
                name
                     x1^-1*x2^-1*x1*x3
                Proof info
                       no contradiction
            True



## II. Instructions to run several computation for a single braid with increasing k values.

At the start of your SageMath file, import the run_preserve_order.py file with the following code

&nbsp;&nbsp;&nbsp; import("run\_preserv\e_order.py")

This will automatically import Ball.py, Braid.py, preserve\_order.py, and word\_length.py.

run_preserve_order_obstruct(gens,max_k,min_k=2,order=1,track_extra_elements = False,add\_extra\_products=False,count=False,Print=False, tree=False,zero_esp_sum=True,time=False):

####  The function run_preserve_order_obstruct.

input: 
- a braid *b* and and two integers *k*=maximum and *l*=minimun 

output: 
- This function will iteratively call the preserve\_order\_obstruct function for increasing *k*-values starting at the minimum *k*-value (input of *l*), and stopping at the maximum *k*-value (inputed of *k*). This function creates a txt file named b_k_l.txt where it will display the output.

- With no optional parameters, for each *k*-value in the iterative range, this function will display on a new line

 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; k=current k-value; found pre-cone: True or False

When the program returns True, for a fixed i between *l* and *k*, there is at least one conjugate invariant i-precone of the free group preserved by the braid. When the program returns False, for a given i, there is no possible conjugate invariant i-precone of the free group preserved by the braid.

Optional parameters:
- Setting "track\_extra\_elements = True" will improve the efficiency of the program by looking for contradictions from outside of the k-precone. This setting can lead to finding condradictions at smaller values of *k*.

- Setting "tree=True", if the function returns False, will print enough information to construct a proof that b does not preserve an order. The information printed is a binary tree where each node of the tree has the following information: unique id of the node, parent node  unique id, element name that was added to the precone at that stage of the tree, and proof information at that node. If there is a contradiction at the node, the proof info will show two elements in the precone that are inverses of each other, and equations describing how those two elements were added to the cone. If there is no contradiction at that node, the proof info will say "no contradiction".


