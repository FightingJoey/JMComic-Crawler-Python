# -*- coding:UTF-8 -*-
import os, sys, shutil
from jmcomic.cl import get_env
  
def get_all_pdfs(directory):  
    pdfs = []  # 用来存放所有PDF文件的列表  
  
    # 使用os.walk()函数遍历目录及其所有子目录  
    for dirpath, dirnames, filenames in os.walk(directory):  
        # 使用glob.glob()函数找到所有PDF文件  
        for filename in filenames:  
            if filename.endswith('.pdf'):  # 如果文件以'.pdf'结尾  
                pdfs.append(os.path.join(dirpath, filename))  # 添加文件路径到列表中  

    return pdfs

def main():
    root = get_env('JM_DOWNLOAD_DIR', None)
    pdfs = get_all_pdfs(root)
    for pdf in pdfs:
        val = os.system(f'pdf-compressor --compression-level low "{pdf}"')
        print(val)
        os.remove(pdf)

if __name__ == '__main__':
    main()
