#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import random

with open('/home/user/polythink-instruct-dataset/dataset/multi-turn/claude_daily_banter.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Lấy 20 mẫu để phân tích pattern
# Lấy mẫu đầu, giữa, cuối và random
samples = []
samples.append(data[0])  # Mẫu đầu
samples.append(data[100])
samples.append(data[200])
samples.append(data[400])
samples.append(data[600])
samples.append(data[800])  # Mẫu cuối
samples.extend(data[830:840])  # 10 mẫu sensitive topics

for i, sample in enumerate(samples, 1):
    print('=' * 80)
    print(f'MẪU {i}: {sample["id"]}')
    print('=' * 80)
    for msg in sample['conversations']:
        role = msg['role'].upper()
        content = msg['content']
        print(f'{role}:')
        print(content)
        print()
    print()
