import pathlib
import sqlite3
from preProcessScript import decompress_recursively
from preProcessScript import move_unwanted_files
from preProcessScript import batch_rename_files
from preProcessScript import split_all_pdfs_in_folder # <-- 导入正确的脚本

def preProcess(work_space:str):
    """
    执行完整的工作流：解压 -> 筛选 -> 重命名 -> 格式统一为图片。
    """
    # ==================== 参数配置 ====================
    BASE_FOLDER = pathlib.Path(work_space)
    folder_to_be_unzip = BASE_FOLDER / "0_foldertobeunzip"
    folder_after_unzip = BASE_FOLDER / "1_afterunzip"
    folder_for_unwanted_files = BASE_FOLDER / "2_unwanted_files"
    folder_renamed_mixed = BASE_FOLDER / "3_renamed_mixed_files"
    folder_final_images = BASE_FOLDER / "4_final_images"

    EXTENSIONS_TO_KEEP = {'.pdf', '.jpg'}
    IMAGE_DPI = 150
    # 所有DRY_RUN开关都已移除，默认为实际执行
    # ================================================

    print("### 步骤 1: 开始递归解压 ###")
    decompress_recursively.main(folder_to_be_unzip, folder_after_unzip)
    print("-" * 60)

    print("\n### 步骤 2: 开始移动不需要的文件 ###")
    move_unwanted_files.main(folder_after_unzip, folder_for_unwanted_files, EXTENSIONS_TO_KEEP, is_dry_run=False)
    print("-" * 60)

    print("\n### 步骤 3: 开始复制并重命名文件 ###")
    batch_rename_files.main(folder_after_unzip,
                            folder_renamed_mixed,
                            "", is_dry_run=False)
    print("-" * 60)

    # --- 步骤 4: 调用功能完备的脚本，一步到位 ---
    print("\n### 步骤 4: 整合所有文件为图片格式到最终目录 ###")
    split_all_pdfs_in_folder.main(
        source_folder=folder_renamed_mixed,
        destination_folder=folder_final_images,
        image_dpi=IMAGE_DPI
    )
    print("-" * 60)

    print("\n>>> 所有工作流执行完毕。 <<<")
    print(f"最终成果已全部输出至: {folder_final_images}")

if __name__ == "__main__":
    work_space = r'C:\Users\EDY\Desktop\testProject\串起来\data\proj1'
    preProcess(work_space)
