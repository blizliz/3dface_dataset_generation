import os
import shutil

import numpy as np
import trimesh
import pyrender
import matplotlib.pyplot as plt

from pyrender import Node

MIN_DEGREES = -0.6
MAX_DEGREES = 0.6
STEP_DEGREES = 0.1

save_path = 'dataset'
if not os.path.exists(save_path):
    os.makedirs(save_path)
else:
    shutil.rmtree(save_path)
    os.makedirs(save_path)

face_trimesh = trimesh.load('./result.obj')
face_mesh = pyrender.Mesh.from_trimesh(face_trimesh)

inx = 0
for x in np.arange(MIN_DEGREES, MAX_DEGREES + STEP_DEGREES, STEP_DEGREES):
    for y in np.arange(MIN_DEGREES, MAX_DEGREES + STEP_DEGREES, STEP_DEGREES):
        inx += 1
        scene = pyrender.Scene()

        rotate_vec = np.array([x, y, 0.0, 1])
        rotate_vec_norm = rotate_vec / np.linalg.norm(rotate_vec)

        face_node = Node(mesh=face_mesh, translation=np.array([0, 0, -2.5]), rotation=rotate_vec_norm)
        scene.add_node(face_node)

        camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
        camera_pose = np.array([
            [1.0,  0.0, 0.0, 0.0],
            [0.0,  1.0, 0.0, 0.0],
            [0.0,  0.0, 1.0, 0.0],
            [0.0,  0.0, 0.0, 1.0],
         ])
        scene.add(camera, pose=camera_pose)
        light = pyrender.light.DirectionalLight(color=np.ones(3), intensity=5.0)
        scene.add(light, pose=camera_pose)
        r = pyrender.OffscreenRenderer(600, 600, point_size=1)
        color, depth = r.render(scene)
        plt.figure()
        plt.axis('off')
        plt.imshow(color, cmap=plt.cm.gray_r)
        file_name = "{0}.jpg".format(inx)
        complete_name = os.path.join(save_path, file_name)
        plt.savefig(complete_name)
        plt.close()
