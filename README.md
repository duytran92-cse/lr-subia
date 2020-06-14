# lr-subia
Project SUBIA - La Rochelle, France

## 8 steps to deploy the project

![#f03c15](https://via.placeholder.com/15/f03c15/000000?text=+) Step 1 : Download the dataset [here](https://www.dropbox.com/s/8ftwerhvbrm84ni/subia_dataset.zip) and move it into the project repo

```bash
wget [download_link]
```

![#c5f015](https://via.placeholder.com/15/c5f015/000000?text=+) Step 2 : Clean dataset

```python3 clean-dataset.py```

![#1589F0](https://via.placeholder.com/15/1589F0/000000?text=+) Step 3 : Synchronize dataset

```python3 sync-dataset.py```

![#ee91bc](https://via.placeholder.com/15/ee91bc/000000?text=+) Step 4 : Partition dataset

```python3 data-partition.py```

:large_orange_diamond: *arg1* : mode -> ***all/ALL (recommended), image/IMAGE, annotation/ANNOTATION***

:large_blue_diamond: *arg2* : data training amount

:large_orange_diamond: *arg3* : data training ratio (***less than 1***)

![#6a097d](https://via.placeholder.com/15/6a097d/000000?text=+) Step 5 : PASCAL VOC Conversion

```python3 text2xml.py```

![#a27557](https://via.placeholder.com/15/a27557/000000?text=+) Step 6 : CSV Conversion

```python3 xml2csv.py```