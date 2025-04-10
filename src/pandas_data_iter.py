from utils_zp import *

import ast
import csv

csv.field_size_limit(sys.maxsize)


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
class PandasSample:
    videoID:str
    sampleID:str
    url:str
    timestart:str
    timeend:str
    caption:str
    matching_score:float
    desirable_filtering:str
    shot_boundary_detection:list

    @classmethod
    def timestamp_to_float(cls, timestamp:str):
        h, m, s = map(float, timestamp.split(':'))
        return h*3600+m*60+s


class PandasDataIter:
    def __init__(self, csv_file):
        # self.csv_file = path(csv_file)
        self.file_iter = FileIO.csv_load(path(csv_file), iteration=True)

    def __iter__(self):
        def inner():
            next(self.file_iter)
            for line in self.file_iter:
                videoID, url, timestamp, caption, matching_score, desirable_filtering, shot_boundary_detection = line
                timestamp, caption, matching_score, desirable_filtering, shot_boundary_detection = map(
                    ast.literal_eval, 
                    [timestamp, caption, matching_score, desirable_filtering, shot_boundary_detection]
                )
                for p, (timestamp_, caption_, matching_score_, desirable_filtering_, shot_boundary_detection_) in enumerate(zip(
                    timestamp, caption, matching_score, desirable_filtering, shot_boundary_detection
                )):
                    yield PandasSample(
                        videoID=videoID,
                        sampleID=f'{videoID}_{p}',
                        url=url,
                        timestart=timestamp_[0],
                        timeend=timestamp_[1],
                        caption=caption_,
                        matching_score=float(matching_score_),
                        desirable_filtering=desirable_filtering_,
                        shot_boundary_detection=shot_boundary_detection_,
                    )
        return inner()



TRAIN70M_CSV = '/home/zhipang/PhyDynamics/data/Pandas-70M/panda70m_training_full.csv'
TRAIN10M_CSV = '/home/zhipang/PhyDynamics/data/Pandas-70M/panda70m_training_10m.csv'
TRAIN2M_CSV = '/home/zhipang/PhyDynamics/data/Pandas-70M/panda70m_training_2m.csv'
VALID_CSV = '/home/zhipang/PhyDynamics/data/Pandas-70M/panda70m_validation_with_additional_annotation.csv'
TEST_CSV = '/home/zhipang/PhyDynamics/data/Pandas-70M/panda70m_testing_with_additional_annotation.csv'


if __name__ == '__main__':
    for a in PandasDataIter(TEST_CSV):
        print(a)
        input()