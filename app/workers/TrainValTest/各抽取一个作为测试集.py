import pathlib
import sys
import shutil
from typing import Set, Tuple


def extract_and_move_samples_by_dimension(source_dir: str, dest_dir: str, dry_run: bool = True) -> None:
    """
    根据“银行名称-样式”维度，从源文件夹中为每个组合抽取一个.jpg样本文件，
    并将其移动（剪切）到目标文件夹。

    Args:
        source_dir (str): 包含原始图片的源文件夹路径。
        dest_dir (str): 用于存放抽取样本的目标文件夹路径。
        dry_run (bool, optional): 是否为演练模式。True则只打印操作，不实际移动文件。
    """
    source_path = pathlib.Path(source_dir)
    dest_path = pathlib.Path(dest_dir)

    # --- 1. 验证和准备 ---
    if not source_path.is_dir():
        print(f"错误: 源文件夹 '{source_dir}' 不存在或不是一个有效的文件夹。")
        sys.exit(1)

    print(f"[*] 开始扫描源文件夹: {source_path.resolve()}")

    if dry_run:
        print("[*] --- 演练模式 --- (文件不会被实际移动)")
        print(f"[*] 样本文件计划被移动到: {dest_path.resolve()}")
    else:
        print("\033[93m[警告] --- 生效模式 --- 文件将从源文件夹被永久移动!\033[0m")  # 添加颜色以示警告
        try:
            print(f"[*] 准备目标文件夹: {dest_path.resolve()}")
            dest_path.mkdir(parents=True, exist_ok=True)
            print("    └── 目标文件夹已就绪。")
        except OSError as e:
            print(f"错误: 无法创建目标文件夹 '{dest_path}'. 错误信息: {e}")
            sys.exit(1)

    print("-" * 60)

    # --- 2. 扫描与提取 ---
    processed_combinations: Set[Tuple[str, str]] = set()
    total_files_scanned = 0
    samples_moved = 0
    malformed_count = 0

    for file_path in source_path.rglob('*.jpg'):
        if not file_path.is_file():
            continue

        total_files_scanned += 1
        parts = file_path.stem.split('_')

        if len(parts) < 3:
            malformed_count += 1
            continue

        bank_name = parts[0]
        style = parts[2]
        combination = (bank_name, style)

        # 如果这个“银行-样式”组合尚未处理过，则处理它
        if combination not in processed_combinations:

            destination_file_path = dest_path / file_path.name

            print(f"[*] 发现新组合 '{bank_name} - {style}'")
            print(f"    └── 抽取样本文件: {file_path.name}")

            if not dry_run:
                try:
                    # 将 shutil.copy2 更改为 shutil.move
                    shutil.move(file_path, destination_file_path)
                    print(f"    └── ✅ 移动成功")
                except OSError as e:
                    print(f"    └── ❌ 移动失败: {e}")
            else:
                # 在演练模式下，只打印信息
                print(f"    └── (演练) 将移动到: {destination_file_path}")

            print()

            # 标记这个组合为已处理
            processed_combinations.add(combination)
            samples_moved += 1

    # --- 3. 总结报告 ---
    print("-" * 60)
    print(f"[*] 操作完成。")
    print(f"[*] 共扫描 {total_files_scanned} 个 .jpg 文件。")
    print(f"[*] 发现 {len(processed_combinations)} 个不同的“银行-样式”组合。")
    if malformed_count > 0:
        print(f"[*] 警告: 跳过了 {malformed_count} 个文件名格式不正确的文件。")

    if dry_run:
        print(f"[*] 在演练模式下，共有 {samples_moved} 个样本文件被识别，可供移动。")
    else:
        print(f"[*] 成功移动 {samples_moved} 个样本文件到目标文件夹。")
    print(f"[*] 目标文件夹路径: {dest_path.resolve()}")


# ==============================================================================
# --- MAIN SCRIPT CONTROLLER ---
# ==============================================================================
def main():
    """
    配置并运行文件名分析与样本剪切任务。
    """
    # ==================== 1. 基本配置 ====================
    #
    # 源文件夹：包含所有原始.jpg文件的文件夹路径
    # 示例: r'C:\Users\YourUser\Desktop\回单照片'
    SOURCE_DIRECTORY = r'C:\Users\EDY\Desktop\testProject\申元按银行顺序标注回单\post处理\0916回单标注0917完成的已复检（新规）'

    # 目标文件夹：用于存放提取出的样本图片的文件夹路径（如果不存在，脚本会自动创建）
    # 示例: r'C:\Users\YourUser\Desktop\回单样本'
    DESTINATION_DIRECTORY = r'C:\Users\EDY\Desktop\testProject\申元按银行顺序标注回单\post处理\test'

    # 演练模式：
    # - True:  只打印将要执行的操作，不实际移动任何文件（强烈建议首次运行时使用）。
    # - False: 实际执行文件移动（剪切）操作。这是一个破坏性操作！
    DRY_RUN_MODE = False

    # =====================================================

    try:
        extract_and_move_samples_by_dimension(SOURCE_DIRECTORY, DESTINATION_DIRECTORY, DRY_RUN_MODE)
    except Exception as e:
        print(f"\n程序执行时发生意外错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
