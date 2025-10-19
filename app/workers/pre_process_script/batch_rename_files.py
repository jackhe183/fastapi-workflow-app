# batch_rename_files.py

import pathlib
import shutil  # <--- 修改1：导入shutil库用于文件复制
from typing import List


def batch_rename_files(
        source_dir: pathlib.Path,  # <--- 修改2：参数名改为 source_dir
        destination_dir: pathlib.Path,  # <--- 修改3：新增 destination_dir 参数
        prefix: str,
        start_counter: int = 1,
        dry_run: bool = True
):
    """
    递归地扫描源目录中的所有文件，将它们复制并重命名到目标目录中。
    此操作为非破坏性，不会修改源目录中的任何文件。

    Args:
        source_dir: 要扫描的源文件夹路径。
        destination_dir: 复制并重命名后文件存放的目标文件夹。
        prefix: 新文件名的前缀 (当前版本代码未使用，但保留参数)。
        start_counter: 计数器的起始数字。
        dry_run: 如果为 True，则只打印将要进行的操作，不实际复制或重命名文件。
    """
    # --- 1. 安全性与有效性检查 ---
    if not source_dir.is_dir():
        print(f"错误: 源文件夹 '{source_dir}' 不存在或不是一个有效的目录。")
        return

    if dry_run:
        print("=" * 60)
        print("****** 当前为演练模式，不会复制或重命名任何文件。******")
        print("=" * 60)
    else:
        print("=" * 60)
        print("****** !!! 警告：当前为实际操作模式 !!! ******")
        print("******     文件将被复制并重命名到新位置。    ******")
        print("=" * 60)
        # 在实际模式下，如果目标文件夹不存在则创建它
        try:
            destination_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"错误: 无法创建目标文件夹 '{destination_dir}': {e}")
            return

    try:
        # --- 2. 发现所有源文件 ---
        all_files: List[pathlib.Path] = [
            item for item in source_dir.rglob('*') if item.is_file()
        ]
        all_files.sort()  # 排序确保重命名顺序一致

        if not all_files:
            print("信息: 在源目录中未找到任何文件。")
            return

        print(f"总共发现 {len(all_files)} 个文件。准备开始处理...")
        print("-" * 60)

        processed_count = 0
        skipped_count = 0

        # --- 3. 遍历并执行“复制并重命名” ---
        for i, old_path in enumerate(all_files):
            counter = start_counter + i
            file_extension = old_path.suffix

            # 构建新文件名 (根据您的代码，已移除前缀)
            new_name = f"{counter:04d}{file_extension}"

            # <--- 修改4：构建完整的新路径，指向目标文件夹 ---
            new_path = destination_dir / new_name

            # 根据模式执行操作
            if dry_run:
                print(
                    f"[演练] 将复制: '{old_path.relative_to(source_dir.parent)}' -> '{new_path.relative_to(destination_dir.parent)}'")
                processed_count += 1
                continue

            # --- 4. 实际执行操作 ---
            try:
                # 安全性检查：如果新文件名已存在，则跳过
                if new_path.exists():
                    print(f"  -> 警告: 目标文件名 '{new_path.name}' 已存在，跳过此文件。")
                    skipped_count += 1
                    continue

                # <--- 修改5：核心操作从 rename 改为 copy2 ---
                # copy2 会同时复制文件内容和元数据（如修改时间）
                shutil.copy2(old_path, new_path)
                print(f"  -> 成功: 已复制并重命名 '{old_path.name}' -> '{new_path.name}'")
                processed_count += 1

            except Exception as e:
                print(f"  -> 错误: 处理文件 '{old_path.name}' 时发生未知错误: {e}")
                skipped_count += 1

        print("\n" + "=" * 60)
        print("处理完成！")
        if dry_run:
            print(f"演练总结：总共有 {processed_count} 个文件将被复制并重命名。")
        else:
            print(f"成功处理: {processed_count} 个文件")
            if skipped_count > 0:
                print(f"跳过或失败: {skipped_count} 个文件")
        print("=" * 60)

    except Exception as e:
        print(f"在处理过程中发生严重错误: {e}")


# <--- 修改6：将main函数参数化，以便主脚本调用 ---
def main(source_folder: pathlib.Path,
         destination_folder: pathlib.Path,
         prefix: str,
         is_dry_run: bool):
    """
    主函数，用于配置和运行脚本。
    """
    batch_rename_files(
        source_dir=source_folder,
        destination_dir=destination_folder,
        prefix=prefix,
        dry_run=is_dry_run
    )


if __name__ == '__main__':
    # 这是一个直接运行此脚本时的示例配置
    source_directory = pathlib.Path(r"C:\path\to\source_folder")
    dest_directory = pathlib.Path(r"C:\path\to\destination_folder")
    file_prefix = ""  # 前缀

    # 首次运行时，强烈建议将 dry_run 设置为 True
    main(source_directory, dest_directory, file_prefix, is_dry_run=True)