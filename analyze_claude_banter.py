#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script phân tích chi tiết dataset claude_daily_banter.json
"""

import json
import re
from collections import Counter, defaultdict
from typing import Dict, List, Any

def load_dataset(filepath: str) -> List[Dict]:
    """Load JSON dataset"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def analyze_conversation_length(data: List[Dict]) -> Dict:
    """Phân tích độ dài conversations"""
    lengths = []
    for item in data:
        conv_length = len(item['conversations'])
        lengths.append(conv_length)

    return {
        'total_conversations': len(data),
        'min_length': min(lengths),
        'max_length': max(lengths),
        'avg_length': sum(lengths) / len(lengths),
        'length_distribution': Counter(lengths)
    }

def analyze_system_prompts(data: List[Dict]) -> Dict:
    """Phân tích system prompts"""
    system_prompts = []
    relationships = []
    topics = []

    pattern_relationship = r'Bạn là (.*?), đang nói chuyện'
    pattern_topic = r'đang nói chuyện về (.*?)\.'

    for item in data:
        for msg in item['conversations']:
            if msg['role'] == 'system':
                system_prompts.append(msg['content'])

                # Extract relationship
                match_rel = re.search(pattern_relationship, msg['content'])
                if match_rel:
                    relationships.append(match_rel.group(1))

                # Extract topic
                match_topic = re.search(pattern_topic, msg['content'])
                if match_topic:
                    topics.append(match_topic.group(1))

    return {
        'total_system_prompts': len(system_prompts),
        'relationships': Counter(relationships).most_common(20),
        'topics': Counter(topics).most_common(50),
        'sample_prompts': system_prompts[:10]
    }

def analyze_vocabulary(data: List[Dict]) -> Dict:
    """Phân tích từ vựng trong assistant responses"""
    all_words = []
    all_lines = []
    slang_words = []
    emoticons = []

    # Slang patterns
    slang_list = ['vcl', 'vl', 'vãi', 'cháy', 'ngon', 'ngol', 'flex', 'pressing',
                  'đm', 'sml', 'wtf', 'u là trời', 'check var', 'chốt', 'ngầu',
                  'xịn', 'đỉnh', 'feeder', 'hóng', 'phốt', 'FOMO', 'simp',
                  'tích lúa', 'đáng tiền', 'kidney time', 'tụt mood']

    emoticon_pattern = r':\)\)|:\(|:<|:v|:>|:\||:\('

    for item in data:
        for msg in item['conversations']:
            if msg['role'] == 'assistant':
                content = msg['content']
                all_lines.extend(content.split('\n'))

                # Count emoticons
                emoticons.extend(re.findall(emoticon_pattern, content))

                # Count slang
                for slang in slang_list:
                    if slang.lower() in content.lower():
                        slang_words.append(slang)

                # Extract words
                words = re.findall(r'\w+', content.lower())
                all_words.extend(words)

    return {
        'total_words': len(all_words),
        'unique_words': len(set(all_words)),
        'most_common_words': Counter(all_words).most_common(100),
        'slang_usage': Counter(slang_words).most_common(30),
        'emoticon_usage': Counter(emoticons).most_common(10),
        'avg_line_length': sum(len(line) for line in all_lines) / len(all_lines) if all_lines else 0,
        'total_lines': len(all_lines)
    }

def analyze_line_breaks(data: List[Dict]) -> Dict:
    """Phân tích việc xuống dòng trong responses"""
    line_counts = []

    for item in data:
        for msg in item['conversations']:
            if msg['role'] == 'assistant':
                lines = msg['content'].split('\n')
                line_counts.append(len(lines))

    return {
        'avg_lines_per_response': sum(line_counts) / len(line_counts),
        'max_lines': max(line_counts),
        'min_lines': min(line_counts),
        'line_distribution': Counter(line_counts).most_common(10)
    }

def analyze_abbreviations(data: List[Dict]) -> Dict:
    """Phân tích các từ viết tắt"""
    abbreviations = {
        r'\bt\b': 'tao/tôi',
        r'\bm\b': 'mày',
        r'\bko\b|\bk\b': 'không',
        r'\br\b': 'rồi',
        r'\bs\b': 'sao',
        r'\bbt\b': 'biết',
        r'\bvs\b': 'với',
        r'\bj\b': 'gì',
        r'\bh\b': 'giờ',
        r'\bđc\b': 'được',
        r'\bcf\b': 'café',
        r'\bik\b': 'đi'
    }

    abbr_counts = defaultdict(int)

    for item in data:
        for msg in item['conversations']:
            if msg['role'] == 'assistant' or msg['role'] == 'user':
                content = msg['content'].lower()
                for pattern, meaning in abbreviations.items():
                    matches = re.findall(pattern, content)
                    abbr_counts[f"{pattern} ({meaning})"] += len(matches)

    return dict(sorted(abbr_counts.items(), key=lambda x: x[1], reverse=True))

def categorize_by_topic_type(data: List[Dict]) -> Dict:
    """Phân loại theo loại chủ đề"""
    categories = {
        'technology': ['laptop', 'điện thoại', 'iphone', 'tai nghe', 'máy tính', 'app', 'game'],
        'food': ['ăn', 'phở', 'pizza', 'buffet', 'café', 'cà phê', 'đồ ăn', 'order'],
        'entertainment': ['concert', 'phim', 'karaoke', 'game', 'tiktok', 'youtube'],
        'shopping': ['mua', 'giày', 'quần áo', 'đồ', 'shopping'],
        'study_work': ['assignment', 'deadline', 'học', 'pressing', 'việc', 'dự án'],
        'health': ['gym', 'tập', 'sức khỏe', 'bác sĩ', 'trầm cảm', 'nghiện'],
        'relationship': ['bồ', 'crush', 'yêu', 'chia tay', 'đá'],
        'sensitive': ['trầm cảm', 'nghiện', 'quấy rối', 'thai', 'nợ', 'cô lập']
    }

    category_counts = defaultdict(int)

    for item in data:
        for msg in item['conversations']:
            if msg['role'] == 'system':
                content = msg['content'].lower()
                for category, keywords in categories.items():
                    if any(keyword in content for keyword in keywords):
                        category_counts[category] += 1
                        break

    return dict(category_counts)

def main():
    print("=" * 80)
    print("PHÂN TÍCH CHUYÊN SÂU: CLAUDE_DAILY_BANTER.JSON")
    print("=" * 80)

    # Load data
    filepath = '/home/user/polythink-instruct-dataset/dataset/multi-turn/claude_daily_banter.json'
    data = load_dataset(filepath)

    print(f"\n✅ Đã load {len(data)} conversations\n")

    # 1. Conversation length analysis
    print("\n" + "=" * 80)
    print("1. PHÂN TÍCH ĐỘ DÀI HỘI THOẠI")
    print("=" * 80)
    length_stats = analyze_conversation_length(data)
    print(f"Tổng số conversations: {length_stats['total_conversations']}")
    print(f"Độ dài trung bình: {length_stats['avg_length']:.2f} messages")
    print(f"Độ dài min-max: {length_stats['min_length']} - {length_stats['max_length']}")
    print(f"\nPhân bố độ dài (top 10):")
    for length, count in sorted(length_stats['length_distribution'].items())[:10]:
        print(f"  {length} messages: {count} conversations")

    # 2. System prompts analysis
    print("\n" + "=" * 80)
    print("2. PHÂN TÍCH SYSTEM PROMPTS")
    print("=" * 80)
    system_stats = analyze_system_prompts(data)
    print(f"\nTop 10 quan hệ (relationships):")
    for rel, count in system_stats['relationships'][:10]:
        print(f"  '{rel}': {count} lần ({count/len(data)*100:.1f}%)")

    print(f"\nTop 30 chủ đề (topics):")
    for topic, count in system_stats['topics'][:30]:
        print(f"  '{topic}': {count} lần")

    # 3. Vocabulary analysis
    print("\n" + "=" * 80)
    print("3. PHÂN TÍCH TỪ VỰNG")
    print("=" * 80)
    vocab_stats = analyze_vocabulary(data)
    print(f"Tổng số từ: {vocab_stats['total_words']:,}")
    print(f"Số từ unique: {vocab_stats['unique_words']:,}")
    print(f"Tổng số dòng: {vocab_stats['total_lines']:,}")
    print(f"Độ dài trung bình mỗi dòng: {vocab_stats['avg_line_length']:.2f} ký tự")

    print(f"\nTop 30 từ phổ biến nhất:")
    for word, count in vocab_stats['most_common_words'][:30]:
        print(f"  '{word}': {count} lần")

    print(f"\nSlang usage (top 20):")
    for slang, count in vocab_stats['slang_usage'][:20]:
        print(f"  '{slang}': {count} lần")

    print(f"\nEmoticon usage:")
    for emoticon, count in vocab_stats['emoticon_usage']:
        print(f"  '{emoticon}': {count} lần")

    # 4. Line breaks analysis
    print("\n" + "=" * 80)
    print("4. PHÂN TÍCH XUỐNG DÒNG")
    print("=" * 80)
    line_stats = analyze_line_breaks(data)
    print(f"Trung bình số dòng/response: {line_stats['avg_lines_per_response']:.2f}")
    print(f"Min-Max dòng: {line_stats['min_lines']} - {line_stats['max_lines']}")
    print(f"\nPhân bố số dòng:")
    for lines, count in line_stats['line_distribution']:
        print(f"  {lines} dòng: {count} responses")

    # 5. Abbreviations
    print("\n" + "=" * 80)
    print("5. PHÂN TÍCH TỪ VIẾT TẮT")
    print("=" * 80)
    abbr_stats = analyze_abbreviations(data)
    for abbr, count in list(abbr_stats.items())[:15]:
        print(f"  {abbr}: {count} lần")

    # 6. Topic categories
    print("\n" + "=" * 80)
    print("6. PHÂN LOẠI CHỦ ĐỀ")
    print("=" * 80)
    topic_cats = categorize_by_topic_type(data)
    for category, count in sorted(topic_cats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {category.upper()}: {count} conversations ({count/len(data)*100:.1f}%)")

    print("\n" + "=" * 80)
    print("✅ HOÀN TẤT PHÂN TÍCH!")
    print("=" * 80)

if __name__ == '__main__':
    main()
