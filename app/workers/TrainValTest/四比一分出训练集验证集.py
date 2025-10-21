import pathlib
import sys
import shutil
from collections import defaultdict
import math
from typing import Dict, List


def split_train_val_sets(
        source_dir: str,
        train_dir: str,
        valid_dir: str,
        dry_run: bool = True
) -> None:
    """
    根据“银行名称-样式”维度，将源文件夹中的.jpg文件按约4:1的比例
    移动（剪切）到训练集和验证集文件夹。

    约束条件: 每个类别在训练集和验证集都至少包含一个文件。

    Args:
        source_dir (str): 包含原始图片的源文件夹路径。
        train_dir (str): 用于存放训练集样本的目标文件夹路径。
        valid_dir (str): 用于存放验证集样本的目标文件夹路径。
        dry_run (bool, optional): 是否为演练模式。True则只打印操作，不实际移动文件。
    """
    source_path = pathlib.Path(source_dir)
    train_path = pathlib.Path(train_dir)
    valid_path = pathlib.Path(valid_dir)

    # --- 1. 验证和准备 ---
    if not source_path.is_dir():
        print(f"错误: 源文件夹 '{source_dir}' 不存在或不是一个有效的文件夹。")
        sys.exit(1)

    print(f"[*] 开始扫描源文件夹: {source_path.resolve()}")

    if dry_run:
        print("[*] --- 演练模式 --- (文件不会被实际移动)")
        print(f"[*] 训练集文件夹 (计划): {train_path.resolve()}")
        print(f"[*] 验证集文件夹 (计划): {valid_path.resolve()}")
    else:
        print("\033[91m[警告] --- 生效模式 --- 文件将从源文件夹被永久移动!\033[0m")
        try:
            print(f"[*] 准备目标文件夹...")
            train_path.mkdir(parents=True, exist_ok=True)
            valid_path.mkdir(parents=True, exist_ok=True)
            print("    └── 训练集和验证集文件夹已就绪。")
        except OSError as e:
            print(f"错误: 无法创建目标文件夹. 错误信息: {e}")
            sys.exit(1)

    print("-" * 60)

    # --- 2. 第一步: 扫描所有文件并按类别分组 ---
    print("[*] 正在扫描并按“银行-样式”类别分组文件...")
    grouped_files: Dict[tuple, List[pathlib.Path]] = defaultdict(list)
    total_files_scanned = 0
    malformed_count = 0

    for file_path in sorted(source_path.rglob('*.jpg')):  # 排序以保证每次运行结果一致
        if not file_path.is_file():
            continue

        total_files_scanned += 1
        parts = file_path.stem.split('_')

        if len(parts) < 3:
            malformed_count += 1
            continue

        bank_name = parts[0]
        style = parts[2]
        category = (bank_name, style)
        grouped_files[category].append(file_path)

    print(f"[*] 分组完成。发现 {len(grouped_files)} 个独特的类别。")
    print("-" * 60)

    # --- 3. 第二步: 对每个组进行划分并移动文件 ---
    print("[*] 开始按类别划分训练集和验证集...")
    total_moved_train = 0
    total_moved_valid = 0
    skipped_categories_count = 0

    for category, files in grouped_files.items():
        bank_name, style = category
        n = len(files)

        print(f"\n处理类别: '{bank_name} - {style}' (共 {n} 个文件)")

        # 根据约束，每个类别至少需要2个文件才能划分
        if n <= 1:
            print("    └── 警告: 文件数量不足2个，无法划分，已跳过。")
            skipped_categories_count += 1
            continue

        # 计算分配数量：确保验证集至少有1个，训练集至少有1个
        # 使用 max(1, ...) 确保即使在数量很少的情况下，验证集也能分到1个
        # round(n / 5) 是为了最接近20%的比例
        num_valid = max(1, round(n / 5))
        num_train = n - num_valid

        print(f"    └── 划分计划: {num_train} 个用于训练, {num_valid} 个用于验证。")

        # 分配文件列表
        files_for_valid = files[:num_valid]
        files_for_train = files[num_valid:]

        # 移动到验证集
        for file_path in files_for_valid:
            if not dry_run:
                try:
                    shutil.move(str(file_path), str(valid_path / file_path.name))
                except OSError as e:
                    print(f"      └── ❌ 移动失败: {file_path.name} -> {e}")
                    continue
            print(f"      └── [验证集] 移动: {file_path.name}")
            total_moved_valid += 1

        # 移动到训练集
        for file_path in files_for_train:
            if not dry_run:
                try:
                    shutil.move(str(file_path), str(train_path / file_path.name))
                except OSError as e:
                    print(f"      └── ❌ 移动失败: {file_path.name} -> {e}")
                    continue
            print(f"      └── [训练集] 移动: {file_path.name}")
            total_moved_train += 1

    # --- 4. 总结报告 ---
    print("-" * 60)
    print(f"[*] 操作完成。")
    print(f"[*] 共扫描 {total_files_scanned} 个 .jpg 文件。")
    if malformed_count > 0:
        print(f"[*] 跳过了 {malformed_count} 个文件名格式不正确的文件。")
    if skipped_categories_count > 0:
        print(f"[*] 跳过了 {skipped_categories_count} 个因文件数不足而无法划分的类别。")

    print("\n[*] 最终统计:")
    if dry_run:
        print(f"[*] [演练模式] 计划移动 {total_moved_train} 个文件到训练集。")
        print(f"[*] [演练模式] 计划移动 {total_moved_valid} 个文件到验证集。")
    else:
        print(f"[*] 成功移动 {total_moved_train} 个文件到训练集: {train_path.resolve()}")
        print(f"[*] 成功移动 {total_moved_valid} 个文件到验证集: {valid_path.resolve()}")


# ==============================================================================
# --- MAIN SCRIPT CONTROLLER ---
# ==============================================================================
def main():
    """
    配置并运行数据集划分任务。
    """
    # ==================== 1. 基本配置 ====================
    #
    # 源文件夹：包含所有原始.jpg文件的文件夹路径
    # 示例: r'C:\Users\YourUser\Desktop\所有回单'
    SOURCE_DIRECTORY = r'C:\Users\EDY\Desktop\testProject\申元按银行顺序标注回单\post处理\0916回单标注0917完成的已复检（新规）'

    # 训练集目标文件夹：划分出的训练集图片将被移动到这里
    # 示例: r'C:\Users\YourUser\Desktop\dataset\train'
    TRAIN_DIRECTORY = r'C:\Users\EDY\Desktop\testProject\申元按银行顺序标注回单\post处理\train'

    # 验证集目标文件夹：划分出的验证集图片将被移动到这里
    # 示例: r'C:\Users\YourUser\Desktop\dataset\validation'
    VALID_DIRECTORY = r'C:\Users\EDY\Desktop\testProject\申元按银行顺序标注回单\post处理\eval'

    # 演练模式：
    # - True:  只打印将要执行的操作，不实际移动任何文件（强烈建议首次运行时使用）。
    # - False: 实际执行文件移动（剪切）操作。这是一个破坏性操作！
    DRY_RUN_MODE = False

    # =====================================================

    try:
        split_train_val_sets(SOURCE_DIRECTORY, TRAIN_DIRECTORY, VALID_DIRECTORY, DRY_RUN_MODE)
    except Exception as e:
        print(f"\n程序执行时发生意外错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
