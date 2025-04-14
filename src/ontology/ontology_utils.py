from utils_zp import *


class OntologyNode:
    def __init__(self, val=None):
        self.val = val
        self.nxt: Dict[str, 'OntologyNode'] = {}
    
    def get_nxt(self, nxt_str):
        if nxt_str not in self.nxt:
            self.nxt[nxt_str] = OntologyNode(nxt_str)
        return self.nxt[nxt_str]
    
    def update_by_dict(self, dic):
        if isinstance(dic, dict):
            for k in sorted(dic):
                self.get_nxt(k).update_by_dict(dic[k])
        elif isinstance(dic, list):
            for k in sorted(dic):
                self.get_nxt(k)
        else:
            raise Exception(f'wrong type of dic, which is {type(dic)}')

    @property
    def dic(self):
        # if not self.nxt:
        #     return self.val
        res = {}
        for p in self.nxt:
            # if not p.nxt:
            res[p] = self.nxt[p].dic
        return res

    @property
    def all_val_list(self):
        lst = [self.val]
        for nxt in self.nxt:
            lst.extend(self.nxt[nxt].all_val_list)
        return lst
    
    def __repr__(self):
        return json.dumps(self.dic, indent=4)
    
    @staticmethod
    def load(json_path):
        root = OntologyNode()
        root.update_by_dict(auto_load(json_path))
        return root
    
    def dump(self, json_path):
        auto_dump(self.dic, json_path)
    
    @staticmethod
    def load_from_md(md_path):
        root = OntologyNode()
        content = auto_load(md_path, force=True)
        stack = [root]
        for line in content.split('\n'):
            if not line.strip().startswith('*'):
                continue
            prefix_space, text = line.split('*', 1)
            text = text.strip()
            deep = len(prefix_space)//4
            stack = stack[:deep+1]
            # print(deep, len(prefix_space))
            nxt_node = (stack[-1].get_nxt(text))
            stack.append(nxt_node)

        return root

    def dump_dic_to_md(self, md_path, deep=-1):
        if deep == -1:
            with open(md_path, 'w')as f:
                f.write('')
        else:
            with open(md_path, 'a')as f:
                if not deep:
                    f.write(f'# {self.val}\n')
                else:
                    f.write(' '*(deep*4-4) + f'* {self.val}\n')
        for nxt_ in self.nxt:
            self.nxt[nxt_].dump_dic_to_md(md_path, deep+1)


if __name__ == '__main__':
    md_path_ = '/home/zhipang/PhyDynamics/CategoryOntology/res_4_1.md'
    ontology = OntologyNode.load_from_md(md_path_)
    print(ontology.dic)
    ontology.dump('/home/zhipang/PhyDynamics/CategoryOntology/ontology_4_1.json')
    