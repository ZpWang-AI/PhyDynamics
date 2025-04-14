from pandas_data_iter import *
from llm_api import *


class FilterResult:
    def __init__(self, filter_res_file):
        self.filter_res_file = path(filter_res_file)
        if not self.filter_res_file.exists():
            print(f'filter_res_file "{self.filter_res_file.name}" not exists, auto create a new one')
            make_path(file_path=self.filter_res_file)
    
    def __iter__(self):
        def inner():
            with open(self.filter_res_file, 'r')as f:
                while 1:
                    line = f.readline().strip()
                    if not line:
                        break
                    sampleID, filter_res = line.split(' ', 1)
                    filter_res = filter_res == 'True'
                    yield sampleID, filter_res
            pass

        return inner()

    def add(self, sampleID, filter_res):
        with open(self.filter_res_file, 'a')as f:
            f.write(f'{sampleID} {str(filter_res)}\n')

    @property
    def info(self):
        total = 0
        retained = 0
        for sampleID, filter_res in self:
            total += 1
            retained += filter_res
        return total, retained

    def save_to_csv(self, init_csv_path, filtered_csv_path):
        cnt = [-1, 0]
        with open(init_csv_path, 'r')as init_csv:
            with open(filtered_csv_path, 'w')as filtered_csv:
                with open(self.filter_res_file, 'r')as filter_res_f:
                    filtered_csv.write(init_csv.readline())
                    cur_videoID = ''
                    cur_filter_res = False

                    def process_sample():
                        cnt[0] += 1
                        if cur_filter_res:
                            filtered_csv.write(init_csv.readline())
                            cnt[1] += 1
                        else:
                            init_csv.readline()

                    while 1:
                        line = filter_res_f.readline().strip()
                        if not line:
                            break
                        sampleID, fr = line.split(' ')
                        videoID_, fr = sampleID[:-2], (fr != 'False')
                        if videoID_ == cur_videoID:
                            cur_filter_res |= fr
                        else:
                            process_sample()
                            cur_videoID = videoID_
                            cur_filter_res = fr

                    process_sample()


        print(f'total: {cnt[0]}, after filter: {cnt[1]}')
                        



class DataFilter:
    def __init__(self, csv_file, filter_res_file):
        # csv_file = path(csv_file)
        self.data_iter = iter(PandasDataIter(csv_file=csv_file))
        self.filter_res = FilterResult(filter_res_file=filter_res_file)
        pass
    

    def filter_func(self, sample:PandasSample):
        if sample.desirable_filtering != 'desirable':
            return False
        if len(sample.shot_boundary_detection) > 1:
            return False
        if PandasSample.timestamp_to_float(sample.timeend)-PandasSample.timestamp_to_float(sample.timestart) <= 3:
            return False
        
        def query_llm(prompt: str):            
            response = llm_api(prompt.format(caption=sample.caption)).lower()
            if 'no' in response:
                return 0
            elif 'yes' in response:
                return 1
            else:
                with open(self.filter_res.filter_res_file.parent / 'exception_llm_api.txt', 'a')as f:
                    f.write(f'{gap_line()}\n{sample.sampleID} {sample.caption}\n{prompt}\n{response}\n\n')
                return 2
        
        r1 = query_llm(PROMPT1)
        if r1 == 0:
            return True
        elif r1 == 2:
            return None

        r2 = query_llm(PROMPT2)
        if r2 == 0:
            return False
        elif r2 == 2:
            return None

        r3 = query_llm(PROMPT3)
        if r3 == 0:
            return True
        elif r3 == 1:
            return False
        else:
            return None

        return True
    
    def start(self):
        pg = tqdm.tqdm()
        for _ in self.filter_res:
            next(self.data_iter)
            pg.update(1)
        with open(self.filter_res.filter_res_file, 'a')as f:
            for sample in self.data_iter:
                f.write(
                    f'{sample.sampleID} {str(self.filter_func(sample))}\n'
                )
                pg.update(1)
        
        # print(self.filter_res.info)


if __name__ == '__main__':
    target_csv = '/home/zhipang/PhyDynamics/data/Pandas-70M/panda70m_training_10m.csv'
    target_csv = '/home/zhipang/PhyDynamics/data/Pandas-70M/panda70m_training_full.csv'
    target_csv = '/home/zhipang/PhyDynamics/data/Pandas-70M/panda70m_validation_with_additional_annotation.csv'
    target_csv = '/home/zhipang/PhyDynamics/data/Pandas-70M/panda70m_testing_with_additional_annotation.csv'
    target_csv = '/home/zhipang/PhyDynamics/data/Pandas-70M/panda70m_training_2m.csv'
    
    target_csv = path(target_csv)
    version = 'base_3sec_llm1'
    filter_res_txt = path('/home/zhipang/PhyDynamics/data/Pandas-70M/filter_res/') / version / f'{target_csv.stem}.txt'
    # filter_res_txt = '/home/zhipang/PhyDynamics/data/Pandas-70M/filter_res_valid.txt'
    dfilter = DataFilter(target_csv, filter_res_txt)
    # dfilter.start()
    # print(FilterResult(filter_res_txt).info)

    FilterResult('/home/zhipang/PhyDynamics/data/Pandas-70M/filter_res/base_3sec_llm1/panda70m_training_2m.txt').save_to_csv(
        init_csv_path=target_csv,
        filtered_csv_path=filter_res_txt.parent / (target_csv.stem+'.csv')
    )

    '''
    test
2000 

6000 
3613
2886

    valid
2000 

6000 
3748
2955

    2m
800000 

2400000 
1482263
1182194

    10m
3755240 

10473922 
6455269
5222312

    full
3779763 

70723513 
46376170
34127659
    '''