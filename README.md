# Lid Cavity Dataset

## Dataset

The dataset is the solution of

 $$\frac{\partial u}{\partial t}(t,x,y)+(u(t,x,y)\cdot \nabla) u(t,x,y)-\nu \Delta u(t.x,y)=-\nabla p(t,x,y) \quad x\in (-0.05,0.05), y\in (-0.05,0.05), t\in (0,10)$$

 $$\nabla \cdot u=0$$

 $$u(0,x,y)=(0,0) \quad x\in (-0.05,0.05), y\in (-0.05,0.05)$$

 $$u(0,x,-0.05)=(0,0) \quad x\in [-0.05,0.05]$$

 $$u(0,x,0.05)=(1,0) \quad x\in [-0.05,0.05]$$
 
 $$u(0,-0.05,y)=(0,0) \quad y\in [-0.05,0.05)$$
 
 $$u(0,0.05,y)=(0,0) \quad y\in [-0.05,0.05)$$
 
 $$p(0,x,y)=0$$
 
 $$u(t,x,y)=(0,0) \quad x\in (-0.05,0.05), y\in (-0.05,0.05), t\in (0,10)$$
 
 $$u(t,x,-0.05)=(0,0) \quad x\in [-0.05,0.05],t\in (0,10)$$
 
 $$u(t,x,0.05)=(1,0) \quad x\in [-0.05,0.05],t\in (0,10)$$
 
 $$u(t,-0.05,y)=(0,0) \quad y\in [-0.05,0.05),t\in (0,10)$$
 
 $$u(t,0.05,y)=(0,0) \quad y\in [-0.05,0.05), t\in (0,10)$$

As we are in 2D this system has an unique weak solution (see Ladyzhenskaya (1958, 1959), Lions and Prodi (1959)).
For more details on the dateset , see [this link](https://www.openfoam.com/documentation/tutorial-guide/2-incompressible-flow/2.1-lid-driven-cavity-flow).

Note that $u$ is discontinous on $(-0.05,0.05)$, $(0.05,0.05)$. This is not a problem as the dataset is created using the finite volume method, using icoFoam.

$\nu$ varies from $0.001$ to $0.000001$, as such the Reynolds number varies from $100$ to $10000.$

We assume that $u$ and $p$ belong to the space of functions 
$$L^{2}([-0.05,0.05],0,10)=\{u:[0,10]\times [-0.05,0.05]\times [-0.05,0.05]\rightarrow \mathbb{R}^{k} | \int_{0}^{10} ||u(t)||_{1}^{2}dt=\int_{0}^{10}\left(\int_{[-0.05,0.05]}\sum_{i=1}^{k}|u(t,x,y)\cdot e_{i}|dxdy\right)^{2}dt<+\infty \}.$$

So the relative error that is used for measures the model performance is:
$$\frac{\int_{0}^{10}\left(\int_{[-0.05,0.05]}\sum_{i=1}^{k}|(u(t,x,y)-\hat{u}(t,x,y))\cdot e_{i}|dxdy\right)^{2}dt}{\int_{0}^{10}\left(\int_{[-0.05,0.05]}\sum_{i=1}^{k}|u(t,x,y)\cdot e_{i}|dxdy\right)^{2}dt}$$

The integrals are calculated with the composite trapezoidal formula.



## Package installation guide
First install OpenFoam 2312. Them from this directory do the following:

```sh
pip install PyFoam numpy Ofpp tqdm
cd data
openfoam2312
python generate_data.py
cd ..
pip install .
```

## Usage example
```sh
from lidcavity import LidCavity
data=LidCavity(batch_size=10)
train_loader=data.train_loader ##Gives a pytorch dataloader
```
