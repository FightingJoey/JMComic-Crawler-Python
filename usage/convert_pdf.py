import re
import os, sys
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from PyPDF2 import PdfReader, PdfWriter

output_dirs = []

def convert(root=None, sub_root=None):
    dir_path = root if sub_root == None else sub_root
    fs = os.listdir(dir_path)
    has_subdir = False
    for f1 in fs:
        tmp_path = os.path.join(dir_path, f1)
        if not 'output' in tmp_path and os.path.isdir(tmp_path):
            has_subdir = True
            convert(dir_path, tmp_path)
        elif not '.DS_Store' in tmp_path and not os.path.isdir(tmp_path):
            has_subdir = False
            break
    if has_subdir == False:
        output = os.path.join(root, 'output')
        if not os.path.exists(output):
            os.makedirs(output)
            output_dirs.append(output)
        pdf_name = os.path.join(output, os.path.basename(sub_root) + '.pdf')
        imgs_to_pdf(sub_root, pdf_name)
        deldir(sub_root)
        print(f"{pdf_name} 转化完成！")

def imgs_to_pdf(folder_path, pdf_file_path):
    """
    合成文件夹下的所有图片为pdf
    Args:
        folder_path (str): 源文件夹
        pdf_file_path (str): 输出路径
    """
    img_extensions = ('jpg', 'jpeg', '.png', 'bmp', '.tiff', '.tiff', '.webp')
    img_files = [f for f in os.listdir(folder_path) if f.lower().endswith(img_extensions)]
    img_files.sort(key=lambda x: int(x.split('.')[0]))
    
    images = []
    for file in img_files:
        img_path = os.path.join(folder_path, file)
        image = Image.open(img_path).convert("RGB")
        images.append(image)

    if len(images) != 0:
        images[0].save(pdf_file_path, save_all=True, append_images=images[1:], quality=95)

def merge_all(root):
    s = os.listdir(root)
    s.sort(key = lambda i: int(re.split(r'(\d+)', i)[1]))
    chunks = list(partition(s, 10))
    for index, sub in enumerate(chunks):
        start = index * 10 + 1
        end = (index + 1) * 10
        if len(sub) < 10:
            end = end - 10 + len(sub)
        output = root + "/{}-{}.pdf".format(start, end)
        merge_pdf(sub, output, root)

# pdf合并函数
def merge_pdf(merge_list, output_pdf, root_dir):
    """
    merge_list: 需要合并的pdf列表
    output_pdf：合并之后的pdf名
    """
    # 实例一个 PDF文件编写器
    output = PdfWriter()
    for ml in merge_list:
        pdf_input = PdfReader(open(os.path.join(root_dir, ml), 'rb'))
        page_count = len(pdf_input.pages)
        for i in range(page_count):
            output.add_page(pdf_input.pages[i])
        if os.path.isfile(os.path.join(root_dir, ml)):
            os.remove(os.path.join(root_dir, ml))
    output.write(open(output_pdf, 'wb'))

def partition(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

# 删除文件夹
def deldir(dir):
    if not os.path.exists(dir):
        return False
    if os.path.isfile(dir):
        os.remove(dir)
        return
    for i in os.listdir(dir):
        t = os.path.join(dir, i)
        if os.path.isdir(t):
            deldir(t)  # 重新调用次方法
        else:
            os.unlink(t)
    if os.path.exists(dir):
        os.removedirs(dir)  # 递归删除目录下面的空文件夹


def main():
    root = sys.argv[1]
    convert(root)
    for output in output_dirs:
        if output == root + '/output':
            continue
        merge_all(output)
    print("所有PDF合并完成！")
    return root

if __name__ == '__main__':
    print(main(), end='')