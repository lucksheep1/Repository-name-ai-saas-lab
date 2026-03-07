#!/usr/bin/env python3
"""
SaaS Lab Heartbeat - 定时汇报执行器
由 OpenClaw heartbeat 触发
"""
import os
import sys
from datetime import datetime

# 添加项目路径
sys.path.insert(0, '/root/.openclaw/workspace')

def should_send_report():
    """检查是否应该发送报告"""
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    
    # AM 窗口: 08:30-09:30
    am_window = (hour == 8 and minute >= 30) or (hour == 9 and minute <= 30)
    
    # PM 窗口: 20:30-21:30  
    pm_window = (hour == 20 and minute >= 30) or (hour == 21 and minute <= 30)
    
    return am_window, pm_window, now

def get_latest_report(report_type):
    """读取最新报告"""
    report_dir = '/root/.openclaw/workspace/reports'
    if report_type == 'AM':
        filepath = f'{report_dir}/daily_report_AM.md'
    else:
        filepath = f'{report_dir}/daily_report_PM.md'
    
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return f.read()
    return None

def format_report_for_feishu(content, report_type):
    """将 Markdown 转为飞书消息"""
    # 简单转换 - 保留标题和列表
    lines = content.split('\n')
    result = []
    for line in lines:
        if line.startswith('# '):
            result.append(f"**{line[2:]}**")
        elif line.startswith('## '):
            result.append(f"**{line[3:]}**")
        elif line.startswith('- ') or line.startswith('* '):
            result.append(f"• {line[2:]}")
        elif line.strip():
            result.append(line)
    return '\n'.join(result)

if __name__ == '__main__':
    am_window, pm_window, now = should_send_report()
    
    if am_window:
        report = get_latest_report('AM')
        if report:
            print("AM 报告窗口已触发")
            # 打印报告，后面由 agent 发送
            print("REPORT_TYPE:AM")
            print(report)
            
    elif pm_window:
        report = get_latest_report('PM')
        if report:
            print("PM 报告窗口已触发")
            # 打印报告，后面由 agent 发送
            print("REPORT_TYPE:PM")
            print(report)
    else:
        print(f"非报告窗口 ({now.hour}:{now.minute})")
