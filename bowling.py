"""bowling"""


class Frame:
    """Frame"""

    def __init__(self, num):
        """Frame init"""
        self.num = num
        self.throws = []

    @property
    def is_done(self):
        """function to check frame is completed"""
        return sum(self.throws) == 10 or len(self.throws) == 2

    @property
    def check_strike(self):
        """check frame is a strike"""
        return sum(self.throws) == 10 and len(self.throws) == 1

    @property
    def check_spare(self):
        """check frame is a spare"""
        return sum(self.throws) == 10 and len(self.throws) == 2

    def score(self, next_throws):
        """calculate the frame score"""
        res = sum(self.throws)
        if self.check_strike:
            res += sum(next_throws[:2])
        elif self.check_spare:
            res += sum(next_throws[:1])
        return res

    def roll(self, pins):
        """record the pins on a frame"""
        if pins < 0 or pins > 10:
            raise ValueError('invalid pins {} in frame {}, value must be 1 to 10'.format(
                pins, self.num))
        if sum(self.throws) + pins > 10:
            raise ValueError('invalid pins {} frame {} sum or rolls cannot exceed 10 pins'.format(
                pins, self.num))
        if len(self.throws) == 2:
            raise ValueError('you cannot roll more then twice in the frame {}'.format(self.num))
        self.throws.append(pins)


class Game:
    """Game"""

    def __init__(self):
        """Game init"""
        self.bonus_throws = []
        self.frames = [Frame(i) for i in range(1, 11)]
        self.frame_num = 0

    @property
    def current_frame(self):
        """get current frame object"""
        return self.get_frame(self.frame_num)

    def get_frame(self, frame_num):
        """get frame by frame number"""
        return self.frames[frame_num]

    def next_throws(self, frame_num):
        """get all next throws"""
        next_throws = []
        next_frame_num = frame_num + 1
        while next_frame_num < 10:
            next_throws += self.get_frame(next_frame_num).throws
            next_frame_num += 1
        next_throws += self.bonus_throws
        return next_throws

    def handle_bonus_throw(self, pins):
        """handle 10th frame bonus throws"""
        if self.get_frame(9).check_spare:
            if len(self.bonus_throws) == 1:
                raise ValueError('invalid play, no bonus rounds available to play')
            self.bonus_throws += [pins]
        elif self.get_frame(9).check_strike:
            if len(self.bonus_throws) == 2:
                raise ValueError('invalid play, no bonus rounds available to play')
            if sum(self.bonus_throws + [pins]) > 10:
                if len(self.bonus_throws) == 1 and self.bonus_throws[0] == 10:
                    pass
                else:
                    raise ValueError('invalid pings value')
            self.bonus_throws += [pins]
        else:
            raise ValueError('invalid play bonus throw can be played on 10th frame strike or spare')

    def roll(self, pins):
        """bowling rolls in a frame"""
        if self.frame_num == 10:
            self.handle_bonus_throw(pins)
        else:
            self.current_frame.roll(pins)
            if self.current_frame.is_done:
                self.frame_num += 1

    def score(self):
        """calculate final score"""
        if self.frame_num < 10:
            raise IndexError('Game is still in progress, cannot show score now')
        if self.get_frame(9).check_spare:
            if len(self.bonus_throws) != 1:
                raise IndexError('If the final frame is a spare one bonus roll must be taken.')
        if self.get_frame(9).check_strike:
            if len(self.bonus_throws) != 2:
                raise IndexError('If the final frame is a strike two bonus rolls must be taken.')
        return sum(frame.score(self.next_throws(frame.num))
                   for frame in self.frames)

    def display_score_board(self):
        """display score board with frame number and score"""
        frame_numbers = ""
        rolls = ""
        for frame in self.frames:
            frame_numbers = "{}   {}   ".format(frame_numbers, frame.num)
            rolls = "{}  {}  ".format(rolls, "|".join([str(i) for i in frame.throws]))
            if frame.num == 10 and (frame.check_strike or frame.check_spare):
                rolls = "{}|{}".format(rolls, "|".join([str(i) for i in self.bonus_throws]))
        print("\nScore Board\n{}\n{}".format(frame_numbers, rolls))
