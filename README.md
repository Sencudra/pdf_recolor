# About

Tired of recoloring pdf assets? This prototype will help!

# How to use

1. Install `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

2. Setup color config

    ```json
    {
        "replacements": [
            {
                "color": {
                    "old": "#000000",
                    "new": "#FFFFFF"
                },
                "opacity": {
                    "old": 1.0,
                    "new": 0.5
                }
            }
        ]

    }

    ```

3. Run tool on one file or directory

```bash
usage: recolor.py [-h] --config-path CONFIG_PATH
                  [--output-path OUTPUT_PATH] [--verbose]
                  target_path
```


# Todo

1. Support colors with opacity.
2. Support gradients.
3. Add ability to recolor without config.
4. Improve performance