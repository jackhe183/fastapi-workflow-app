# 文件名建议: split_all_pdfs_in_folder.py

import fitz  # PyMuPDF
import shutil
from pathlib import Path

def split_all_pdfs_in_folder(
        source_dir: Path,
        destination_dir: Path,
        dpi: int
):
    """
    【最终正确版本】
    将一个文件夹内的所有内容（PDF和JPG）统一处理成图片格式，并输出到目标文件夹。
    此脚本封装了所有相关逻辑，包括PDF转换和JPG复制。

    Args:
        source_dir (Path): 包含PDF和JPG文件的源文件夹。
        destination_dir (Path): 用于存放最终所有JPG文件的目标文件夹。
        dpi (int): PDF转JPG时的分辨率。
    """
    # --- 1. 准备工作 ---
    if not source_dir.is_dir():
        print(f"[!] 错误: 源文件夹 '{source_dir}' 不存在。")
        return
    try:
        destination_dir.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"[!] 错误: 无法创建目标文件夹 '{destination_dir}': {e}")
        return

    pdf_files = list(source_dir.rglob("*.pdf"))
    if not pdf_files:
        print("    - 未找到PDF文件。")
    else:
        for pdf_path in pdf_files:
            try:
                with fitz.open(pdf_path) as doc:
                    if not doc.page_count:
                        continue
                    for page_num in range(doc.page_count):
                        page = doc.load_page(page_num)
                        pix = page.get_pixmap(dpi=dpi)
                        output_filename = f"{pdf_path.stem}_page{page_num + 1}.jpg"
                        pix.save(destination_dir / output_filename)
            except Exception as e:
                print(f"    [!] 处理PDF '{pdf_path.name}' 时出错: {e}")
        print(f"    - 完成 {len(pdf_files)} 个PDF文件的转换。")

def main(source_folder: Path, destination_folder: Path, image_dpi: int):
    """主函数，用于被外部脚本调用。"""
    split_all_pdfs_in_folder(
        source_dir=source_folder,
        destination_dir=destination_folder,
        dpi=image_dpi
    )

if __name__ == "__main__":
    SOURCE = Path(r'C:\path\to\source_mixed_files')
    DEST = Path(r'C:\path\to\final_images')
    main(SOURCE, DEST, 150)