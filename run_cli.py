import cv2, numpy as np, argparse
from gtts import gTTS
from gfpgan import GFPGANer
import subprocess, os

def restore(input_path, output_path):
    restorer = GFPGANer(model_path="models/GFPGANv1.3.pth", upscale=2)
    img = cv2.imread(input_path)
    _, _, restored = restorer.enhance(img, has_aligned=False, only_center_face=False, paste_back=True)
    cv2.imwrite(output_path, restored)

def make_audio(text, out):
    tts = gTTS(text=text, lang="en")
    tts.save(out)

def talk(restored, audio, output):
    img = cv2.imread(restored)
    size = min(img.shape[:2])
    crop = img[(img.shape[0]-size)//2:(img.shape[0]+size)//2,
               (img.shape[1]-size)//2:(img.shape[1]+size)//2]
    cv2.imwrite("temp_face.jpg", crop)
    subprocess.run([
        "python", "-m", "wav2lip.inference",
        "--checkpoint_path", "models/wav2lip.pth",
        "--face", "temp_face.jpg",
        "--audio", audio,
        "--outfile", output
    ])
    os.remove("temp_face.jpg")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output_face", default="output/restored.jpg")
    parser.add_argument("--output_video", default="output/talk_hi.mp4")
    parser.add_argument("--text", default="Hi")
    args = parser.parse_args()

    os.makedirs("output", exist_ok=True)
    restore(args.input, args.output_face)
    make_audio(args.text, "temp_hi.mp3")
    talk(args.output_face, "temp_hi.mp3", args.output_video)
    os.remove("temp_hi.mp3")
    print("✅ Done:", args.output_video)
