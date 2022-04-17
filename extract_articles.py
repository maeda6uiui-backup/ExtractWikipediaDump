import argparse
import xml.etree.ElementTree as ET
from pathlib import Path
from tqdm import tqdm

def main(args):
    input_root_dirname:str=args.input_root_dirname
    output_root_dirname:str=args.output_root_dirname
    index_output_filepath:str=args.index_output_filepath

    input_root_dir=Path(input_root_dirname)
    input_files=list(input_root_dir.glob("**/*"))
    input_files=[x for x in input_files if x.is_file()]

    output_root_dir=Path(output_root_dirname)
    output_root_dir.mkdir(exist_ok=True,parents=True)

    id_title_dict={}

    for input_file in tqdm(input_files):
        with input_file.open("r") as r:
            data=r.read()

        data="<data>"+data+"</data>"

        element=ET.fromstring(data)

        for doc in element.findall("doc"):
            id=doc.attrib["id"]
            url=doc.attrib["url"]
            title=doc.attrib["title"]
            text=doc.text

            id_title_dict[id]=title

            lines=text.splitlines()
            lines=lines[2:]
            lines=[x for x in lines if x!=""]

            output_dir=output_root_dir.joinpath(str(id))
            output_dir.mkdir(exist_ok=True)

            info_file=output_dir.joinpath("info.txt")
            with info_file.open("w") as w:
                w.write(f"{title}\n")
                w.write(f"{url}\n")

            text_file=output_dir.joinpath("text.txt")
            with text_file.open("w") as w:
                for line in lines:
                    w.write(f"{line}\n")

    with open(index_output_filepath,"w") as w:
        for id,title in id_title_dict.items():
            w.write(f"{id}\t{title}\n")
    
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("-i","--input_root_dirname",type=str)
    parser.add_argument("-o","--output_root_dirname",type=str)
    parser.add_argument("-x","--index_output_filepath",type=str,default="./index.tsv")
    args=parser.parse_args()

    main(args)
