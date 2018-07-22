#include <iostream>
#include <sstream>
#include <unistd.h>
#include <opencv2/opencv.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui.hpp>

#define THRESHOLD 50
#define MIN_CONTOUR_AREA 100000

using namespace std;

int fileNumber = 0;
void savePic(cv::Mat frame);


int main(int argc, char* argv[]){
    fileNumber = (int)argv[1][0] - (int)'0';

    cv::VideoCapture cap(0);

    cv::Mat frame, prevFrame, bg, dst, diff, gray, rect;

    vector<vector<cv::Point>> contours;
    //vector<vector<cv::Point>> truncatedContours;
    //cv::Scalar *color = new cv::Scalar(255, 255, 0);

    cap >> frame;
    frame.copyTo(bg);

    cv::imshow("bg", bg);

    while(1){
        cap >> frame;

        cv::absdiff(frame, bg, diff);
        cv::cvtColor(diff, gray, cv::COLOR_BGR2GRAY);
        cv::threshold(gray, dst, THRESHOLD, 255, cv::THRESH_BINARY);

        cv::findContours(dst, contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_NONE);

         for(int i = 0; i < (int)contours.size(); i++){
             if(cv::contourArea(contours.at(i)) >= MIN_CONTOUR_AREA){
                printf("Area is %f\n", cv::contourArea(contours.at(i)));
                savePic(frame);
                // truncatedContours.push_back(contours.at(i));
                cap >> bg;
             }
         }

        //cv::drawContours(frame, truncatedContours, -1, *color, 5);

        cv::imshow("frame", frame);
        cv::imshow("dst", dst);

        contours.clear();
        //truncatedContours.clear();

        int key = cv::waitKey(1) & 0xFF;
        if(key == 'q'){
            break;
        }else if(key == 's'){
            cv::imwrite("capimage.jpg", frame);
        }

    }

    cv::destroyAllWindows();
    // delete color;
    return 0;
}

void savePic(cv::Mat frame){
    string fileName = "image";
    fileName += to_string(fileNumber);
    fileName += ".jpg";
    printf("file name is %s\n", fileName.c_str());
    cv::imwrite(fileName.c_str(), frame);
    fileNumber++;
}
