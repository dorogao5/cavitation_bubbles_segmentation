# Cavitation Bubbles Segmentation

This project provides tools to detect, segment and track cavitation bubbles in video streams. It uses a YOLO-based segmentation model together with the ByteTrack tracker to extract bubble trajectories and compute various statistics.

## Features

- Bubble detection and segmentation on each frame
- Object tracking with trajectory export
- Automatic CSV reports with size and velocity of each bubble
- Histograms and summary plots for quick analysis
- Streamlit dashboard and FastAPI service
- Docker support for easy deployment

## Quick Start

1. Clone the repository
   ```bash
   git clone https://github.com/your-user/cavitation_bubbles_segmentation.git
   cd cavitation_bubbles_segmentation
   ```
2. Copy `.env.example` to `.env` and adjust parameters
3. Build and run the containers
   ```bash
   docker-compose up --build
   ```
4. Open [http://localhost:8501](http://localhost:8501) to access the Streamlit app and upload a video

## Project Structure

```
├── main_fastapi.py        # REST API for video processing
├── main_streamlit.py      # Web interface
├── download_from_huggingface.py  # download pretrained weights
├── src/
│   ├── segmentation.py        # YOLO segmentation logic
│   ├── tracker_bytetrack.py   # ByteTrack integration
│   ├── tracking.py            # simple centroid tracker
│   ├── video_processing.py    # processing pipeline
│   └── utils.py
```

## Training and Tuning

Use `train_model.py` to train on your dataset and `tune_model.py` to run hyperparameter search. Pretrained weights can be downloaded from Hugging Face with `download_from_huggingface.py`.

## Running Without Docker

Install the dependencies and start the services manually

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main_streamlit.py             # start the dashboard
uvicorn main_fastapi:app --reload    # start the API server
```

## API Endpoints

The FastAPI service exposes a `/process` endpoint that accepts a video and returns processed frames along with bubble statistics. See `main_fastapi.py` for details.

## License

This project is licensed under the MIT License.

## Dataset

The project expects videos containing cavitation bubbles. Training data in YOLO format can be downloaded from Roboflow as shown in the training script. You can use your own dataset by editing `train_model.py` and updating the `data.yaml` path.

## Contributing

Contributions are welcome! Feel free to open issues or pull requests to improve the code, fix bugs, or add new features.

## Example Usage

To run the API server manually

```bash
uvicorn main_fastapi:app --reload
```

To process a single video from the command line

```bash
python main_fastapi.py --input path/to/video.mp4 --output results/
```

After processing, statistics will be stored in the `results` directory along with the annotated video.

## Acknowledgements

This project builds upon the [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) library and the [ByteTrack](https://github.com/ifzhang/ByteTrack) tracker. Special thanks to the Roboflow team for hosting the dataset.
 