from utils_zp import *

# ==============
set_cuda_devices('2,3,4,5')
# ==============

from llm_zp import QwenOmni
from _prompt import *
add_sys_path(__file__, 2)

from pandas_videoclip_iter import *


class Annotate:
    def __init__(self, video_dir, output_dir, num, device='auto'):
        self.videoclip_iter = PandasVideoClipIter(video_dir=video_dir)
        self.qwen_omni = QwenOmni(
            model_or_model_path='/home/zhipang/pretrained_models/Qwen2.5-Omni-7B', 
            mode='bf16', 
            input_device='cuda:1'
        )
        self.output_dir = path(output_dir)
        self.clip_num = num
        pass

    def start(self):
        cnt = 0
        pb = tqdm.tqdm(total=self.clip_num)
        for videoclip in iter(self.videoclip_iter):
            videoclip: VideoClipSample
            llm_res = self._process_clip(videoclip)
            self.save_res(videoclip, llm_res)

            cnt += 1
            pb.update(1)
            if cnt >= self.clip_num:
                break
            pass
    
    def save_res(self, videoclip:VideoClipSample, llm_res:List[str]):
        with open(self.output_dir / (videoclip.clipID+'.txt'), 'w')as f:
            for _res in llm_res:
                f.write(_res+'\n')
                f.write(gap_line(fillchar='-', total_len=20)+'\n')
            f.write(gap_line(fillchar='=')+'\n\n')

    def _process_clip(self, videoclip:VideoClipSample):
        conversation = [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": "You are Qwen, a virtual human developed by the Qwen Team, Alibaba Group, capable of perceiving auditory and visual inputs, as well as generating text and speech."}
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "video", "video": str(videoclip.video_path)},
                    {'type': 'text', 'text': DESC_PROMPT},
                ],
            },
        ]
        
        dense_desc:str = self.qwen_omni(conversation)[0]
        print(gap_line())
        print(dense_desc)
        print(gap_line())

        conversation = [
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": "You are Qwen, a virtual human developed by the Qwen Team, Alibaba Group, capable of perceiving auditory and visual inputs, as well as generating text and speech."}
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "video", "video": str(videoclip.video_path)},
                    {'type': 'text', 'text': CLS_AND_REASON_PROMPT.format(**{'ontology': ONTOLOGY, 'description': dense_desc})},
                ],
            },
        ]
        cls_and_reason:str = self.qwen_omni(conversation)[0]
        
        print(cls_and_reason)
        print(gap_line())
        # cls, reason = cls_and_reason.aplit('reason:', 1)
        # cls = cls.split('class:', 1)[1]
        # cls, reason = cls.strip(), reason.strip()

        return [dense_desc, cls_and_reason]



if __name__ == '__main__':
    Annotate(
        video_dir=VALID_VIDEO_DIR,
        output_dir='/home/zhipang/PhyDynamics/src/annotate/~output_sample',
        num=3,
        # device='balanced',
        # device='cpu',
        device='auto',
        # device='cuda:0'
    ).start()