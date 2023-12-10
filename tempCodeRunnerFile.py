
        #     column = (-1)**i
        #     if array.slot[self.slot[0], self.slot[1]+column] == 2:
        #         for j in range(2):
        #             row = (-1)**(i+j+1)
        #             if array.slot[self.slot[0]+row, self.slot[1]+column] == 2:
        #                 self.surround[2**i+j] = 1
        # for idx, val in enumerate(self.surround):
        #     if val == True:
        #         self.image = pygame.transform.rotate(bullet_corner_img, 180+idx*90)
        #         return