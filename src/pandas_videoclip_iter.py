from utils_zp import *

import ast


'''
videoID, 
-2yHu5qgTzM

url, 
https://www.youtube.com/watch?v=-2yHu5qgTzM

timestamp, 
"[['0:01:20.880', '0:01:23.983'], ['0:02:31.151', '0:02:34.320'], ['0:03:28.841', '0:03:33.680']]"

caption, 
"['A neuron in a black background.', 'A woman is standing on a black background and talking to the camera.', 'There is a whiteboard with equations on it, and a man and a woman are standing in front of it.']"

matching_score, 
"[0.451416015625, 0.4990234375, 0.434814453125]"

desirable_filtering, 
"['1_still_foreground_image', 'desirable', 'desirable']"

shot_boundary_detection
"[[['0:00:00.000', '0:00:03.069']], [['0:00:00.000', '0:00:03.169']], [['0:00:00.000', '0:00:02.702'], ['0:00:02.736', '0:00:04.838']]]"
'''


@dataclass
class VideoClipSample:
    # videoID:str
    clipID:str
    url:str
    # timestart:str
    # timeend:str
    caption:str
    matching_score:float
    desirable_filtering:str
    shot_boundary_detection:list
    video_path:path

    @classmethod
    def timestamp_to_float(cls, timestamp:str):
        h, m, s = map(float, timestamp.split(':'))
        return h*3600+m*60+s


class PandasVideoClipIter:
    def __init__(self, video_dir):
        # self.csv_file = path(csv_file)
        self.video_dir = path(video_dir)

    def __iter__(self):
        def inner():
            assert self.video_dir.exists()
            for son_dirs in listdir_full_path(self.video_dir):
                for _file in listdir_full_path(son_dirs):
                    if _file.suffix != '.mp4':
                        continue
                    _info = auto_load(
                        _file.parent / (_file.stem+'.json')
                    )
                    _id = _info['url'].split('v=')[-1]
                    _id += _info['key'][-1]
                    yield VideoClipSample(
                        clipID=_id,
                        url=_info['url'],
                        caption=_info['caption'],
                        matching_score=_info['matching_score'],
                        desirable_filtering=_info['desirable_filtering'],
                        shot_boundary_detection=ast.literal_eval(_info['shot_boundary_detection']),
                        video_path=_file,
                    )
        return inner()


TEST_VIDEO_DIR = '/home/zhipang/PhyDynamics/data/Pandas-70M/testset'
VALID_VIDEO_DIR = '/home/zhipang/PhyDynamics/data/Pandas-70M/validationset'
TRAIN2M_FILTER147K_VIDEO_DIR = '/home/zhipang/PhyDynamics/data/Pandas-70M/train2m_filter_sy'


if __name__ == '__main__':
    for a in PandasVideoClipIter(TEST_VIDEO_DIR):
        print(a)
        input()