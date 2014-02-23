r"""
The Matroid Union takes matroids as arguments and returns their union.

Let Mi = (Si,Ii)
Matroid Union M = M1 v M2 v M3 v ... v Mk is defined as (S1 U S2 U S3 U ... U Sk,I1 v I2 v I3 v ... v Ik )
where I1 v I2 v I3 v ... v Ik = {i1 U i2 U i3 U ... U ik | ij \in Ij }

EXAMPLES::

	sage: M1 = matroids.Uniform(3,6)
	sage: M2 = matroids.Uniform(2,4)
	sage: M = MatroidUnion(M1,M2)
	sage: M.is_valid()
	True

	sage: N = MatroidUnion(M2,M1)
	sage: M == N
	True

	sage: P = MatroidUnion([M1,M2])
	sage: Q = MatroidUnion([M1,M2],M1)


"""
from matroid import Matroid
from itertools import combinations
import sage.matrix.matrix_space as matrix_space
from sage.matrix.constructor import Matrix
from sage.graphs.all import Graph, graphs
import sage.matrix.matrix
from sage.rings.all import ZZ, QQ, FiniteField, GF
import sage.matroids.matroid
import sage.matroids.basis_exchange_matroid
from minor_matroid import MinorMatroid
from dual_matroid import DualMatroid
from rank_matroid import RankMatroid
from circuit_closures_matroid import CircuitClosuresMatroid
from basis_matroid import BasisMatroid
from linear_matroid import LinearMatroid, RegularMatroid, BinaryMatroid, TernaryMatroid, QuaternaryMatroid
import sage.matroids.utilities
from networkx import NetworkXError


def MatroidUnion2(M0,M1): #Only the first argument can be a iterable

	#Checking if the arguments given are valid

	if not (isinstance(M0,Matroid) and isinstance(M1,Matroid)):
		raise ValueError("Arguments don't appear to be matroids")
	

	#Constructing matroid union from two matroids
	#rank(X) = max ( |Y| + rM2(X) ) where Y subset of X, and Y belongs to M0 \cap M1.dual()



	common_ground_set = M0.groundset()
	common_ground_set = common_ground_set.union(M1.groundset())

	def f(X):
		ground_set = common_ground_set.intersection(X)
		delSet = common_ground_set-ground_set

		def h(X):
			return M0.rank(set(X).intersection(M0.groundset()))

		#Extending matroid M0 to the union of groundsets
		I0 = RankMatroid(groundset=common_ground_set,rank_function=h)

		def g(X):
			return M1.rank(set(X).intersection(M1.groundset()))

		#Extending matroid M1 to the  union of groundsets
		I1 = RankMatroid(groundset=common_ground_set,rank_function=g)

		#Restricting matroid M0 to set X
		I0 = I0.delete(delSet)

		#Taking M1 dual and restricting to set X
		I1 = I1.dual()
		I1 = I1.delete(delSet)

		# rank(X) = max ( |Y| + rM2(X) ) where Y subset of X, and Y belongs to I0 \cap I1
		r1 = len(I0.intersection(I1))
		r2 = M1.rank(set(X).intersection(M1.groundset()))
		return r1+r2
	return RankMatroid(groundset=common_ground_set,rank_function=f)

def MatroidUnion(matroids=[],*args):

	if isinstance(matroids,set):
		matroids = list(matroids)
	
	if not isinstance(matroids,list):
		matroids = [matroids]

	matroids.extend(list(args))

	M0 = matroids[0]
	M1 = matroids[1]

	for i in range(len(matroids)-1):
		M1 = matroids[i+1]
		M0=MatroidUnion2(M0,M1)

	return M0




