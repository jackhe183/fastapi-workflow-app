# decompress_recursively.py

import pathlib
import shutil
import sys
import time
import patoolib
from patoolib.util import PatoolError

# 支持的压缩文件扩展名集合
ARCHIVE_EXTENSIONS = {
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".iso", ".jar", ".cbz",
    ".cbr", ".ace", ".arj", ".cab", ".chm", ".cpio", ".deb", ".lha", ".lzh",
    ".rpm", ".xz", ".wim"
}


def decompress_recursively(source_folder: pathlib.Path,
                           output_folder: pathlib.Path):
    """
    将源文件夹的所有内容（包括压缩包内的文件）提取到指定的输出文件夹。
    此操作是非破坏性的，不会修改源文件夹。

    Args:
        source_folder (pathlib.Path): 要处理的源文件夹路径。
        output_folder (pathlib.Path): 所有文件将被提取到的目标文件夹路径。
    """
    if not source_folder.is_dir():
        print(f"错误: 源文件夹 '{source_folder}' 不存在或不是一个文件夹。", file=sys.stderr)
        return

    # 确保输出文件夹存在
    output_folder.mkdir(parents=True, exist_ok=True)
    print(f"处理: {source_folder.name}  ->  {output_folder.name}")

    # --- 阶段 1: 遍历源文件夹，复制/解压到输出文件夹 ---
    for item in source_folder.rglob("*"):
        relative_path = item.relative_to(source_folder)
        dest_path = output_folder / relative_path

        if item.is_dir():
            dest_path.mkdir(exist_ok=True)
            continue

        if item.suffix.lower() in ARCHIVE_EXTENSIONS:
            try:
                print(f"  [正在解压] {item.name}")
                patoolib.extract_archive(str(item), outdir=str(dest_path.parent), verbosity=-1)
            except PatoolError as e:
                print(f"  [解压失败] {item.name}: {e}", file=sys.stderr)
        else:
            shutil.copy2(item, dest_path)

    # --- 阶段 2: 在输出文件夹内部，递归处理所有被解压出来的嵌套压缩包 ---

    # ==================== 修改1：增加一个集合来“记忆”已处理过的文件 ====================
    processed_archives = set()
    # =================================================================================

    while True:
        # ==================== 修改2：查找压缩包时，跳过已处理过的 ======================
        nested_archives = [
            p for p in output_folder.rglob('*')
            if p.suffix.lower() in ARCHIVE_EXTENSIONS and p not in processed_archives
        ]
        # =================================================================================

        if not nested_archives:
            break

        for archive in nested_archives:
            # ==================== 修改3：无论后续成功与否，立刻“记住”它 ==================
            processed_archives.add(archive)
            # =================================================================================

            try:
                print(f"  [正在解压嵌套包] {archive.name}")
                patoolib.extract_archive(str(archive), outdir=str(archive.parent), verbosity=-1)

                retries = 5
                delay = 0.2
                for i in range(retries):
                    try:
                        archive.unlink()
                        break
                    except PermissionError:
                        if i < retries - 1:
                            time.sleep(delay)
                        else:
                            print(f"  [删除失败] 无法删除文件 '{archive.name}'。将保留该文件并继续。", file=sys.stderr)

            except PatoolError as e:
                print(f"  [嵌套解压失败] {archive.name}: {e}", file=sys.stderr)


def main(source_folder: pathlib.Path, output_folder: pathlib.Path):
    """
    主函数，用于配置和运行脚本。
    """
    decompress_recursively(source_folder=source_folder, output_folder=output_folder)
    print("\n解压任务完成。")


if __name__ == "__main__":
    BASE_FOLDER = pathlib.Path(r'C:\Users\EDY\Desktop\testProject\串起来\data\proj1')
    TARGET_FOLDER = BASE_FOLDER / 'dd_sss_saa'
    OUTPUT_FOLDER = BASE_FOLDER / "unzip"
    main(source_folder=TARGET_FOLDER, output_folder=OUTPUT_FOLDER)