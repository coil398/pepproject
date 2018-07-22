#include <iostream>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/features2d.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc.hpp>

using namespace std;
using namespace cv;

int main(){
    VideoCapture cap(0);
    Ptr<Feature2D> detector = FastFeatureDetector::create();
    vector<KeyPoint> keypoint;
    Mat frame, gray_image;

    if(!cap.isOpened()){
        return -1;
    }

    while(1){
        cap >> frame;

        cvtColor(frame, gray_image, CV_RGB2GRAY);

        detector->detect(gray_image, keypoint);

        for(int i = 0; i < keypoint.size(); i++){
            KeyPoint *point = &(keypoint[i]);
            Point center;
            int radius;
            center.x = cvRound(point->pt.x);
            center.y = cvRound(point->pt.y);
            radius = cvRound(point->size*0.25);
            circle(frame, center, radius, Scalar(51, 0, 255));
        }

        imshow("Window", frame);

        int key = waitKey(1) & 0xff;
        if(key == 'q'){
            break;
        }else if(key == 's'){
            imwrite("capimage.jpg", frame);
        }
    }
    destroyAllWindows();
    return 0;
}
