import os
from collections import defaultdict
import matplotlib.pyplot as plt

def analyze_dataset():
    dataset_path = "d:/rice_detect_system/datasets"
    stats = defaultdict(lambda: defaultdict(int))
    class_names = ['Bacteria_Leaf_Blight', 'Brown_Spot', 'Leaf_smut']
    
    for split in ['train', 'valid', 'test']:
        labels_dir = os.path.join(dataset_path, split, 'labels')
        
        for label_file in os.listdir(labels_dir):
            if label_file.endswith('.txt'):
                with open(os.path.join(labels_dir, label_file), 'r') as f:
                    lines = f.readlines()
                    stats[split]['total_images'] += 1
                    
                    # 记录图片包含的病害类别
                    classes_in_image = set()
                    for line in lines:
                        class_id = int(line.split()[0])
                        classes_in_image.add(class_id)
                    
                    # 统计每个类别的图片数
                    for class_id in classes_in_image:
                        stats[split][f'class_{class_id}_images'] += 1
    
    # 计算总图片数
    total_images = sum(stats[split]['total_images'] for split in ['train', 'valid', 'test'])
    
    # 打印统计结果
    print("数据集统计分析结果:")
    for split in ['train', 'valid', 'test']:
        split_percentage = (stats[split]['total_images'] / total_images) * 100
        print(f"\n{split}集:")
        print(f"图片总数: {stats[split]['total_images']}张 ({split_percentage:.1f}%)")
        print("各类别图片分布:")
        for class_id in [0, 1, 2]:
            count = stats[split][f'class_{class_id}_images']
            percentage = (count / stats[split]['total_images']) * 100
            print(f"  {class_names[class_id]}: {count}张 ({percentage:.1f}%)")
    
    # 可视化部分
    plt.figure(figsize=(12, 10))
    plt.rcParams['font.sans-serif'] = ['SimSun']  # 设置中文字体为宋体
    plt.rcParams['font.family'] = 'SimSun'  # 设置字体族为宋体
    plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
    plt.rcParams['font.size'] = 10.5  # 五号字体大小
    plt.rcParams['mathtext.fontset'] = 'custom'  # 设置数学公式字体
    plt.rcParams['mathtext.rm'] = 'Times New Roman'  # 设置英文和数字字体
    plt.rcParams['mathtext.it'] = 'Times New Roman:italic'  # 设置斜体
    plt.rcParams['mathtext.bf'] = 'Times New Roman:bold'  # 设置粗体
    
    # 1. 数据集划分比例饼图
    plt.subplot(2, 2, 1)
    sizes = [stats[split]['total_images'] for split in ['train', 'valid', 'test']]
    labels = [f'{split}集\n({sizes[i]}张, {sizes[i]/total_images*100:.1f}%)' 
             for i, split in enumerate(['train', 'valid', 'test'])]
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, 
           textprops={'fontsize':10}, pctdistance=0.85)
    plt.title('数据集划分比例', pad=15, fontsize=12)

    # 2. 各类别总体分布柱状图
    plt.subplot(2, 2, 2)
    total_counts = [sum(stats[split][f'class_{i}_images'] for split in ['train', 'valid', 'test'])
                   for i in [0, 1, 2]]
    plt.bar(class_names, total_counts, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.title('各类别总体分布', fontsize=12)
    plt.ylabel('图片数量', fontsize=11)
    plt.xticks(rotation=15)

    # 3. 各数据集类别分布堆叠柱状图
    plt.subplot(2, 2, 3)
    width = 0.5
    splits = ['train', 'valid', 'test']
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    for i, class_name in enumerate(class_names):
        counts = [stats[split][f'class_{i}_images'] for split in splits]
        plt.bar(splits, counts, width, label=class_name, bottom=[
            sum(stats[split][f'class_{j}_images'] for j in range(i)) 
            for split in splits
        ], color=colors[i])
    plt.title('各数据集类别分布', fontsize=12)
    plt.ylabel('图片数量', fontsize=11)
    plt.legend(fontsize=10)
    
    # 4. 各类别在数据集中的分布比例
    plt.subplot(2, 2, 4)
    for i, class_name in enumerate(class_names):
        sizes = [stats[split][f'class_{i}_images'] for split in ['train', 'valid', 'test']]
        labels = [f'{split}集\n({sizes[j]}张, {sizes[j]/sum(sizes)*100:.1f}%)' 
                 for j, split in enumerate(['train', 'valid', 'test'])]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90,
               textprops={'fontsize':9}, pctdistance=0.85)
        plt.title(f'{class_name}分布比例', fontsize=12)
        break  # 只显示第一个类别的饼图，避免重复

    plt.tight_layout(pad=3.0)
    plt.savefig('d:/rice_detect_system/datasets/dataset_stats.png', dpi=300, bbox_inches='tight')
    print("\n统计图表已保存至: d:/rice_detect_system/datasets/dataset_stats.png")

analyze_dataset()