#!/usr/bin/env bash
# Fetches MuseTalk + its dependencies (~3.5 GB). Run once, from python/.
set -e
cd "$(dirname "$0")"

[ -d repo ] || git clone --depth 1 https://github.com/TMElyralab/MuseTalk.git repo
mkdir -p models/face-parse-bisent
ln -sfn ../models repo/models   # the repo resolves ./models relative to itself

hf download TMElyralab/MuseTalk --local-dir models \
  --include "musetalkV15/musetalk.json" "musetalkV15/unet.pth"
hf download stabilityai/sd-vae-ft-mse --local-dir models/sd-vae \
  --include "config.json" "diffusion_pytorch_model.bin"
hf download openai/whisper-tiny --local-dir models/whisper \
  --include "config.json" "pytorch_model.bin" "preprocessor_config.json"

curl -L https://download.pytorch.org/models/resnet18-5c106cde.pth \
  -o models/face-parse-bisent/resnet18-5c106cde.pth
python -c "
from huggingface_hub import hf_hub_download; import shutil
p = hf_hub_download('ManyOtherFunctions/face-parse-bisent', '79999_iter.pth')
shutil.copy(p, 'models/face-parse-bisent/79999_iter.pth')"

echo '✅ weights ready'
