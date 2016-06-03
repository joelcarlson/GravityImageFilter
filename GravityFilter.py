from PIL import Image

class GravityFilter(object):

    def __init__(self, source_image_path, n_colors, mult=1, quant_method=1, thumbnail=True):
        self.n_colors = n_colors
        self.source_image = Image.open(source_image_path)
        self.source_image.thumbnail((128,128))
        self.mult = mult
        self.thumbnail = thumbnail

        #0 = median cut, 1 = max coverage, 2 = octree
        self.source_quantized = self.source_image.quantize(colors = n_colors, method=quant_method)
        # Get well formatted source palette
        self.source_palette = self._pal_lst_to_tuples(self.source_quantized.getpalette())

    def _pal_lst_to_tuples(self, quantized_image):
        # Image.quantize.getpalette returns a list
        # This function converts that list to a list
        # of tuples in format (R, G, B)

        #3 for r,g, and b
        it = [iter(quantized_image[:self.n_colors*3])] * 3
        return zip(*it)


    def _rgb_distance(self, source, target):
        # Given an RGB tuple, return euclidean distance to other tuple
        if source == target:
            return 0.0000000001
        return sum([(x-y)**2 for x,y in zip(source, target)])**0.5

    def _modify_color(self, px_tuple, pal_tuples):
        """
        param px_tuple acquired from Image.getpixel((x,y))
        param pal_tuples acquired from pal_lst_to_tuples(Image.getpalette(), n_colors)
        return tuple of modified R,G,B components (r,g,b)
        """
        #Coef is currently 1/distance^2 where distance is RGB space euclidean distance
        coefs = [self.mult*1/(self._rgb_distance(px_tuple, col)**2) for col in pal_tuples]
        vectors = [(px_tuple[0] - col[0], px_tuple[1] - col[1], px_tuple[2] - col[2]) for col in pal_tuples]

        #multiply vectors by coefs
        vectors = [(vec[0]*coef, vec[1]*coef, vec[2]*coef) for vec,coef in zip(vectors, coefs)]

        # Sum components of the vectors
        px_move = map(sum, zip(*vectors))

        return tuple([int(pos+dir) for pos,dir in zip(px_tuple, px_move)])

    def filter_image(self, target_image_path):
        """
        param source object of class Image
        param target object of class Image
        param palette palette in same format as Image.getpalette()
        """
        target = Image.open(target_image_path)
        if self.thumbnail:
            target.thumbnail((512,512))

        for x in range(target.size[0]):
            #if x % 10 == 0:
            #    print x
            for y in range(target.size[1]):
                cur_px = target.getpixel((x,y))

                #this is a hacky fix for when the px value is too close to
                # white. If the px is too close, then it overshoots white and
                # and becomes a random color
                if sum(cur_px) > 550:
                    continue
                mod_px = self._modify_color(cur_px, self.source_palette)

                # Make sure colors stay in RGB range
                if mod_px[0] > 255:
                    mod_px = (255, mod_px[1], mod_px[2])
                if mod_px[1] > 255:
                    mod_px = (mod_px[0], 255, mod_px[2])
                if mod_px[2] > 255:
                    mod_px = (mod_px[0], mod_px[1], 255)


                target.putpixel((x,y), mod_px)

        self.filtered_image =  target




if __name__ == "__main__":
    source_image_path = "test_images/sunset_good.jpg"
    target_image_path = "test_images/sunset_bad.jpg"

    test = GravityFilter(source_image_path, 10, mult=1500, quant_method=1)
    test.filter_image(target_image_path)
    test.filtered_image.save('output/target_filtered.png')

    good = Image.open(source_image_path)
    good.thumbnail((512,512))
    good.save('output/source.png')

    bad = Image.open(target_image_path)
    bad.thumbnail((512,512))
    bad.save('output/target.png')

    test.source_quantized.save('output/quantized.png')
