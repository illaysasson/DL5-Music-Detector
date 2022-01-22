class BoundingBox:
    def __init__(self, category, x, y, width, height, image_width=None, image_height=None):
        self.category, self.x, self.y, self.width, self.height = category, x, y, width, height

        self.bbox = [self.category, self.x, self.y, self.width, self.height]
        if x < 1: # Doesn't account for screen-wide bboxes
            self.bbox = self.absolute_bbox(self.bbox, image_width, image_height)
            self.category, self.x, self.y, self.width, self.height = self.bbox

        self.min_corner, self.max_corner = self.bbox_to_corner(self.bbox)

    def absolute_bbox(self, bbox, image_width, image_height):
        abs_mid_x, abs_mid_y, abs_width, abs_height = bbox[1] * image_width, bbox[2] * image_height, bbox[3] * image_width, bbox[4] * image_height
        abs_bbox = [bbox[0], round(abs_mid_x), round(abs_mid_y), round(abs_width), round(abs_height)]

        return abs_bbox

    def bbox_to_corner(self, bbox):
        category, abs_mid_x, abs_mid_y, abs_width, abs_height = bbox
        abs_min_x, abs_min_y = round(abs_mid_x - abs_width/2), round(abs_mid_y - abs_height/2)
        min_corner = (abs_min_x, abs_min_y)

        abs_max_x, abs_max_y = round(abs_mid_x + abs_width/2), round(abs_mid_y + abs_height/2)
        max_corner = (abs_max_x, abs_max_y)

        return min_corner, max_corner

    def __str__(self):
        return str(self.bbox)

    def __repr__(self):
        return str(self)
