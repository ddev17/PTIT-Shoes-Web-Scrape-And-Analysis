from util.crf.pos_tag import pos_tag

def run_model(text, model_path='./tmp/model.bin'):
    label = pos_tag(text, format="text", model_path=model_path)
    return label

if __name__ == '__main__':
    # Example input text
    text = "Chàng trai 9X Quảng Trị khởi nghiệp từ nấm sò"
    output = run_model(text)
    print(output)
