# Train pos_tag model command

```bash
python train.py --train tmp/shoe_data/train.txt --test tmp/shoe_data/test.txt --model tmp/model.bin
```
# Run pos_tag model
```bash
python pos_tag.py --text "unisex" --model "E:\ptit\khdl\PTIT-Shoes-Web-Scrape-And-Analysis\tmp\model.bin"
```

model.bin và train.txt đặt ở trong folder tmp

train.py là chỗ train model'

trong folder util/crf có 2 file là load_data.py và train.py là 2 file xử lí đọc data và train model dc import vào train.py ở ngoài src

Hiện tại model có train được nhưng không chính xác
