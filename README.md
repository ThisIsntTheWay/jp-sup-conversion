# SUP to ASS conversion
Script to convert SUPs into ASS subtitles using `manga-ocr`.  

Basically another take on [VobSubConvertJp](https://github.com/naipofo/VobSubConvertJp), but using a newer `manga-ocr` version and with all dependencies conveniently packaged into a container image.

>[!WARNING]
>This won't produce perfect subtitles, but it'll produce good enough results

## Usage with docker
1. Place all `.sup` files into some folder, e.g. `subtitles`
2. Run containierized script against folder
```bash
docker run --rm --gpus all                             \
    -v $(pwd)/subtitles:/app/subtitles                 \
    -t ghcr.io/thisisnttheway/jp-sup-conversion:latest \
    subtitles
```

>[!NOTE]
>To use CUDA, ensure that the package `nvidia-container-toolkit` has been installed.  
>Otherwise, omit the `--gpu` argument.

## Usage without docker
1. Clone repo
2. Ensure [`vobsub2png`](https://crates.io/crates/vobsub2png) is installed
3. Ensure Java is installed and [`BDSup2Sub.jar`](https://raw.githubusercontent.com/wiki/mjuhasz/BDSup2Sub/downloads/BDSup2Sub.jar) is in the same place as the script (`main.py`)
4. Install all python requirements
```bash
pip install --no-cache-dir -r requirements.txt
```
5. Put all `.sup` files into a folder, e.g. `subtitles`
6. Run script against folder with `.sup` files
```bash
python3 main.py subtitles
```