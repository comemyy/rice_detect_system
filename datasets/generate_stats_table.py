import os
from collections import defaultdict
import pandas as pd

def generate_stats_table():
    dataset_path = "d:/rice_detect_system/datasets"
    stats = defaultdict(lambda: defaultdict(int))
    class_names = ['Bacteria_Leaf_Blight', 'Brown_Spot', 'Leaf_smut']
    
    # 收集统计数据
    for split in ['train', 'valid', 'test']:
        labels_dir = os.path.join(dataset_path, split, 'labels')
        
        for label_file in os.listdir(labels_dir):
            if label_file.endswith('.txt'):
                with open(os.path.join(labels_dir, label_file), 'r') as f:
                    lines = f.readlines()
                    stats[split]['total_images'] += 1
                    
                    classes_in_image = set()
                    for line in lines:
                        class_id = int(line.split()[0])
                        classes_in_image.add(class_id)
                    
                    for class_id in classes_in_image:
                        stats[split][f'class_{class_id}_images'] += 1

    # 创建并保存Excel表格
    data = []
    for class_id, class_name in enumerate(class_names):
        row = {'病害类别': class_name}
        for split in ['train', 'valid', 'test']:
            row[f'{split}集数量'] = stats[split][f'class_{class_id}_images']
        data.append(row)
    
    df = pd.DataFrame(data)
    excel_path = 'd:/rice_detect_system/datasets/disease_stats.xlsx'
    df.to_excel(excel_path, index=False)
    print(f"统计表格已保存至: {excel_path}")

if __name__ == '__main__':
    generate_stats_table()