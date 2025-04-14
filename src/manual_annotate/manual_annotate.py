from pandas_data_iter import *
from ontology_utils import *


MANUAL_ANNOTATION_DIR = path('/home/zhipang/PhyDynamics/data/Pandas-70M/manual_annotation')


class ManualAnnotation:
    def __init__(self, csv_file, ontology_file):
        self.data_iter = iter(PandasDataIter(csv_file=csv_file))
        self.ontology = OntologyNode.load_from_md(md_path=ontology_file)
        self.annotation_file = MANUAL_ANNOTATION_DIR / (path(csv_file).stem+'.txt')
        make_path(file_path=self.annotation_file)
    
    def start_annotate(self):
        with open(self.annotation_file, 'r')as f:
            while f.readline():
                next(self.data_iter)
                # print(1)
        all_val_list = (self.ontology.all_val_list)
        # print(all_val_list)
        assert len(all_val_list) == len(set(all_val_list))
        all_val_set = set(all_val_list)

        for sample in self.data_iter:
            print(sample.caption)
            # print(self.ontology)
            labels = []
            while 1:
                annotation = input().strip()
                if annotation == '-':
                    return

                with open(self.annotation_file, 'a')as f:
                    line = sample.sampleID + ' ' + annotation + '\n'
                    # print(line)
                    f.write(line)
                break
                if annotation == 'n':
                    break

                if annotation not in all_val_set:
                    print(f'{annotation} not in val set')
                    continue
                else:
                    print(f'> added {annotation}')
                    labels.append(annotation)

    def calculate(self):
        res = collections.defaultdict(int)
        with open(self.annotation_file, 'r')as f:
            for line in f.readlines():
                for label in line.split()[1:]:
                    res[label] += 1
        return res


if __name__ == '__main__':
    annotation = ManualAnnotation(
        TRAIN2M_CSV,
        '/home/zhipang/PhyDynamics/CategoryOntology/res_4_1.md',
    )
    # annotation.start_annotate()
    res = annotation.calculate()
    print(res)