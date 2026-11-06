This is a python 3d renderer I made from scratch for my school projects in year 9

Deps:
* numpy
* pygame

Features:
- import any OBJ file
- mouse control
- Hitboxes
- movement, sliding, crouching and clipping prevention when standing up in small spaces
- text based scene editor
  ```python
  -b 0 0 0               # set background colour
  -o cube.obj 1 0 1      # create cube at at 1,0,1 from cube.obj
  -o sphere.obj 1 0 0    # create sphere at at 1,0,1 from sphere.obj
  -c 0 -3 0 100 2 100    # make collision box 1
  -c 0 0 0 2 2 2         # make collision box 2
  ```

Here are a few screenshots

<img width="500" alt="image" src="https://github.com/user-attachments/assets/64ce857c-57fe-4c62-8f56-da32f6ee70cb" />


<img width="500" alt="image" src="https://github.com/user-attachments/assets/3343ed4e-05eb-4ecb-b053-3676b609ab64" />
