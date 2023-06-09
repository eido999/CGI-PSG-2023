import time
from CombineModel_jt import CombineModel
import cv2
import numpy as np
import os
import glob
from tqdm import tqdm
import jittor as jt

jt.flags.use_cuda = 1

#models for face/eye1/eye2/nose/mouth
combine_model = CombineModel()

print('start')
fileRoot = './test'
saveroot = './save/'
images_path = sorted(glob.glob(fileRoot+r"/*"))

params = [
    [0.80, 0.63, 1.0, 0.88, 0.93, 1],
    [1.0, 1.0, 1.0, 1.0, 0.84, 0],
    [0.1, 0.39, 0.58, 0.63, 0.49, 1],
    [1.0, 1.0, 1.0, 1.0, 1.0, 1],
    [0.78, 1.0, 1.0, 1.0, 0.79, 1],
    [0.78, 1.0, 1.0, 1.0, 0.79, 1]
]

i = 0
s = 0
for x,fileName in enumerate(images_path):
    print('Input file:',fileName)
    mat_img = cv2.imread(fileName)
    mat_img = cv2.resize(mat_img, (512, 512), interpolation=cv2.INTER_CUBIC)
    mat_img = cv2.cvtColor(mat_img, cv2.COLOR_RGB2BGR)
    sketch = (mat_img).astype(np.uint8)
    combine_model.sex = params[s][5]
    #666
    combine_model.part_weight['eye1'] = params[s][0]
    combine_model.part_weight['eye2'] = params[s][1]
    combine_model.part_weight['nose'] = params[s][2]
    combine_model.part_weight['mouth'] = params[s][3]
    combine_model.part_weight[''] = params[s][4]
    print(s)
    combine_model.predict_shadow(mat_img)
    
    output_file = 'ori'+ fileName[7:-4] +'.jpg'
    print('Output file:',output_file)
    cv2.imwrite(os.path.join(saveroot , output_file),cv2.cvtColor(combine_model.generated, cv2.COLOR_BGR2RGB))
    i = i + 1
    s = i%6
    jt.gc()
