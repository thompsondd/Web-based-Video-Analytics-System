import cv2, os, time, torch, math
from ultralytics import YOLO
from tqdm import tqdm
import numpy as np
from uitls import *

class AI_see:
    def __init__(self,filename,path_model):
        assert os.path.exists(filename), f"File '{filename}' does not exist"
        device = (
            "cuda"
            if torch.cuda.is_available()
            else "mps"
            if torch.backends.mps.is_available()
            else "cpu"
        )

        self.filename=filename
        self.video = cv2.VideoCapture(filename)
        self.video.set(cv2.CAP_PROP_FPS, 60)
        self.video.set(cv2.CAP_PROP_BUFFERSIZE, 5)

        self.model = YOLO(os.path.join(path_model,'yolov8n.pt'))
        self.model.to(device)
        self.className = self.model.names

        # Define the text, font, and position
        self.text = f"Number of people: "
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 2  # Font scale factor
        self.font_color = (0, 0, 255)  # BGR color (green in this case)
        self.font_thickness = 2  # Thickness of the text
        self.position = (10, 50) # Position to place the text (top-left corner)
        (label_width, label_height), baseline = cv2.getTextSize(self.text, self.font, 
                                                                self.font_scale, self.font_thickness)
        self.height_add = math.ceil(max(self.position[1],label_height)*1.35)
        
    def __del__(self):
        self.video.release()
        del self.model

    def get_prediction(self):
        video_read_state, frame = self.video.read()
        results = self.model(frame, stream=True, verbose=False)
        count = 0
        # plot = True
        
        for r in results:
            frame = r.plot()
            boxes = r.boxes
            for box in boxes:
                cls = int(box.cls[0])
                if self.className[cls]=="person":
                    count +=1

        new_h = frame.shape[0]+self.height_add
        new_frame = np.zeros((new_h,frame.shape[1],3))+255.
        new_frame[self.height_add:new_h,:,:] = frame
        new_frame = new_frame.astype('uint8')

        # Insert the text into the image
        cv2.putText(new_frame, self.text+str(count), self.position, self.font, self.font_scale, self.font_color, self.font_thickness)
        return video_read_state, new_frame

    def get_frame(self):
        video_read_state, frame = self.get_prediction()
        frame_convert_state, jpeg = cv2.imencode('.jpg',frame)
        return  jpeg.tobytes()
    
    def create_video(self,st_bar=None):
        fourcc = cv2.VideoWriter_fourcc(*'H264')
        
        path = self.filename

        name,ext = os.path.basename(path).split(".")
        directory_path = os.path.dirname(path)
        output_video = os.path.join(directory_path,"ignore_"+name+"_yolo.mp4")

        # Get the video's frame dimensions and frames per second (fps)
        frame_width = int(self.video.get(3))
        frame_height = int(self.video.get(4))+ self.height_add
        fps = int(self.video.get(5))

        # Create the VideoWriter object to write the video
        out = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height))
        
        total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        bar = tqdm(total=total_frames,desc="Video create")
        if st_bar!=None: 
            t = 0
            start = time.time()
        while True:
            video_read_state, frame = self.get_prediction()
            if video_read_state==False: break
            out.write(frame)
            bar.update(1)
            if st_bar!=None:
                t+=1
                catch = time.time()
                estimated_time = (catch-start)*(total_frames-t)/t
                st_bar.progress(t/total_frames, text=f"Please wait a few seconds! - Estimated finished time: {convert_date_string(estimated_time)}")
        bar.close()
        return output_video