#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>
#include <map>

using namespace cv;
using namespace std;


float* foo( cv::Mat image ){
        
        cv::Mat img = image;
        
        if(! image.data )                              
            {
                cout <<  "Could not open || find the image" << std::endl ;
                return NULL;
            }

    int* colorVec = new int[10];
    for(int k=0;k<10;k++){
        colorVec[k] = 0;
        }        

    
    
    for (int y = 0; y < img.rows; y++){
        for (int x= 0; x < img.cols; x++ ){
            
            if (img.at<cv::Vec3b>(y,x) == cv::Vec3b(0,0,0)){ colorVec[0]++;continue; }
            if (img.at<cv::Vec3b>(y,x) == cv::Vec3b(0,0,255)){ colorVec[1]++;continue; }
            if (img.at<cv::Vec3b>(y,x) == cv::Vec3b(255,0,0)){ colorVec[2]++;continue; }
            if (img.at<cv::Vec3b>(y,x) == cv::Vec3b(0,255,0)){ colorVec[3]++;continue;}
            if (img.at<cv::Vec3b>(y,x) == cv::Vec3b(159,155,255)){ colorVec[4]++;continue; }
            if (img.at<cv::Vec3b>(y,x) == cv::Vec3b(96,100,0)){ colorVec[5]++;continue;}
            if (img.at<cv::Vec3b>(y,x) == cv::Vec3b(255,255,255)){ colorVec[6]++;continue;}
            if (img.at<cv::Vec3b>(y,x) == cv::Vec3b(255,255,0)){colorVec[7]++; continue;}
            if (img.at<cv::Vec3b>(y,x) == cv::Vec3b(0,255,255)){ colorVec[8]++;continue;}
            if (img.at<cv::Vec3b>(y,x) == cv::Vec3b(255,0,255)){ colorVec[9]++;continue;}
            std::cout << image.at<cv::Vec3b>(y,x) << " color no contemplado"<< std::endl;
        }
    }

    float * returnVec = new float[10];
    for (int k=0;k<10;k++){
        returnVec[k] = (float)colorVec[k] / (float)(image.rows*image.cols);

    }
    
    return returnVec;

    }
