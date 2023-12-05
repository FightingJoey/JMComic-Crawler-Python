# -*- coding:UTF-8 -*-
import os, sys, shutil
import subprocess
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

def compress(source, output):
    compressPdfDocument = ap.Document(source)  # 需要压缩的pdf文件路径
    pdfoptimizeOptions = ap.optimization.OptimizationOptions()
    pdfoptimizeOptions.image_compression_options.compress_images = True
    pdfoptimizeOptions.image_compression_options.image_quality = 10
    compressPdfDocument.optimize_resources(pdfoptimizeOptions)
    compressPdfDocument.save(output)  # 需要压缩后保存的文件路径

def get_ghostscript_path():
    gs_names = ['gs', 'gswin32', 'gswin64']
    for name in gs_names:
        if shutil.which(name):
            return shutil.which(name)
    raise FileNotFoundError(f'No GhostScript executable was found on path ({"/".join(gs_names)})')


def main():
    root = get_env('JM_DOWNLOAD_DIR', None)
    pdfs = get_all_pdfs(root)
    # gs = get_ghostscript_path()
    # quality = {
    #     0: '/default',
    #     1: '/prepress',
    #     2: '/printer',
    #     3: '/ebook',
    #     4: '/screen'
    # }
    for pdf in pdfs:
        # file_name = os.path.basename(pdf)[:-4]
        # directory = os.path.dirname(pdf)
        # compress_pdf = os.path.join(directory, file_name + '-compress.pdf')
        # print(f"源文件: {pdf}, 压缩文件: {compress_pdf}")
        # compress(pdf, compress_pdf)

        subprocess.call(f'pdf-compressor --compression-level low "{pdf}"')

        # os.remove(pdf)

if __name__ == '__main__':
    main()
