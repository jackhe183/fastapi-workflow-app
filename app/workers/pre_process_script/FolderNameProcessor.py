import pathlib
import sys
import os  # 引入 os 以便创建测试文件夹


class FolderNameProcessor:
    """
    一个用于处理特定格式文件夹名称的类。
    文件夹名称格式: part[0]_part[1]_part[2]_...
    """

    def __init__(self, folder_path: pathlib.Path, dry_run: bool = True):
        if not folder_path.is_dir():
            print(f"错误：提供的路径 '{folder_path}' 不是一个有效的文件夹或不存在。")
            sys.exit(1)

        self.path = folder_path
        self.dry_run = dry_run
        self.original_name = self.path.name
        self.parts = self.original_name.split('_')
        # 初始化时的打印信息可以帮助确认目标是否正确，予以保留
        print(f"--- 目标已加载 ---")
        print(f"  路径: {self.path}")
        print(f"  解析: {self.parts}")
        print(f"  演练模式: {'开启' if self.dry_run else '关闭'}")
        print("-" * 20)

    def _commit_changes(self):
        new_name = "_".join(self.parts)
        new_path = self.path.with_name(new_name)

        if self.path.name == new_name:
            print("注意：名称无变化。")
            return

        print(f"操作预览：'{self.path.name}' -> '{new_name}'")

        if self.dry_run:
            print("状态：演练模式，未执行重命名。")
        else:
            try:
                self.path.rename(new_path)
                print(f"状态：成功重命名！")
                self.path = new_path
            except FileExistsError:
                print(f"错误：目标 '{new_name}' 已存在。")
            except Exception as e:
                print(f"发生错误：{e}")

        # 即使在演练模式下也更新内部状态，以支持连续操作
        self.original_name = new_name

    def add(self, new_part: str, index: int):
        if 0 <= index <= len(self.parts):
            self.parts.insert(index, new_part)
            self._commit_changes()
        else:
            print(f"错误：添加操作的索引 {index} 超出范围。")

    def delete(self, index: int):
        if 0 <= index < len(self.parts):
            self.parts.pop(index)
            self._commit_changes()
        else:
            print(f"错误：删除操作的索引 {index} 超出范围。")

    def modify(self, new_part: str, index: int):
        if 0 <= index < len(self.parts):
            self.parts[index] = new_part
            self._commit_changes()
        else:
            print(f"错误：修改操作的索引 {index} 超出范围。")

    def swap(self, index1: int, index2: int):
        if (0 <= index1 < len(self.parts)) and (0 <= index2 < len(self.parts)):
            self.parts[index1], self.parts[index2] = self.parts[index2], self.parts[index1]
            self._commit_changes()
        else:
            print(f"错误：交换操作的索引超出范围。")

    def get(self, index: int) -> str | None:
        """
        获取指定索引位置的 part 字符串 (此版本不打印信息，只返回值)。
        """
        if 0 <= index < len(self.parts):
            return self.parts[index]
        else:
            # 如果索引无效，静默返回 None
            return None


def main():
    # --- 参数配置 ---

    # 将字符串路径转换为 pathlib.Path 对象
    target_folder = pathlib.Path(
        r'/串起来/data/proj1\dd_sss_saa'
    )

    # --- 执行操作 ---
    processor = FolderNameProcessor(target_folder, dry_run=True)

    # 调用 get 方法并打印其返回值
    result = processor.get(2)
    print(result)

    # 你也可以继续执行其他操作
    # print("\n执行其他操作示例:")
    # processor.modify("bbb", 2)


if __name__ == "__main__":
    main()