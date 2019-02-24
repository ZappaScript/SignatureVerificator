#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <iostream>
#include <map>
#include <boost/python.hpp>
using namespace cv;
using namespace std;



    
Vec3b patternArray = Vec3b(0,0,0);
Vec3b backgroundArray = Vec3b(255,255,255);

std::map<std::string,Vec2i> points;


std::map<std::string,Vec2i> buildMap(std::map<std::string,Vec2i> points){


points["p2"] = Vec2i( -1, 0 );
points["p3"] = Vec2i( -1, 1 );
points["p4"] = Vec2i( 0, 1 );
points["p5"] = Vec2i( 1, 1 );
points["p6"] = Vec2i( 1, 0 );
points["p7"] = Vec2i( 1, -1 );
points["p8"] = Vec2i( 0, -1 );
points["p9"] = Vec2i( -1, -1 );


/*points.insert( std::pair <std::string, Vec2i>( "p2", Vec2i( -1, 0 )));
points.insert( std::pair <std::string, Vec2i>( "p3", Vec2i( -1, 1 )));
points.insert( std::pair <std::string, Vec2i>( "p4", Vec2i( 0, 1 )));
points.insert( std::pair <std::string, Vec2i>( "p5", Vec2i( 1, 1 )));
points.insert( std::pair <std::string, Vec2i>( "p6", Vec2i( 1, 0 )));
points.insert( std::pair <std::string, Vec2i>( "p7", Vec2i( 1, -1 )));
points.insert( std::pair <std::string, Vec2i>( "p8", Vec2i( 0, -1 )));
points.insert( std::pair <std::string, Vec2i>( "p9", Vec2i( -1, -1 ))); */

return points;
}

int getPositiveNeighbors(int x,int y,Mat img)
    {
        int numPN = 0;
    for (int i = -1; i<2; i++){
        for (int z = -1; z < 2; z++){
            if(i==0 && z==0)
                continue;
            if  (img.at<Vec3b>(y+i,x+z)==patternArray ) 
                numPN+=1; 
                }
         }
    return numPN;
    }

bool firstCondition(int x,int y, Mat img)
    {
        int res = getPositiveNeighbors(x,y,img);
        if  ( (2 <= res) && (res <= 6))
        {
       
        return true;
        }
    return false;
}

bool secondCondition(int x,int y, Mat img)
        {
        int numberTransitions = 0;
        
        if ( (img.at<Vec3b>(y + points["p9"][0], x + points["p9"][1] ) == backgroundArray) && (img.at<Vec3b>(y + points["p2"][0], x + points["p2"][1]) == patternArray) ) 
            {
                //p9-p2
                numberTransitions+=1;
            }
        
        if ((img.at<Vec3b>(y + points["p2"][0], x + points["p2"][1]) == backgroundArray) && (img.at<Vec3b>(y + points["p3"][0], x + points["p3"][1]) == patternArray) ) 
            {
                //p2-p3
                numberTransitions+=1;
            }
        
        if ((img.at<Vec3b>(y + points["p3"][0], x + points["p3"][1]) == backgroundArray) && (img.at<Vec3b>(y + points["p4"][0], x + points["p4"][1]) == patternArray) ) 
            {
                //p3-p4
                numberTransitions+=1;
            }

        if ((img.at<Vec3b>(y + points["p4"][0], x + points["p4"][1]) == backgroundArray) && (img.at<Vec3b>(y + points["p5"][0], x + points["p5"][1]) == patternArray) ) 
            {
                //p4-p5
                numberTransitions+=1;
            }

        if ((img.at<Vec3b>(y + points["p5"][0], x + points["p5"][1]) == backgroundArray) && (img.at<Vec3b>(y + points["p6"][0], x + points["p6"][1]) == patternArray) ) 
            {
                //p5-p6
                numberTransitions+=1;
            }

        if ((img.at<Vec3b>(y + points["p6"][0], x + points["p6"][1]) == backgroundArray) && (img.at<Vec3b>(y + points["p7"][0], x + points["p7"][1]) == patternArray) ) 
            {
                //p6-p7
                numberTransitions+=1;
            }

        if ((img.at<Vec3b>(y + points["p7"][0], x + points["p7"][1]) == backgroundArray) && (img.at<Vec3b>(y + points["p8"][0], x + points["p8"][1]) == patternArray) ) 
            {
                //p7-p8
                numberTransitions+=1;
            }

        if ((img.at<Vec3b>(y + points["p8"][0], x + points["p8"][1]) == backgroundArray) && (img.at<Vec3b>(y + points["p9"][0], x + points["p9"][1]) == patternArray) ) 
            {
                //p9
                numberTransitions+=1;
            }      
        
        
        return (numberTransitions==1);
    }    
        

bool unevenThirdFourthCondition(int x,int y, Mat img)
    {
    bool thirdCond = (img.at<Vec3b>(y + points["p2"][0], x + points["p2"][1]) == backgroundArray) || (img.at<Vec3b>(y + points["p4"][0], x + points["p4"][1])==backgroundArray)  || (img.at<Vec3b>(y + points["p6"][0], x + points["p6"][1])==backgroundArray);
    bool fourthCond = (img.at<Vec3b>(y + points["p4"][0], x + points["p4"][1]) == backgroundArray) || (img.at<Vec3b>(y + points["p6"][0], x + points["p6"][1])==backgroundArray)  || (img.at<Vec3b>(y + points["p8"][0], x + points["p8"][1])==backgroundArray);
    
    return ( thirdCond && fourthCond );
    }

bool evenThirdFourthCondition(int x,int y, Mat img)
    {
    
        bool thirdCond = (img.at<Vec3b>(y + points["p2"][0], x + points["p2"][1])==backgroundArray) || (img.at<Vec3b>(y + points["p4"][0], x + points["p4"][1])==backgroundArray)  || (img.at<Vec3b>(y + points["p8"][0], x + points["p8"][1])==backgroundArray);
        bool fourthCond = (img.at<Vec3b>(y + points["p2"][0], x + points["p2"][1])==backgroundArray) || (img.at<Vec3b>(y + points["p6"][0], x + points["p6"][1])==backgroundArray)  || (img.at<Vec3b>(y + points["p8"][0], x + points["p8"][1])==backgroundArray);
        
        return ( thirdCond && fourthCond );
    
    }


    extern "C" int foo( Mat image )
{
    //Mat image;
    //image = imread(argv, CV_LOAD_IMAGE_COLOR);   // Read the file

    if(! image.data )                              // Check f|| invalid input
    {
        cout <<  "Could not open || find the image" << std::endl ;
        return -1;
    }

    namedWindow( "Display window", WINDOW_AUTOSIZE );// Create a window f|| display.
    imshow( "Display window", image );                   // Show our image inside it.

    waitKey(0);                                          // Wait f|| a keystroke in the window
    return 0;
}

bool applyThiningProcedure(Mat img,int x,int y,bool even){
    bool change = false;
    
    if  (img.at<Vec3b>(y,x) == Vec3b(255,255,255) )
        {
            return false;
        }

    if (even)
        {
            
            if(firstCondition(x,y,img) && secondCondition(x,y,img) && evenThirdFourthCondition(x,y,img))
            {
                
                img.at<Vec3b>(y,x) = Vec3b(255,255,255);
                change = true;
            }
        }
        else
        {   
            
            if(firstCondition(x,y,img) && secondCondition(x,y,img) && unevenThirdFourthCondition(x,y,img))
            {
                
                img.at<Vec3b>(y,x) = Vec3b(255,255,255);
                change = true;
            }
        
        }    
    return change; //check identation in ||iginal file



}


extern "C" Mat zhThinning(Mat img){
    
    points = buildMap(points);
    int changes = 1;
    int height= img.rows;
    int width = img.cols;
    cout << height << " " << width << endl;
    
    copyMakeBorder(img,img, 1, 1, 1, 1, BORDER_CONSTANT, Vec3b(255,255,255));
    while(changes > 0)
    {
        changes = 0;
        for (int even=1;even < 3; even++)
        {
            for (int y= 0; y < height; y++)
            {
                for (int x = 0; x < width; x++) 
                {
                        
                    if (applyThiningProcedure(img,x,y, even%2 == 0 ))
                        {changes += 1;
                        
    
                        }
                }
            }
        }
    }
    //string newRoute = route.substr(0,route.length()-4) + "_t.tif";
    //imwrite(newRoute,img) ;   
    return img;
    

}

