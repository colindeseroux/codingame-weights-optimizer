# 🎮 Codingame weights optimizer

The aim of this project is to convert the weights of a NumPy model (.npz) into the most optimised string possible for Codingame.

## 📦 Installation

```sh
pip install -r requirements.txt
```

## ▶️ Usage

### 🧠 Optimizing

Either ensure that you have a `model.npz` file in the current path, or change the path in the main file.

```sh
python optimizer.py
```

### 🚀 Run inference

Copy the text in `model.txt` to the `ENCODED` tag of `inference.py`.  
Modify the inference code with your model and game loop as you like.

## 📚 Citation

If you find LinkedIn-banner-generator is useful, please consider giving us a star 🌟 and citing it.

```bibtex
@software{Codingame-weights-optimizer,
    author = {Colin de Seroux},
    month = apr,
    title = {Codingame-weights-optimizer},
    url = {https://github.com/colindeseroux/codingame-weights-optimizer},
    version = {1.0.0},
    year = {2025}
}
```

## 📄 License

This project is licensed under the Apache License 2.0.  
See the [LICENSE](./LICENSE) file for more details.
