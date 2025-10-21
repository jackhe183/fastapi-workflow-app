import pathlib
import random
import os
import shutil


def process_end_folders(target_dir: pathlib.Path, move_to_dir: pathlib.Path, threshold: int, dry_run: bool = True):
    """
    处理目标文件夹下的末端文件夹，将超出阈值的文件移动到指定目录。

    Args:
        target_dir: 目标文件夹的路径。
        move_to_dir: 用于存放超出阈值文件的目标文件夹。
        threshold: 每个末端文件夹中文件的数量上限。
        dry_run: 是否为演练模式。如果为True，则只打印信息而不实际移动文件。
    """
    if not target_dir.is_dir():
        print(f"错误：提供的路径 '{target_dir}' 不是一个有效的文件夹。")
        return

    # 准备移动目标文件夹
    if not dry_run:
        move_to_dir.mkdir(parents=True, exist_ok=True)

    print(f"开始扫描目标文件夹：'{target_dir}'")
    print(f"文件数量阈值上限设置为：{threshold}")
    print(f"超出阈值的文件将被移动到：'{move_to_dir}'")
    if dry_run:
        print("当前为演练模式，不会实际移动任何文件。")
    else:
        print("警告：当前为实战模式，将实际移动文件！")
    print("=" * 50)

    # 使用 rglob 遍历所有子目录
    for p in target_dir.rglob('*'):
        if p.is_dir():
            # 判断是否为末端文件夹（不包含任何其他文件夹）
            subdirs = [sub for sub in p.iterdir() if sub.is_dir()]
            if not subdirs:
                # 获取该文件夹下所有文件的列表
                files = sorted([f for f in p.iterdir() if f.is_file()])  # 排序以保证可复现性
                file_count = len(files)

                print(f"\n[检查末端文件夹] '{p}'")
                print(f"  > 发现 {file_count} 个文件。")

                if file_count > threshold:
                    num_to_move = file_count - threshold
                    print(f"  > 文件数量超出阈值 {threshold}，需要移动 {num_to_move} 个文件。")

                    # 随机选择要移动的文件
                    files_to_move = random.sample(files, num_to_move)

                    for file_to_move in files_to_move:
                        # 构造目标路径
                        destination_path = move_to_dir / file_to_move.name

                        if dry_run:
                            print(f"  [演练] 计划移动: {file_to_move} -> {destination_path}")
                        else:
                            try:
                                # 处理潜在的文件名冲突
                                counter = 1
                                new_destination_path = destination_path
                                while new_destination_path.exists():
                                    new_name = f"{destination_path.stem}_{counter}{destination_path.suffix}"
                                    new_destination_path = move_to_dir / new_name
                                    counter += 1

                                # 使用 shutil.move，因为它更健壮，可以跨盘符移动
                                shutil.move(str(file_to_move), str(new_destination_path))
                                if new_destination_path != destination_path:
                                    print(f"  [已移动] {file_to_move} -> {new_destination_path} (因重名而重命名)")
                                else:
                                    print(f"  [已移动] {file_to_move} -> {new_destination_path}")

                            except (OSError, shutil.Error) as e:
                                print(f"  [错误] 移动文件时出错: {file_to_move} - {e}")
                else:
                    print(f"  > 文件数量未超过阈值，无需操作。")

    print("\n" + "=" * 50)
    print("扫描完成。")


def main():
    """
    主函数，用于配置和运行脚本。
    """
    # ==================== 参数配置 ====================

    # 1. 设置你的目标文件夹路径
    #    请将下面的路径替换为你的实际文件夹路径
    #    例如: target_folder = pathlib.Path(r"C:\Users\YourUser\Documents\MyFolder")
    target_folder = pathlib.Path(
        r"/申元按银行顺序标注回单/post0906回单汇总data（已尽可能合并单联并控制上限30）")

    # 2. 设置用于存放多余文件的目标文件夹路径
    #    脚本会自动创建这个文件夹。这里设置为在目标文件夹的同级目录下创建一个新文件夹。
    #    您可以自定义为您想要的任何有效路径。
    move_destination_folder = target_folder.parent / "超出阈值被移出的文件"

    # 3. 设置每个末端文件夹中允许保留的最多文件数
    file_count_threshold = 30

    # 4. 设置是否为演练模式
    #    True: 只打印将要移动的文件列表，不执行移动操作（推荐首先使用此模式）
    #    False: 实际执行移动操作（请在确认无误后使用）
    is_dry_run = False

    # ===============================================

    # 检查路径是否存在
    if str(target_folder) == "YOUR_TARGET_FOLDER_PATH" or not os.path.exists(target_folder):
        print("请在脚本的 `main` 函数中正确设置 `target_folder` 的路径。")
        return

    process_end_folders(
        target_dir=target_folder,
        move_to_dir=move_destination_folder,
        threshold=file_count_threshold,
        dry_run=is_dry_run
    )


if __name__ == "__main__":
    main()
