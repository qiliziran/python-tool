import os
import sys
from collections import defaultdict
from typing import List, Dict, Union, Tuple


class HexTool:
    def __init__(self):
        self.segments: List[Tuple[int, bytearray]] = []  # 数据片段列表

    def _sort_and_merge_segments(self):
        self.segments.sort(key=lambda x: x[0])
        merged_segments = []

        for segment in self.segments:
            if not merged_segments:
                merged_segments.append(segment)
                continue

            last_segment = merged_segments[-1]
            last_end = last_segment[0] + len(last_segment[1])
            start = segment[0]
            data = segment[1]
            if start < last_end:
                raise ValueError(
                    f"地址重叠错误: 新片段 0x{start:08X}-0x{start + len(data) - 1:08X} "
                    f"与现有片段 0x{last_segment[0]:08X}-0x{last_segment[0] + len(last_segment[1]) - 1:08X} 重叠"
                )
            elif start == last_end:
                # 相邻片段，合并
                last_segment[1].extend(data)
            else:
                # 无重叠，添加新片段
                merged_segments.append(segment)

        self.segments = merged_segments

    def _parse_line(self, line_num, line):
        # 基本验证
        if len(line) < 11:
            raise ValueError(f"行 {line_num}: 行太短")

        # 解析记录长度
        byte_count = int(line[1:3], 16)
        if len(line) < 11 + byte_count * 2:
            raise ValueError(f"行 {line_num}: 长度需要 {11+byte_count*2} 字符, 实际 {len(line)}")

        # 解析地址
        address = int(line[3:7], 16)

        # 解析记录类型
        record_type = int(line[7:9], 16)

        # 解析数据
        data_bytes = []
        data_start = 9
        for i in range(byte_count):
            byte_str = line[data_start + 2 * i : data_start + 2 * i + 2]
            data_bytes.append(int(byte_str, 16))

        # 解析校验和
        checksum_pos = data_start + 2 * byte_count
        checksum = int(line[checksum_pos : checksum_pos + 2], 16)

        # 计算校验和
        all_bytes = [byte_count, address >> 8, address & 0xFF, record_type]
        all_bytes.extend(data_bytes)
        calc_checksum = (-sum(all_bytes)) & 0xFF

        if calc_checksum != checksum:
            raise ValueError(f"行 {line_num}: 校验和错误: 计算值 0x{calc_checksum:02X}, 文件值 0x{checksum:02X}")

        return record_type, address, data_bytes

    def load_hex(self, file_path):
        with open(file_path, "r") as f:
            lines = [line.strip() for line in f.readlines()]

        # 解析所有行
        segment_addr = 0x00000000
        segment_data = bytearray()

        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line.startswith(":"):
                continue

            record_type, address, data_bytes = self._parse_line(line_num, line)

            match record_type:
                case 0x00:  # 数据记录
                    addr = segment_addr + address
                    if addr != segment_addr + len(segment_data):
                        if segment_data:
                            self.segments.append((segment_addr, segment_data))
                        segment_addr = addr
                        segment_data = bytearray()
                    segment_data.extend(data_bytes)
                case 0x01:
                    break
                case 0x04:
                    new_addr = (data_bytes[0] << 8 | data_bytes[1]) << 16
                    if segment_addr != new_addr:
                        if segment_data:
                            self.segments.append((segment_addr, segment_data))
                        segment_addr = new_addr
                        segment_data = bytearray()
                case default:
                    raise ValueError(f"行 {line_num}: 不支持的记录类型: 0x{record_type:02X}")

        # 添加最后一个片段
        if segment_data:
            self.segments.append((segment_addr, segment_data))

        self._sort_and_merge_segments()

        return

    def load_bin(self, file_path, base_address=0):
        with open(file_path, "rb") as f:
            data = f.read()

        bin_start = base_address
        bin_end = base_address + len(data) - 1

        bin_range = range(bin_start, bin_end + 1)
        for segment_start, segment_data in self.segments:
            segment_end = segment_start + len(segment_data) - 1
            segment_range = range(segment_start, segment_end + 1)
            # 判断是否有重叠
            if bin_start <= segment_end and bin_end >= segment_start:
                raise ValueError(
                    f"BIN文件地址空间冲突: BIN地址 0x{bin_start:08X}-0x{bin_end:08X} "
                    f"与已有片段 0x{segment_start:08X}-0x{segment_end:08X} 重叠"
                )

        # 添加新的数据片段
        self.segments.append((bin_start, bytearray(data)))
        self._sort_and_merge_segments()

        return

    def make_hex(self, output_path, block_size=16):
        hex_lines = []

        # 如果没有数据，只添加结束记录
        if not self.segments:
            raise ValueError("没有数据片段可供转换")

        for start, data in self.segments:
            upper_addr = start & 0xFFFF0000
            upper = upper_addr >> 16  # 高位地址
            hex_lines.append(self._make_hex_record(0x04, 0, [upper >> 8, upper & 0xFF]))

            # 处理数据块
            for i in range(0, len(data), block_size):
                hex_lines.append(self._make_hex_record(0x00, start & 0xFFFF, data[i : i + block_size]))
                start += block_size

        # 添加结束记录
        hex_lines.append(":00000001FF")

        with open(output_path, "w") as f:
            f.write("\n".join(hex_lines))

        return

    def make_bin(self, output_path, fill_value=0x00, base_address=None):
        if not self.segments:
            raise ValueError("没有数据片段可供转换")

        if base_address == None:
            base_address = self.segments[0][0]

        # 计算输出数据大小
        end_addr = self.segments[-1][0] + len(self.segments[-1][1]) - 1
        data_size = end_addr - base_address + 1

        # 创建填充数组
        merged_data = bytearray([fill_value] * data_size)

        # 填充实际数据
        for start, data in self.segments:
            merged_data[start - base_address : start - base_address + len(data)] = data

        with open(output_path, "wb") as f:
            f.write(merged_data)

        return len(merged_data)

    def add_segment(self, start_address, data: bytearray):
        segment_start = start_address
        segment_end = start_address + len(data) - 1
        for _start, _data in self.segments:
            _end = _start + len(_data) - 1
            # 检查是否有重叠
            if not (segment_end < _start or segment_start > _end):
                raise ValueError(
                    f"地址重叠错误: 新片段 0x{segment_start:08X}-0x{segment_end:08X} "
                    f"与现有片段 0x{_start:08X}-0x{_end:08X} 重叠"
                )

        self.segments.append((segment_start, data))
        self._sort_and_merge_segments()

        return

    def write_byte(self, address: int, value: int):
        if not 0 <= value <= 255:
            return

        if not self.segments:
            raise ValueError(f"没有任何段")

        for start, data in self.segments:
            end = start + len(data) - 1
            if address >= start and address <= end:
                data[address - start] = value
                return True

        raise ValueError(f"写入地址不存在")

    def print_summary(self):
        if not self.segments:
            print("空")
            return

        start_addr = self.segments[0][0]
        end_addr = self.segments[-1][0] + len(self.segments[-1][1]) - 1
        print(f"起始地址: 0x{start_addr:08X}")
        print(f"结束地址: 0x{end_addr:08X}")
        print(f"地址范围: {end_addr - start_addr + 1:,} 字节")
        print(f"数据片段数: {len(self.segments)}")

        print(f"内存区域:")
        for i, (start, data) in enumerate(self.segments):
            print(f"  片段 {i+1}: 0x{start:08X} - 0x{start + len(data) - 1:08X} " f"({len(data):,} 字节)")

            # 显示片段前16字节的十六进制表示
            preview = " ".join(f"{b:02X}" for b in data[:16])
            if len(data) > 16:
                preview += " ..."
            print(f"      数据预览: {preview}")

    def _make_hex_record(self, record_type, address, data: bytearray):
        data = list(data)

        byte_count = len(data)
        # 构造记录头：长度(1B) + 地址(2B) + 类型(1B)
        header = [
            byte_count,
            (address >> 8) & 0xFF,  # 地址高字节
            address & 0xFF,  # 地址低字节
            record_type,
        ]

        # 合并所有字节：头 + 数据
        record_bytes = header + data

        # 计算校验和：所有字节和的补码
        total = sum(record_bytes)
        checksum = (-total) & 0xFF

        # 格式化为HEX字符串
        hex_str = "".join(f"{b:02X}" for b in (record_bytes + [checksum]))
        return f":{hex_str}"


def main():
    # test
    hex_tool = HexTool()

    hex_tool.load_hex("./data/rh/example.hex")

    hex_tool.add_segment(0x00000000, bytearray([0x11] * 16))
    hex_tool.add_segment(0x00000020, bytearray([0x33] * 16))
    hex_tool.add_segment(0x00000010, bytearray([0x22] * 16))
    hex_tool.write_byte(0x00000001, 0x77)

    hex_tool.print_summary()
    hex_tool.make_hex("data/output/test.hex")
    hex_tool.make_bin("data/output/test.bin")


if __name__ == "__main__":
    main()
