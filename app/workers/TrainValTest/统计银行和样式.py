import pathlib
import sys
from collections import defaultdict
from typing import Dict, Counter


def analyze_filenames(root_directory: str) -> None:
    """
    分析指定目录下的 .jpg 文件名，并按“银行名称-样式”维度进行统计。

    Args:
        root_directory (str): 要扫描的目标文件夹路径。
    """
    root_path = pathlib.Path(root_directory)

    if not root_path.is_dir():
        print(f"错误: 目录 '{root_directory}' 不存在或不是一个有效的文件夹。")
        sys.exit(1)

    print(f"[*] 开始扫描目标文件夹: {root_path.resolve()}")
    print("-" * 60)

    # 使用 defaultdict 和 Counter 来简化统计逻辑
    # 结构: {'宁波银行': Counter({'样式1': 10, '样式2': 5}), '工商银行': Counter({'样式A': 8})}
    stats: Dict[str, Counter[str]] = defaultdict(Counter)

    file_count = 0
    malformed_count = 0
    malformed_examples = []

    # 使用 .rglob('*.jpg') 来递归查找所有 jpg 文件
    for file_path in root_path.rglob('*.jpg'):
        if file_path.is_file():
            file_count += 1
            parts = file_path.stem.split('_')

            # 期望的文件名格式至少有3个部分 (part[0]_part[1]_part[2])
            if len(parts) >= 3:
                bank_name = parts[0]
                style = parts[2]
                stats[bank_name][style] += 1
            else:
                malformed_count += 1
                if len(malformed_examples) < 5:  # 只记录前5个错误示例
                    malformed_examples.append(file_path.name)

    print("[*] 统计结果:")
    if not stats:
        print("  -> 在目标文件夹中未找到符合命名规范的 .jpg 文件。")
    else:
        # 为了美观地打印，先计算列宽
        max_bank_len = max(len(b) for b in stats.keys()) if stats else 0
        header_bank = "银行名称"
        col_width_bank = max(max_bank_len, len(header_bank)) + 4

        print(f"{header_bank:<{col_width_bank}}{'样式':<15}{'数量'}")
        print(f"{'-' * (col_width_bank - 2):<{col_width_bank}}{'-' * 13:<15}{'-' * 5}")

        # 按银行名称排序
        for bank_name in sorted(stats.keys()):
            # 按样式名称排序
            for style, count in sorted(stats[bank_name].items()):
                print(f"{bank_name:<{col_width_bank}}{style:<15}{count}")

    print("-" * 60)
    print(f"[*] 分析完成。")
    print(f"[*] 共扫描到 {file_count} 个 .jpg 文件。")
    if malformed_count > 0:
        print(f"[*] 警告: 有 {malformed_count} 个文件名格式不正确 (下划线分隔部分少于3个)。")
        print(f"[*]    不规范文件名示例: {malformed_examples}")


# ==============================================================================
# --- MAIN SCRIPT CONTROLLER ---
# ==============================================================================
def main():
    """
    配置并运行文件名分析任务。
    """
    # ==================== 配置区 ====================
    #
    # 请将下面的路径替换为你的目标文件夹路径
    # 示例:
    # - Windows: r'C:\Users\YourUser\Desktop\回单照片'
    # - macOS/Linux: '/Users/YourUser/Documents/receipt_images'
    #
    ROOT_DIRECTORY = \
        r'C:\Users\EDY\Desktop\testProject\申元按银行顺序标注回单\post处理\eval'

    # ==============================================

    try:
        analyze_filenames(ROOT_DIRECTORY)
    except Exception as e:
        print(f"\n程序执行时发生意外错误: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
