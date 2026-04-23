# STL/JPG -> Point Cloud + Pose Alignment

Перед запуском укажите пути **в коде**, в файле `project_paths.py`.

## 1) Настройка путей

Откройте `project_paths.py` и задайте:
- `INPUT_STL` — входной STL
- `INPUT_JPG` — входная фотография
- `STL_CLOUD`, `JPG_CLOUD` — промежуточные облака точек
- `ALIGNED_STL`, `TRANSFORM_TXT` — итоговые файлы

По умолчанию используются папки:
- `data/` для входа
- `output/` для результатов

## 2) Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3) Запуск (без аргументов)

```bash
python stl_to_pointcloud.py
python jpg_to_pointcloud.py
python align_pointclouds_and_pose_stl.py
```

## Примечания

- Все параметры также задаются в коде:
  - `stl_to_pointcloud.py`: `NUM_POINTS`, `METHOD`
  - `jpg_to_pointcloud.py`: `FX`, `FY`, `CX`, `CY`, `MAX_DEPTH`, `VOXEL_SIZE`
  - `align_pointclouds_and_pose_stl.py`: `VOXEL_SIZE`, `ICP_THRESHOLD`, `SAVE_TRANSFORM`
- При первом запуске `jpg_to_pointcloud.py` MiDaS модель будет скачана через `torch.hub`.
