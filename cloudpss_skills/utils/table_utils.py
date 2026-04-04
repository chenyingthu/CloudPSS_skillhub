"""
表格处理工具函数模块

提供CloudPSS表格数据的解析和格式化功能
"""

from typing import Dict, List, Any, Optional


def table_rows(table: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    把 CloudPSS 表格结果展平成行列表

    Args:
        table: CloudPSS返回的表格数据字典

    Returns:
        展平后的行列表，每行是一个字典

    Example:
        rows = table_rows(result_table)
        for row in rows:
            print(row['Bus'], row['Vm'])
    """
    columns = table.get("data", {}).get("columns", [])
    if not columns:
        return []

    labels = [
        column.get("name") or column.get("title") or f"col_{index}"
        for index, column in enumerate(columns)
    ]
    row_count = len(columns[0].get("data", [])) if columns else 0

    rows = []
    for row_index in range(row_count):
        row_data = {}
        for label, column in zip(labels, columns):
            data = column.get("data", [])
            if row_index < len(data):
                row_data[label] = data[row_index]
            else:
                row_data[label] = None
        rows.append(row_data)

    return rows


def format_table_output(
    headers: List[str],
    rows: List[List[Any]],
    column_widths: Optional[List[int]] = None
) -> str:
    """
    格式化表格输出为字符串

    Args:
        headers: 表头列表
        rows: 数据行列表
        column_widths: 可选的列宽列表

    Returns:
        格式化后的表格字符串
    """
    if not rows:
        return ""

    # 自动计算列宽
    if column_widths is None:
        column_widths = []
        for i, header in enumerate(headers):
            max_width = len(str(header))
            for row in rows:
                if i < len(row):
                    max_width = max(max_width, len(str(row[i])))
            column_widths.append(max_width + 2)  # 添加间距

    # 构建分隔线
    separator = "+" + "+".join(["-" * w for w in column_widths]) + "+"

    # 构建表头行
    header_row = "|" + "|".join([
        f"{str(h):^{column_widths[i]}}" for i, h in enumerate(headers)
    ]) + "|"

    # 构建数据行
    data_rows = []
    for row in rows:
        formatted_cells = []
        for i, cell in enumerate(row):
            if i < len(column_widths):
                formatted_cells.append(f"{str(cell):^{column_widths[i]}}")
        data_rows.append("|" + "|".join(formatted_cells) + "|")

    # 组合所有部分
    lines = [separator, header_row, separator] + data_rows + [separator]
    return "\n".join(lines)
