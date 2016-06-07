# Gravity Image Filter

A proof of concept for an image filter that works like gravity, but for colors!

This is a *highly unpolished* class for modifying the colors of a target image using the palette of a source image of presumably higher quality.


### Method

The algorithm is as follows:

  1. Extract color palette of length **N** from source image
  2. For each pixel in the target image:
    1. Get pixel color in RGB
    2. Calculate euclidean distance of pixel color to each color in the palette
    3. Move colors of pixel in RGB space a distance proportional to the inverse of the squared euclidean distance between the pixel and each color in the palette

The algorithm thus moves a target pixel color closer to the colors in the palette that it is already closer to. Colors that the target pixel is further from have little effect. This, in practice, "pulls" the target image toward the source image.

### Example

Below is an example of taking a somewhat washed out image of a sunset, and pulling it towards an image with better color balance:

The code for creating this would look like:

``` python
source_image_path = "test_images/sunset_good.jpg"
target_image_path = "test_images/sunset_bad.jpg"

sunset_filter = GravityFilter(source_image_path, n_colors=9, mult=1500)
sunset_filter.filter_image(target_image_path)
sunset_filter.filtered_image.show()
```

#### Source Image (good quality sunset)

<img src="https://raw.githubusercontent.com/joelcarlson/GravityImageFilter/master/output/source.png" />


#### Source Image Quantized

These are the colors which make up the extracted palette:

<img src="https://raw.githubusercontent.com/joelcarlson/GravityImageFilter/master/output/quantized.png" />


#### Target Image (washed out sunset)

<img src="https://raw.githubusercontent.com/joelcarlson/GravityImageFilter/master/output/target.png" />

#### Filtered Target Image

<img src="https://raw.githubusercontent.com/joelcarlson/GravityImageFilter/master/output/target_filtered.png" />

### Conclusion

The filtered image is certainly more varied in it's colors, and is perhaps more pleasing to the eye. 
