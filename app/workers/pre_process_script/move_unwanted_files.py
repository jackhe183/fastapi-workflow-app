# move_unwanted_files.py

import pathlib
import sys


def move_unwanted_files(source_dir: pathlib.Path,
                        destination_dir: pathlib.Path,
                        keep_extensions: set,
                        dry_run: bool = True):
    """
    Recursively scans a source directory and moves files that do not have
    one of the specified extensions to a destination directory.

    Args:
        source_dir: The directory to scan for files.
        destination_dir: The directory where non-kept files will be moved.
        keep_extensions: A set of lower-case file extensions to keep (e.g., {'.pdf', '.jpg'}).
        dry_run: If True, only prints the actions that would be taken without
                 moving any files.
    """
    # --- 1. 安全性和有效性检查 ---
    if not source_dir.is_dir():
        print(f"错误：源文件夹 '{source_dir}' 不存在或不是一个有效的目录。", file=sys.stderr)
        return

    if dry_run:
        print("=" * 50)
        print("****** 当前为演练模式，不会移动任何文件。******")
        print("=" * 50 + "\n")
    else:
        print("=" * 50)
        print("****** !!! 警告：当前为实际操作模式 !!! ******")
        print("******           文件将被实际移动。         ******")
        print("=" * 50 + "\n")
        # 在实际模式下，如果目标文件夹不存在则创建它
        try:
            destination_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"错误：无法创建目标文件夹 '{destination_dir}': {e}", file=sys.stderr)
            return

    files_to_move = []
    # --- 2. 递归查找所有文件 ---
    print(f"正在扫描文件夹: '{source_dir}'...")
    all_files = [p for p in source_dir.rglob('*') if p.is_file()]

    for path in all_files:
        # 检查文件的扩展名是否在保留列表中（统一转为小写进行比较）
        if path.suffix.lower() not in keep_extensions:
            files_to_move.append(path)

    if not files_to_move:
        print("扫描完成，没有找到需要移动的文件。")
        return

    print(f"扫描完成，共找到 {len(files_to_move)} 个需要移动的文件。")

    # --- 3. 执行移动操作 ---
    for old_path in files_to_move:
        target_path = destination_dir / old_path.name

        # --- 核心安全功能：处理目标文件夹中的文件名冲突 ---
        # 如果目标文件已存在，则在文件名后添加序号
        counter = 1
        new_stem = old_path.stem
        while target_path.exists():
            new_name = f"{new_stem}({counter}){old_path.suffix}"
            target_path = destination_dir / new_name
            counter += 1

        # --- 根据模式执行操作 ---
        if dry_run:
            if new_stem != old_path.stem:  # 如果文件名因冲突而改变
                print(f"[演练] 将移动: '{old_path.relative_to(source_dir)}' -> '{target_path.name}' (因重名而改名)")
            else:
                print(f"[演练] 将移动: '{old_path.relative_to(source_dir)}' -> '{target_path.name}'")
        else:
            # 实际移动文件
            try:
                old_path.rename(target_path)
                if new_stem != old_path.stem:
                    print(f"已移动: '{old_path.name}' -> '{target_path.name}' (因重名而改名)")
                else:
                    print(f"已移动: '{old_path.name}' -> '{target_path.name}'")
            except OSError as e:
                print(f"错误：移动文件 '{old_path.name}' 时失败: {e}", file=sys.stderr)

    print("\n文件移动任务完成。")


# ==================== 修改开始 ====================
def main(source_folder: pathlib.Path,
         destination_folder: pathlib.Path,
         extensions_to_keep: set,
         is_dry_run: bool):
    """
    主函数，用于配置和运行脚本。
    """
    move_unwanted_files(source_folder,
                        destination_folder,
                        extensions_to_keep,
                        dry_run=is_dry_run)
# ==================== 修改结束 ====================


if __name__ == "__main__":
    # ########################### 参数配置区 ###########################
    IS_DRY_RUN = True
    EXTENSIONS_TO_KEEP = {'.pdf', '.jpg'}
    source_folder = pathlib.Path(
        r"C:\Users\EDY\Desktop\testProject\0910回单\rawdata")
    destination_folder = pathlib.Path(
        r"C:\Users\EDY\Desktop\testProject\0910回单\test")
    # ##################################################################

    main(source_folder,
         destination_folder,
         EXTENSIONS_TO_KEEP,
         is_dry_run=IS_DRY_RUN)