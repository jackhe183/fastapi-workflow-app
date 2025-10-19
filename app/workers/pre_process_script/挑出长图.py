import pathlib
import sys
from PIL import Image


def find_and_move_long_images(source_dir: pathlib.Path, dest_dir: pathlib.Path, ratio_threshold: float):
    """
    在源文件夹中查找所有长图并将其移动到目标文件夹。

    Args:
        source_dir (pathlib.Path): 要搜索的源文件夹。
        dest_dir (pathlib.Path): 用于存放长图的目标文件夹。
        ratio_threshold (float): 高宽比阈值。当 "高度/宽度" 大于此值时，判定为长图。
    """
    # 1. 确保目标文件夹存在，如果不存在则创建
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        print(f"目标文件夹已准备就绪: {dest_dir}")
    except OSError as e:
        print(f"错误：无法创建目标文件夹 '{dest_dir}': {e}", file=sys.stderr)
        return

    # 2. 递归查找源文件夹中所有的 jpg/jpeg 文件 (不区分大小写)
    print(f"开始在 '{source_dir}' 中扫描图片文件...")
    image_extensions = {".jpg", ".jpeg"}
    image_paths = [
        p for p in source_dir.rglob('*')
        if p.is_file() and p.suffix.lower() in image_extensions
    ]

    if not image_paths:
        print("未找到任何 .jpg 或 .jpeg 文件。")
        return

    print(f"共找到 {len(image_paths)} 个图片文件，开始筛选长图...")
    long_images_count = 0

    # 3. 遍历所有图片，判断是否为长图
    for image_path in image_paths:
        try:
            # 使用 Pillow 打开图片并获取尺寸
            with Image.open(image_path) as img:
                width, height = img.size

            # 避免除以零的错误
            if width == 0 or height == 0:
                print(f"-> 跳过无效图片 (尺寸为零): {image_path.name}")
                continue

            # 计算高宽比
            aspect_ratio = height / width

            # 4. 如果满足长图条件，则移动文件
            if aspect_ratio > ratio_threshold:
                long_images_count += 1
                print(f"  [发现长图] 文件: {image_path.name} (尺寸: {width}x{height}, 宽高比: {aspect_ratio:.2f})")

                # 准备目标路径，并处理潜在的文件名冲突
                dest_file_path = dest_dir / image_path.name

                # 如果目标文件已存在，则自动重命名
                if dest_file_path.exists():
                    counter = 1
                    while True:
                        new_name = f"{dest_file_path.stem} ({counter}){dest_file_path.suffix}"
                        new_dest_path = dest_dir / new_name
                        if not new_dest_path.exists():
                            dest_file_path = new_dest_path
                            break
                        counter += 1
                    print(f"    - 文件名冲突，将重命名为: {dest_file_path.name}")

                # 移动文件
                try:
                    image_path.rename(dest_file_path)
                    print(f"    - 已成功移动到: {dest_file_path}")
                except OSError as e:
                    print(f"    - [错误] 移动文件 '{image_path.name}' 失败: {e}", file=sys.stderr)

        except FileNotFoundError:
            # 文件可能在处理过程中被移动，忽略即可
            pass
        except Exception as e:
            # 捕获其他异常，如图片文件损坏无法打开
            print(f"-> [错误] 处理文件 '{image_path.name}' 时出错: {e}", file=sys.stderr)

    print(f"\n处理完成！共发现并移动了 {long_images_count} 张长图。")


def main():
    """
    主函数，用于配置和启动任务。
    """
    # ==================== 参数配置 ====================
    # 文件夹A: 包含所有待检查图片的源文件夹路径
    TARGET_FOLDER_A = r"C:\Users\EDY\Desktop\数据集textin\第三批数据清洗\原始数据"  # <-- 修改这里

    # 文件夹B: 用于存放筛选出来的长图的目标文件夹路径
    TARGET_FOLDER_B = r"C:\Users\EDY\Desktop\数据集textin\第三批数据清洗\挑出的长图"  # <-- 修改这里

    # 长图判断阈值: 当 "图片高度 / 图片宽度" 的值大于此阈值时，判定为长图。
    # - 值越大，筛选条件越严格。
    # - 根据您的样本，3.0 是一个比较合理的初始值。
    # - 如果您希望把稍微长一点的图也选出来，可以调低这个值，比如 2.5。
    LONG_IMAGE_RATIO_THRESHOLD = 3.0
    # ================================================

    print("脚本启动...")

    source_path = pathlib.Path(TARGET_FOLDER_A)
    dest_path = pathlib.Path(TARGET_FOLDER_B)

    if not source_path.is_dir():
        print(f"错误：源文件夹 '{source_path}' 不存在或不是一个有效的文件夹。", file=sys.stderr)
        return

    find_and_move_long_images(source_path, dest_path, LONG_IMAGE_RATIO_THRESHOLD)
    print("\n所有操作已完成。")


if __name__ == "__main__":
    main()