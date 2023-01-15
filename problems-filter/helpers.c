#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float average;
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            average = round((image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) / 3.00);
            image[i][j].rgbtBlue = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtRed = average;
        }
    }
    return;
}

int limit(int RGB)
{
    if (RGB > 255)
    {
        RGB = 255;
    }
    return RGB;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    float sepiaBlue;
    float sepiaGreen;
    float sepiaRed;
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sepiaBlue = limit(round(0.272 * image[i][j].rgbtRed + 0.534 * image[i][j].rgbtGreen + 0.131 * image[i][j].rgbtBlue));
            sepiaGreen = limit(round(0.349 * image[i][j].rgbtRed + 0.686 * image[i][j].rgbtGreen + 0.168 * image[i][j].rgbtBlue));
            sepiaRed = limit(round(0.393 * image[i][j].rgbtRed + 0.769 * image[i][j].rgbtGreen + 0.189 * image[i][j].rgbtBlue));

            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtRed = sepiaRed;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE rgb;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            rgb = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = rgb;
        }
    }
    return;
}

int get_blur(int i, int j, int height, int width, RGBTRIPLE image[height][width], int color)
{
    float counter = 0;
    int sum = 0;
    
    for (int k = i - 1; k < (i + 2); k++) 
    {
        for (int l = j - 1; l < (j + 2); l++)
        {
            if (k < 0 || k >= height || l < 0 || l >= width)
            {
                continue;
            }
                    
            if (color == 0)
            {
                sum += image[k][l].rgbtBlue;
            }
            else if (color == 1)
            {
                sum += image[k][l].rgbtGreen;
            }    
            else
            {
                sum += image[k][l].rgbtRed;
            }   
            
            counter++;
        }
    }
    
    return round(sum / counter);
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtBlue = get_blur(i, j, height, width, copy, 0);
            image[i][j].rgbtGreen = get_blur(i, j, height, width, copy, 1);
            image[i][j].rgbtRed = get_blur(i, j, height, width, copy, 2);
        }
    }
    
    return;
}
