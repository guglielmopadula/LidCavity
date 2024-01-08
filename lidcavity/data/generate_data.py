import PyFoam
import numpy as np
from tqdm import trange
import Ofpp
from PyFoam.Execution.BasicRunner import BasicRunner
from PyFoam.Execution.ConvergenceRunner import ConvergenceRunner
from PyFoam.Execution.UtilityRunner import UtilityRunner
from PyFoam.LogAnalysis.BoundingLogAnalyzer import BoundingLogAnalyzer
from PyFoam.RunDictionary.SolutionFile import SolutionFile
from PyFoam.RunDictionary.SolutionDirectory import SolutionDirectory
from PyFoam.RunDictionary.ParsedParameterFile import ParsedParameterFile
from PyFoam.Basics.DataStructures import Field
from scipy.spatial import Delaunay
solver="icoFoam"
case="."
case_dir="./"
dire=SolutionDirectory(case)
dire.clearResults()
print(dire.initialDir())
sol=SolutionFile(dire.initialDir(),"U")
transport_properties_file = "constant/transportProperties"
maximum=1.
nr=10
time_directory = "0.1"
velocity_field_name = "U"
times=np.linspace(0,10,101)
times=np.delete(times,0)
times=np.round(times,1)
par=np.concatenate((np.linspace(1000,3000,300),np.linspace(3001,100000,300)))
mesh = Ofpp.FoamMesh('.')
U_vec=np.zeros((len(par),len(times),400,2))
p_vec=np.zeros((len(par),len(times),400))
for i in trange(len(par)):
    dire.clearResults()
    nu_value = 1/par[i]
    transport_properties = ParsedParameterFile(case_dir+transport_properties_file)
    transport_properties['nu'] = nu_value
    transport_properties.writeFile()
    # Run the solver
    runner = BasicRunner(argv=[solver], silent=True, logname="log.{}.txt".format(solver),)    
    runner.start()
    for j in range(len(times)):
        t=times[j]
        if t.is_integer():
            t_2=int(t)
        else:
            t_2=t
        U=Ofpp.parse_internal_field(str(t_2)+"/U")
        p=Ofpp.parse_internal_field(str(t_2)+"/p")
        U_vec[i,j,:,:]=U[:,:2]
        p_vec[i,j,:]=p


sol.purgeFile()
np.save("U.npy",U_vec)
np.save("p.npy",p_vec)
np.save("par.npy",par)
np.save("times.npy",times)


mesh = Ofpp.FoamMesh('.')
points=np.zeros((mesh.num_cell,3))
for i in range(mesh.num_cell):
    faces=mesh.cell_faces[i]
    cent=0
    v=set([])
    for face in faces:
        for j in mesh.faces[face]:
            v.add(j)

    v=np.array(list(v))
    points[i]=np.mean(mesh.points[v],axis=0)

points=points[:,:2]
np.save("points.npy",points)
dire.clearResults()

grid=np.zeros((len(par),U_vec.shape[1],points.shape[0],4))
grid[:,:,:,0]=np.tile(times.reshape((1,len(times),1)),(len(par),1,points.shape[0]))
grid[:,:,:,1:3]=np.tile(points.reshape((1,1,points.shape[0],2)),(len(par),U_vec.shape[1],1,1))
grid[:,:,:,3]=np.tile(par.reshape((len(par),1,1)),(1,U_vec.shape[1],points.shape[0]))
result=np.concatenate((U_vec,p_vec.reshape(p_vec.shape[0],p_vec.shape[1],p_vec.shape[2],1)),axis=-1)
np.save("grid.npy",grid)
np.save("result.npy",result)

tri=Delaunay(points)
triangles=tri.simplices
np.save("triangles.npy",triangles)
h_points=np.concatenate((np.ones(len(points)).reshape(-1,1),points),axis=1)
areas=np.abs(np.linalg.det(h_points[triangles])*1/2)
weights_triangles=areas*1/3
weights_triangles=np.tile(weights_triangles.reshape(-1,1),(1,3))
weights_triangles=weights_triangles.flatten()
weights_points=np.bincount(triangles.flatten(),weights=weights_triangles)
np.save("weights_space.npy",weights_points)

indexes=np.argsort(times)
edges=np.concatenate((np.arange(0,len(times)-1).reshape(-1,1),np.arange(1,len(times)).reshape(-1,1)),axis=1)
edges=indexes[edges]
weights_edges=np.tile(times[edges[:,1]]-times[edges[:,0]],(1,2))/2
weights_times=np.bincount(edges.flatten(),weights=weights_edges.flatten())
np.save("weights_times.npy",weights_times)


h=0.005
size=20

def fortran_ordering(i,j):
    return j*size+i

def inverse_fortran_ordering(k):
    return k%size,k//size


M_x=np.zeros((400,400))

M_y=np.zeros((400,400))

for k in range(400):
    i,j=inverse_fortran_ordering(k)
    if i==0:
        M_x[k,k]=-1/h
        M_x[k,fortran_ordering(i+1,j)]=1/h
    elif i==19:
            M_x[k,k]=1/h
            M_x[k,fortran_ordering(i-1,j)]=-1/h

    else:
        M_x[k,fortran_ordering(i-1,j)]=-1/(2*h)
        M_x[k,fortran_ordering(i+1,j)]=1/(2*h)

    if j==0:
        M_y[k,k]=-1/h
        M_y[k,fortran_ordering(i,j+1)]=1/h  
    elif j==19:
        M_y[k,k]=1/h
        M_y[k,fortran_ordering(i,j-1)]=-1/h
    else:
        M_y[k,fortran_ordering(i,j-1)]=-1/(2*h)
        M_y[k,fortran_ordering(i,j+1)]=1/(2*h)

np.save("diff_x.npy",M_x)
np.save("diff_y.npy",M_y)
