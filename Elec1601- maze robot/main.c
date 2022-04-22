#include "stdio.h"
#include "stdlib.h"
#include "sdl.h"
#include "SDL2_gfxPrimitives.h"
#include "time.h"

#include "formulas.h"
#include "wall.h"
#include "robot.h"

int done = 0;


int main(int argc, char *argv[]) {
    SDL_Window *window;
    SDL_Renderer *renderer;

    if(SDL_Init(SDL_INIT_VIDEO) < 0){
        return 1;
    }

    window = SDL_CreateWindow("Robot Maze", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, OVERALL_WINDOW_WIDTH, OVERALL_WINDOW_HEIGHT, SDL_WINDOW_OPENGL);
    window = SDL_CreateWindow("Robot Maze", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, OVERALL_WINDOW_WIDTH, OVERALL_WINDOW_HEIGHT, SDL_WINDOW_OPENGL);
    renderer = SDL_CreateRenderer(window, -1, 0);

    struct Robot robot;
    struct Wall_collection *head = NULL;
    int front_left_sensor, front_right_sensor=0;
    int left_sensor, right_sensor = 0;
    clock_t start_time, end_time;
    int msec;
//    int xDir;
//    int xTL;
//    int yTL;
//    int yDir;

    SDL_Surface *m_image;
    SDL_Rect     m_image_position;

    SDL_Surface *m_window_surface;
    SDL_Event    m_window_event;


    SDL_Surface * image = SDL_LoadBMP("car (1).bmp");
    SDL_Surface * imageL = SDL_LoadBMP("car_left.bmp");
    SDL_Surface * image195 = SDL_LoadBMP("car_195.bmp");
    SDL_Surface * image210 = SDL_LoadBMP("car_210.bmp");
    SDL_Surface * image225 = SDL_LoadBMP("car_225.bmp");
    SDL_Surface * image240 = SDL_LoadBMP("car_240.bmp");
    SDL_Surface * image255 = SDL_LoadBMP("car_255.bmp");
    SDL_Surface * image0 = SDL_LoadBMP("car_0.bmp");
    SDL_Surface * image15 = SDL_LoadBMP("car_15.bmp");
    SDL_Surface * image30 = SDL_LoadBMP("car_30.bmp");
    SDL_Surface * image45 = SDL_LoadBMP("car_45.bmp");
    SDL_Surface * image60 = SDL_LoadBMP("car_60.bmp");
    SDL_Surface * image75 = SDL_LoadBMP("car_75.bmp");
    SDL_Surface * image90 = SDL_LoadBMP("car_90.bmp");
    SDL_Surface * image105 = SDL_LoadBMP("car_105.bmp");
    SDL_Surface * image120 = SDL_LoadBMP("car_120.bmp");
    SDL_Surface * image135 = SDL_LoadBMP("car_135.bmp");
    SDL_Surface * image150 = SDL_LoadBMP("car_150.bmp");
    SDL_Surface * image165 = SDL_LoadBMP("car_165.bmp");

    SDL_Surface * image285 = SDL_LoadBMP("car_285.bmp");
    SDL_Surface * image300 = SDL_LoadBMP("car_300.bmp");
    SDL_Surface * image315 = SDL_LoadBMP("car_315.bmp");
    SDL_Surface * image330 = SDL_LoadBMP("car_330.bmp");
    SDL_Surface * image345 = SDL_LoadBMP("car_345.bmp");



    SDL_Surface * imagemap = SDL_LoadBMP("map.bmp");
    SDL_Surface * imagetitle = SDL_LoadBMP("title.bmp");


    SDL_Texture * texture = SDL_CreateTextureFromSurface(renderer, image);
    SDL_Texture * textureL = SDL_CreateTextureFromSurface(renderer, imageL);
    SDL_Texture * texture195 = SDL_CreateTextureFromSurface(renderer, image195);
    SDL_Texture * texture210 = SDL_CreateTextureFromSurface(renderer, image210);
    SDL_Texture * texture225 = SDL_CreateTextureFromSurface(renderer, image225);
    SDL_Texture * texture240 = SDL_CreateTextureFromSurface(renderer, image240);
    SDL_Texture * texture255 = SDL_CreateTextureFromSurface(renderer, image255);

    SDL_Texture * texture0 = SDL_CreateTextureFromSurface(renderer, image0);
    SDL_Texture * texture15 = SDL_CreateTextureFromSurface(renderer, image15);
    SDL_Texture * texture30 = SDL_CreateTextureFromSurface(renderer, image30);
    SDL_Texture * texture45 = SDL_CreateTextureFromSurface(renderer, image45);
    SDL_Texture * texture60 = SDL_CreateTextureFromSurface(renderer, image60);
    SDL_Texture * texture75 = SDL_CreateTextureFromSurface(renderer, image75);
    SDL_Texture * texture90 = SDL_CreateTextureFromSurface(renderer, image90);
    SDL_Texture * texture105 = SDL_CreateTextureFromSurface(renderer, image105);
    SDL_Texture * texture120 = SDL_CreateTextureFromSurface(renderer, image120);
    SDL_Texture * texture135 = SDL_CreateTextureFromSurface(renderer, image135);
    SDL_Texture * texture150 = SDL_CreateTextureFromSurface(renderer, image150);
    SDL_Texture * texture165 = SDL_CreateTextureFromSurface(renderer, image165);
    SDL_Texture * texture285 = SDL_CreateTextureFromSurface(renderer, image285);
    SDL_Texture * texture300 = SDL_CreateTextureFromSurface(renderer, image300);
    SDL_Texture * texture315 = SDL_CreateTextureFromSurface(renderer, image315);
    SDL_Texture * texture330 = SDL_CreateTextureFromSurface(renderer, image330);
    SDL_Texture * texture345 = SDL_CreateTextureFromSurface(renderer, image345);

    SDL_Texture * texturemap = SDL_CreateTextureFromSurface(renderer, imagemap);
    SDL_Texture * texturetitle = SDL_CreateTextureFromSurface(renderer, imagetitle);

    // SETUP MAZE
    // You can create your own maze here. line of code is adding a wall.
    // You describe position of top left corner of wall (x, y), then width and height going down/to right
    // Relative positions are used (OVERALL_WINDOW_WIDTH and OVERALL_WINDOW_HEIGHT)
    // But you can use absolute positions. 10 is used as the width, but you can change this.
//    insertAndSetFirstWall(&head, 1,  OVERALL_WINDOW_WIDTH/2, OVERALL_WINDOW_HEIGHT/2, 10, OVERALL_WINDOW_HEIGHT/2);
//    insertAndSetFirstWall(&head, 2,  OVERALL_WINDOW_WIDTH/2-100, OVERALL_WINDOW_HEIGHT/2+100, 10, OVERALL_WINDOW_HEIGHT/2-100);
//    insertAndSetFirstWall(&head, 3,  OVERALL_WINDOW_WIDTH/2-250, OVERALL_WINDOW_HEIGHT/2+100, 150, 10);
//    insertAndSetFirstWall(&head, 4,  OVERALL_WINDOW_WIDTH/2-150, OVERALL_WINDOW_HEIGHT/2, 150, 10);
//    insertAndSetFirstWall(&head, 5,  OVERALL_WINDOW_WIDTH/2-250, OVERALL_WINDOW_HEIGHT/2-200, 10, 300);
//    insertAndSetFirstWall(&head, 6,  OVERALL_WINDOW_WIDTH/2-150, OVERALL_WINDOW_HEIGHT/2-100, 10, 100);
//    insertAndSetFirstWall(&head, 7,  OVERALL_WINDOW_WIDTH/2-250, OVERALL_WINDOW_HEIGHT/2-200, 450, 10);
//    insertAndSetFirstWall(&head, 8,  OVERALL_WINDOW_WIDTH/2-150, OVERALL_WINDOW_HEIGHT/2-100, 250, 10);
//    insertAndSetFirstWall(&head, 9,  OVERALL_WINDOW_WIDTH/2+200, OVERALL_WINDOW_HEIGHT/2-200, 10, 300);
//    insertAndSetFirstWall(&head, 10,  OVERALL_WINDOW_WIDTH/2+100, OVERALL_WINDOW_HEIGHT/2-100, 10, 300);
//    insertAndSetFirstWall(&head, 11,  OVERALL_WINDOW_WIDTH/2+100, OVERALL_WINDOW_HEIGHT/2+200, OVERALL_WINDOW_WIDTH/2-100, 10);
//    insertAndSetFirstWall(&head, 12,  OVERALL_WINDOW_WIDTH/2+200, OVERALL_WINDOW_HEIGHT/2+100, OVERALL_WINDOW_WIDTH/2-100, 10);
//
//    insertAndSetFirstWall(&head, 2,  220, 400, 10, 80);
//    insertAndSetFirstWall(&head, 2,  20, 400, 200, 10);
//    insertAndSetFirstWall(&head, 2,  20, 50, 10, 350);
//    insertAndSetFirstWall(&head, 2,  20, 50, 280, 10);
//    insertAndSetFirstWall(&head, 2,  300, 50, 10, 100);
//    insertAndSetFirstWall(&head, 2,  300, 150, 110, 10);
//    insertAndSetFirstWall(&head, 2,  400, 50, 10, 100);
//    insertAndSetFirstWall(&head, 2,  400, 50, 220, 10);
//    insertAndSetFirstWall(&head, 2,  620, 50, 10, 290);
//    insertAndSetFirstWall(&head, 2,  620, 340, 20, 10);
//
//    insertAndSetFirstWall(&head, 1,  320, 300, 10, 180);
//    insertAndSetFirstWall(&head, 2,  120, 300, 200, 10);
//    insertAndSetFirstWall(&head, 2,  120, 150, 10, 150);
//    insertAndSetFirstWall(&head, 2,  120, 150, 80, 10);
//    insertAndSetFirstWall(&head, 2,  200, 150, 10, 100);
//    insertAndSetFirstWall(&head, 2,  200, 250, 310, 10);
//    insertAndSetFirstWall(&head, 2,  500, 150, 10, 100);
//    insertAndSetFirstWall(&head, 2,  500, 150, 10, 100);
//    insertAndSetFirstWall(&head, 2,  500, 150, 20, 10);
//    insertAndSetFirstWall(&head, 2,  520, 150, 10, 290);
//    insertAndSetFirstWall(&head, 2,  520, 440, 120, 10);

//    BASIC MAZE B------------------------------------------------------
//
//        insertAndSetFirstWall(&head, 2,  640-10-220, 400, 10, 80);
//    insertAndSetFirstWall(&head, 2,  640-200-20, 400, 200, 10);
//    insertAndSetFirstWall(&head, 2,  640-10-20, 50, 10, 350);
//    insertAndSetFirstWall(&head, 2,  640-280-20, 50, 280, 10);
//    insertAndSetFirstWall(&head, 2,  640-10-300, 50, 10, 100);
//    insertAndSetFirstWall(&head, 2,  640-110-300, 150, 110, 10);
//    insertAndSetFirstWall(&head, 2,  640-10-400, 50, 10, 100);
//    insertAndSetFirstWall(&head, 2,  640-400-220, 50, 220, 10);
//    insertAndSetFirstWall(&head, 2,  640-10-620, 50, 10, 290);
//    insertAndSetFirstWall(&head, 2,  640-620-20, 340, 20, 10);
//
//
//    insertAndSetFirstWall(&head, 1,  640-10-320, 300, 10, 180);
//    insertAndSetFirstWall(&head, 2,  640-200-120, 300, 200, 10);
//    insertAndSetFirstWall(&head, 2,  640-10-120, 150, 10, 150);
//    insertAndSetFirstWall(&head, 2,  640-80-120, 150, 80, 10);
//    insertAndSetFirstWall(&head, 2,  640-10-200, 150, 10, 100);
//    insertAndSetFirstWall(&head, 2,  640-310-200, 250, 310, 10);
//    insertAndSetFirstWall(&head, 2,  640-10-500, 150, 10, 100);
//    insertAndSetFirstWall(&head, 2,  640-20-500, 150, 20, 10);
//    insertAndSetFirstWall(&head, 2,  640-10-520, 150, 10, 290);
//    insertAndSetFirstWall(&head, 2,  640-120-520, 440, 120, 10);

//   //  extension maze -------------------------------------------------------
//#include "math.h"
//
// int i;
//    insertAndSetFirstWall(&head, 12,  120, 450, 10, 30);
//    insertAndSetFirstWall(&head, 12,  220, 450, 10, 30);
//    for (i = 0; i < 100; i++){
//        insertAndSetFirstWall(&head, i,  20 + i , 350 + i, 10, 10); //1
//        insertAndSetFirstWall(&head, i,  20 +100 + i , 350 + i, 10, 10); //1
//    }
//    insertAndSetFirstWall(&head, 12,  20, 280, 10, 70);
//    insertAndSetFirstWall(&head, 12,  120, 280, 10, 70);
//    for (i = 0; i < 180; i++){
//        insertAndSetFirstWall(&head, i,  20 +190 - i/2 , 100 + i, 10, 10); //1
//    }
//    for (i = 0; i < 105; i++){
//        insertAndSetFirstWall(&head, i,  20 +105/2 - i/2 , 175 + i, 10, 10); //1
//    }
//    insertAndSetFirstWall(&head, 2,  20, 175, 105/2, 10);
//    insertAndSetFirstWall(&head, 2,  20, 20, 10, 155);
//    insertAndSetFirstWall(&head, 2,  20, 20, 300, 10);
//    insertAndSetFirstWall(&head, 2,  320, 20, 10, 60);
//    insertAndSetFirstWall(&head, 2,  80, 100, 130, 10);
//    insertAndSetFirstWall(&head, 2,  80, 80, 10, 20);
//    insertAndSetFirstWall(&head, 2,  80, 80, 160, 10);
//
//    double j;
//    for (i = 0; i < 50; i++){
//        j = i;
//        insertAndSetFirstWall(&head, i+1,
//                              // the most important bit is below.
//                              // increase the 20 for a tighter bend
//                              // descrease for a more meandering flow
//                              320 + 30*sin(10*j * M_PI/180),
//                              // increase the 5 for a spacier curve
//                              (i * 5)+80,
//                              10, 10);
//    }
//    for (i = 0; i < 75; i++){
//        j = i;
//        insertAndSetFirstWall(&head, i+1,
//                              // the most important bit is below.
//                              // increase the 20 for a tighter bend
//                              // descrease for a more meandering flow
//                              240 + 30*sin(10*j * M_PI/180),
//                              // increase the 5 for a spacier curve
//                              (i * 5)+80,
//                              10, 10);
//    }
//    insertAndSetFirstWall(&head, 2,  345, 330, 105, 10);
//    insertAndSetFirstWall(&head, 2,  450, 190, 10, 150);
//    insertAndSetFirstWall(&head, 2,  380, 190, 70, 10);
//    insertAndSetFirstWall(&head, 2,  380, 20, 10, 170);
//    insertAndSetFirstWall(&head, 2,  380, 20, 260, 10);
//
//    insertAndSetFirstWall(&head, 2,  255, 455, 345, 10);
//    insertAndSetFirstWall(&head, 2,  600, 100, 10, 365);
//    insertAndSetFirstWall(&head, 2,  530, 100, 70, 10);
//    insertAndSetFirstWall(&head, 2,  530, 80, 10, 20);
//    insertAndSetFirstWall(&head, 2,  530, 80, 110, 10);
//
//insertAndSetFirstWall(&head, 1, 50, OVERALL_WINDOW_HEIGHT - 50, 500, 5);
//insertAndSetFirstWall(&head, 2, 550, OVERALL_WINDOW_HEIGHT - 150, 5, 105);
//insertAndSetFirstWall(&head, 3, 100, OVERALL_WINDOW_HEIGHT - 150, 455,5);
//insertAndSetFirstWall(&head, 4, 100, OVERALL_WINDOW_HEIGHT - 250, 5, 100);
//insertAndSetFirstWall(&head, 5, 100, OVERALL_WINDOW_HEIGHT - 250, 400, 5);
//insertAndSetFirstWall(&head, 6, 500, OVERALL_WINDOW_HEIGHT - 300, 5, 55);
//insertAndSetFirstWall(&head, 7, 150, OVERALL_WINDOW_HEIGHT - 300, 355, 5);
//insertAndSetFirstWall(&head, 8, 150, OVERALL_WINDOW_HEIGHT - 350, 5, 55);
//insertAndSetFirstWall(&head, 9, 150,OVERALL_WINDOW_HEIGHT - 350, 305, 5);
//insertAndSetFirstWall(&head, 10, 450, OVERALL_WINDOW_HEIGHT - 375, 5, 25);
//insertAndSetFirstWall(&head, 11, 200, OVERALL_WINDOW_HEIGHT - 375, 250, 5);
//insertAndSetFirstWall(&head, 12, 200, OVERALL_WINDOW_HEIGHT - 400, 5, 25);
//insertAndSetFirstWall(&head, 13, 200, OVERALL_WINDOW_HEIGHT - 400, 295, 5);
#include "math.h"

 int i;
    for (i = 0; i < 100; i++){
        insertAndSetFirstWall(&head, i,  500 + i , 180 + i, 10, 10); //1
        insertAndSetFirstWall(&head, i,  600 - i , 280 + i, 10, 10); //1
    }
    for (i = 0; i < 25; i++){
    insertAndSetFirstWall(&head, i,  100 - i , 380 + i, 10, 10); //1
    }

//
//    for (i = 0; i < 50; i++){
//        insertAndSetFirstWall(&head, i,  45 + i , 375 + i, 10, 10); //1
//    }

    insertAndSetFirstWall(&head, 4,  45 , 405, 40, 10); //1
    insertAndSetFirstWall(&head, 5,  45 , 385, 10, 50); //1

//insertAndSetFirstWall(&head, 1, 30, OVERALL_WINDOW_HEIGHT - 65, 80, 40);
//insertAndSetFirstWall(&head, 2, 550, OVERALL_WINDOW_HEIGHT - 150, 10, 110);
insertAndSetFirstWall(&head, 3, 100, OVERALL_WINDOW_HEIGHT - 100, 410,10);
//insertAndSetFirstWall(&head, 4, 100, OVERALL_WINDOW_HEIGHT - 250, 10, 100);
//insertAndSetFirstWall(&head, 5, 100, OVERALL_WINDOW_HEIGHT - 250, 400, 10);
//insertAndSetFirstWall(&head, 6, 500, OVERALL_WINDOW_HEIGHT - 300, 10, 60);
insertAndSetFirstWall(&head, 7, 150, OVERALL_WINDOW_HEIGHT - 300, 360, 10);
insertAndSetFirstWall(&head, 8, 150, OVERALL_WINDOW_HEIGHT - 350, 10, 60);
insertAndSetFirstWall(&head, 9, 150,OVERALL_WINDOW_HEIGHT - 350, 310, 10);
insertAndSetFirstWall(&head, 10, 450, OVERALL_WINDOW_HEIGHT - 375, 10, 25);
insertAndSetFirstWall(&head, 11, 200, OVERALL_WINDOW_HEIGHT - 375, 250, 10);
insertAndSetFirstWall(&head, 12, 200, OVERALL_WINDOW_HEIGHT - 400, 10, 25);
insertAndSetFirstWall(&head, 13, 200, OVERALL_WINDOW_HEIGHT - 400, 300, 10);
    updateAllWalls(head, renderer);
    setup_robot(&robot);

    SDL_Event event;




    while(!done){

        SDL_SetRenderDrawColor(renderer, 200, 200, 200, 255);
        SDL_RenderClear(renderer);

        //Move robot based on user input commands/auto commands
        if (robot.auto_mode == 1)
            robotAutoMotorMove(&robot, front_left_sensor, front_right_sensor,  right_sensor, left_sensor);
        robotMotorMove(&robot);



        //Check if robot reaches endpoint. and check sensor values

        if (checkRobotReachedEnd(&robot, 640, 20, 10, 60)){ //Maze 5
        //if (checkRobotReachedEnd(&robot, 0, 340, 10, 100)){ // Maze 3
        //if (checkRobotReachedEnd(&robot, 640, 340, 10, 100)){ //Maze 1
        //if (checkRobotReachedEnd(&robot, 220, 480, 100, 10)){ //Maze 2
        //if (checkRobotReachedEnd(&robot, 640-10-320, 480, 100, 10)){ //Maze 4


        //if (checkRobotReachedEnd(&robot, OVERALL_WINDOW_WIDTH, OVERALL_WINDOW_HEIGHT/2+100, 10, 100)){
            end_time = clock();
            msec = (end_time-start_time) * 1000 / CLOCKS_PER_SEC;
            robotSuccess(&robot, msec);
        }

//        else if(checkRobotHitWalls(&robot, head))
//            robotCrash(&robot);
        //Otherwise compute sensor information
        else {
                                printf("%d", checkRobotHitWalls(&robot, head));

            front_left_sensor = checkRobotSensorFrontLeftAllWalls(&robot, head);
            if (front_left_sensor>0)
                printf("Getting close on the left. Score = %d\n", front_left_sensor);


            front_right_sensor = checkRobotSensorFrontRightAllWalls(&robot, head);
            if (front_right_sensor>0)
                printf("Getting close on the right. Score = %d\n", front_right_sensor);

            right_sensor = checkRobotSensorRightAllWalls(&robot, head);
            if (right_sensor>0)
                    printf("---------------------------Right side. Score = %d\n", right_sensor);


            left_sensor = checkRobotSensorLeftAllWalls(&robot, head);
            if (left_sensor>0)
                    printf("---------------------------Left side. Score = %d\n", left_sensor);

        }

        SDL_Rect maprect = { 0, -40, 800, 600 };
        SDL_RenderCopy(renderer, texturemap, NULL, &maprect);
        updateAllWalls(head, renderer);
        robotUpdate(renderer, &robot);

        int xDir = round(robot.x+(-10/2)*cos((robot.angle)*PI/180));
        int yDir = round(robot.y+(-10/2)*sin((robot.angle)*PI/180));//+(-ROBOT_HEIGHT/2-SENSOR_VISION+sensor_sensitivity*i)*cos((robot->angle)*PI/180));
        int xTL = (int) xDir;
        int yTL = (int) yDir;
         if(robot.angle==0){
            SDL_Rect dstrect = {xTL+5, yTL, 20, 30 };
            SDL_RenderCopy(renderer, texture0, NULL, &dstrect);
        }else if(robot.angle==15){
            SDL_Rect dstrect = { xTL, yTL, 29, 35 };
            SDL_RenderCopy(renderer, texture15, NULL, &dstrect);
        }else if(robot.angle==30){
            SDL_Rect dstrect = { xTL-5, yTL, 33, 37 };
            SDL_RenderCopy(renderer, texture30, NULL, &dstrect);
        }else if(robot.angle==45){
            SDL_Rect dstrect = { xTL-5, yTL, 37, 37 };
            SDL_RenderCopy(renderer, texture45, NULL, &dstrect);
        }else if(robot.angle==60){
            SDL_Rect dstrect = { xTL-7, yTL, 37, 33 };
            SDL_RenderCopy(renderer, texture60, NULL, &dstrect);
        }else if(robot.angle==75){
            SDL_Rect dstrect = { xTL-7, yTL, 35, 29 };
            SDL_RenderCopy(renderer, texture75, NULL, &dstrect);
        }else if(robot.angle==90){
            SDL_Rect dstrect = { xTL-7, yTL+5, 30, 20 };
            SDL_RenderCopy(renderer, texture90, NULL, &dstrect);
        }else if(robot.angle==105){
            SDL_Rect dstrect = { xTL-9, yTL, 34, 29 };
            SDL_RenderCopy(renderer, texture105, NULL, &dstrect);
        }else if(robot.angle==120){
            SDL_Rect dstrect = { xTL-9, yTL, 37, 33 };
            SDL_RenderCopy(renderer, texture120, NULL, &dstrect);
        }else if(robot.angle==135){
            SDL_Rect dstrect = { xTL-11, yTL-7, 37, 37 };
            SDL_RenderCopy(renderer, texture135, NULL, &dstrect);
        }else if(robot.angle==150){
            SDL_Rect dstrect = { xTL-11, yTL-7, 33, 37 };
            SDL_RenderCopy(renderer, texture150, NULL, &dstrect);
        }else if(robot.angle==165){
            SDL_Rect dstrect = { xTL-9, yTL-7, 29, 34 };
            SDL_RenderCopy(renderer, texture165, NULL, &dstrect);
        }else if(robot.angle==285){
            SDL_Rect dstrect = { xTL, yTL-7, 34, 29 };
            SDL_RenderCopy(renderer, texture285, NULL, &dstrect);
        }else if(robot.angle==300){
            SDL_Rect dstrect = { xTL, yTL-7, 37, 33 };
            SDL_RenderCopy(renderer, texture300, NULL, &dstrect);
        }else if(robot.angle==315){
            SDL_Rect dstrect = { xTL, yTL-7, 37, 37 };
            SDL_RenderCopy(renderer, texture315, NULL, &dstrect);
        }else if(robot.angle==330){
            SDL_Rect dstrect = { xTL, yTL-7, 33, 37 };
            SDL_RenderCopy(renderer, texture330, NULL, &dstrect);
        }else if(robot.angle==345){
            SDL_Rect dstrect = { xTL+2, yTL-5, 29, 34 };
            SDL_RenderCopy(renderer, texture345, NULL, &dstrect);
        } else if (robot.angle==270){
            SDL_Rect dstrect = { xTL, yTL-5, 30, 20 };
            SDL_RenderCopy(renderer, textureL, NULL, &dstrect);
        }else if(robot.angle==195){
            SDL_Rect dstrect = { xTL-7, yTL-12,28, 35 };
            SDL_RenderCopy(renderer, texture195, NULL, &dstrect);
        }else if(robot.angle==210){
            SDL_Rect dstrect = { xTL-7, yTL-12, 33, 37  };
            SDL_RenderCopy(renderer, texture210, NULL, &dstrect);
        }else if(robot.angle==225){
            SDL_Rect dstrect = { xTL-7, yTL-14,37, 37  };
            SDL_RenderCopy(renderer, texture225, NULL, &dstrect);
        }else if(robot.angle==240){
            SDL_Rect dstrect = { xTL-7, yTL-12, 37, 33  };
            SDL_RenderCopy(renderer, texture240, NULL, &dstrect);
        }else if(robot.angle==255){
            printf("%d",robot.angle);
            SDL_Rect dstrect = { xTL-2, yTL-10, 34, 29 };
            SDL_RenderCopy(renderer, texture255, NULL, &dstrect);
        }
        else if (robot.angle==180){
           SDL_Rect dstrect = { xTL-5, yTL-10, 20, 30 };
            SDL_RenderCopy(renderer, texture, NULL, &dstrect);
            SDL_RenderPresent(renderer);
        }


        if(robot.auto_mode==0){
            SDL_RenderCopy(renderer, texturetitle, NULL, NULL);
        }

        // Check for user input
        SDL_RenderPresent(renderer);
        while(SDL_PollEvent(&event)){

            if(event.type == SDL_QUIT){
                done = 1;
            }
            const Uint8 *state = SDL_GetKeyboardState(NULL);
            if(state[SDL_SCANCODE_UP] && robot.direction != DOWN){
                robot.direction = UP;
            }
            if(state[SDL_SCANCODE_DOWN] && robot.direction != UP){
                robot.direction = DOWN;
            }
            if(state[SDL_SCANCODE_LEFT] && robot.direction != RIGHT){
                robot.direction = LEFT;
            }
            if(state[SDL_SCANCODE_RIGHT] && robot.direction != LEFT){
                robot.direction = RIGHT;
            }
            if(state[SDL_SCANCODE_SPACE]){
                setup_robot(&robot);
            }
            if(state[SDL_SCANCODE_RETURN]){
                robot.auto_mode = 1;
                start_time = clock();
            }
        }

        SDL_Delay(120);
    }
    SDL_DestroyTexture(texture);
    SDL_FreeSurface(image);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    printf("DEAD\n");
}
